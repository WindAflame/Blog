import json
import os
from typing import Any, Callable
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
    fields = "id,aggregated_rating,artworks,genres,involved_companies,name,parent_game,platforms,rating,slug,summary,videos,game_type"
    byte_array = wrapper.api_request(
        "games", f"fields {fields}; offset 0; where id={game_id};"
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
    callback: Callable[[list[dict], IGDBWrapper], list[any]] = None,
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
        return result if not callback else callback(result, wrapper)
    if isinstance(ids, int):
        result = __requests(wrapper, url_name, key_name, ids)[0]
        return result if not callback else callback(result, wrapper)


def __transform_to_slug_item(data: dict, wrapper: IGDBWrapper):
    return {"name": data["name"], "slug": data["slug"]}


def __transform_to_slug_list(datas: list[dict], wrapper: IGDBWrapper):
    return list(map(lambda i: __transform_to_slug_item(i, wrapper), datas))


def __transform_artworks(datas: list[dict], wrapper: IGDBWrapper):
    return list(map(lambda i: i["image_id"], datas))


def __transform_companies(involved_companies_data: list[dict], wrapper: IGDBWrapper):
    for index, involved_company_data in enumerate(involved_companies_data):
        involved_companies_data[index] = __transform_attribut_from_data(
            wrapper, "companies", "company", involved_company_data, None
        )
    return __transform_to_slug_list(involved_companies_data, wrapper)


def __transform_game_type(data: dict, wrapper: IGDBWrapper):
    return data["type"]


def __transform_to_video_list(datas: list[dict], wrapper: IGDBWrapper):
    return list(map(lambda i: i["video_id"], datas))


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
        ("game_types", "game_type", __transform_game_type),
        ("genres", "genres", __transform_to_slug_list),
        ("involved_companies", "involved_companies", __transform_companies),
        ("games", "parent_game", __transform_to_slug_item),
        ("platforms", "platforms", __transform_to_slug_list),
        ("game_videos", "videos", __transform_to_video_list),
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
