import json
import os
from typing import Any
from dotenv import load_dotenv
from igdb.wrapper import IGDBWrapper
import logging

# Configure the logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("app.log"), logging.StreamHandler()],
)

logger = logging.getLogger(__name__)

# Constants
DESTINATION_DIRECTORY = "static"

# Methods
def __requests(
    wrapper: IGDBWrapper, url_name: str, key_name: str | None, requests_id: any
):
    if key_name is None:
        key_name = url_name
    if isinstance(requests_id, list):
        requests_id = (
            "(" + ",".join([str(i) for i in requests_id]) + ")"
            if len(requests_id) > 1
            else requests_id[0]
        )
    byte_array = wrapper.api_request(url_name, f"fields * ; where id = {requests_id};")
    return json.loads(byte_array)


def __retrieve_game_information(wrapper: IGDBWrapper, game_id: str) -> Any:
    if (data := __read_game_json(game_id)) != None:
        logger.info("Game data finded at dest folder. Load it instead of request API.")
        return data
    byte_array = wrapper.api_request(
        "games", f"fields *; offset 0; where id={game_id};"
    )
    return json.loads(byte_array)[0]

def __read_game_json(game_id: str) -> Any | None:
    filepath = os.path.join(DESTINATION_DIRECTORY, game_id + ".json")
    if not os.path.exists(filepath):
        return None
    data = None
    with open(filepath, "r") as f:
        data = json.load(f)
    return data


def __write_game_json(game_id: str, game_data: dict) -> str:
    if not os.path.isdir(DESTINATION_DIRECTORY):
        os.makedirs(DESTINATION_DIRECTORY)
    filepath = os.path.join(DESTINATION_DIRECTORY, game_id + ".json")
    if os.path.exists(filepath):
        logger.warning("Override %s is planned !", filepath)
    with open(filepath, "w") as f:
        json.dump(game_data, f, indent=4)
    return filepath


def __transform_attribut_from_data(
    wrapper: IGDBWrapper,
    url_name: str,
    key_name: str | list[str] | None,
    game_data: dict,
    callback=None,
):
    if isinstance(key_name, list):
        ids = game_data[key_name[0]]
        for index in range(len(key_name)):
            if index != 0:
                ids = list(map(lambda i: i[key_name[index]], ids))
    else:
        ids = game_data[key_name]
    if isinstance(ids, list):
        if not all(isinstance(id, int) for id in ids):
            return
        result = __requests(wrapper, url_name, key_name, ids)
        return result if not callback else callback(result)
    if isinstance(ids, int):
        return __requests(wrapper, url_name, key_name, ids)[0]


def __transform_artworks(artwork_data: list[dict]):
    return list(map(lambda i: i["image_id"], artwork_data))

def __transform_genres(genres_data: list[dict]):
    return list(
        map(lambda i: {"name": i["name"], "slug": i["slug"]}, genres_data)
    )

def __transform_companies(companies_data: list[dict]):
    return list(
        map(lambda i: {"name": i["name"], "slug": i["slug"]}, companies_data)
    )


# Application
def main():
    load_dotenv()
    logger.info("Environment variable is loaded.")
    if (
        not (client_id := os.getenv("client"))
        or not (access_token := os.getenv("token"))
        or not (game_id := os.getenv("game"))
    ):
        raise Exception("The environment file does not contain the required fields")
    wrapper = IGDBWrapper(client_id, access_token)
    logger.info("Search game %s on IGDB API.", game_id)
    game_data = __retrieve_game_information(wrapper, game_id)
    logger.info(
        "Process game information so that it can be processed by the application"
    )
    for url, key, callback in [
        ("artworks", "artworks", __transform_artworks),
        ("game_types", "game_type", None),
        ("genres", "genres", __transform_genres),
        ("involved_companies", "involved_companies", None),
         # FIXME: final assertion not work
        ("companies", ["involved_companies", "company"], __transform_companies),
    ]:
        if data_transformed := __transform_attribut_from_data(
            wrapper, url, key, game_data, callback
        ):
            game_data[key] = data_transformed

    logger.info("Save in progress ...")
    filepath = __write_game_json(game_id, game_data)
    logger.info(
        "Game information of id=%s is available in file at %s", game_id, filepath
    )


if __name__ == "__main__":
    main()
