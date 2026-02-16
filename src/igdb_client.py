import json
import logging
import os
from typing import Any, Callable

from igdb.wrapper import IGDBWrapper

logger = logging.getLogger(__name__)


class IGDBClient:
    def __init__(self, client_id: str, access_token: str, output_dir: str):
        self._wrapper = IGDBWrapper(client_id, access_token)
        self._output_dir = output_dir

    def request(self, url_name: str, key_name: str | None, ids: any) -> list[dict]:
        if key_name is None:
            key_name = url_name
        if isinstance(ids, list):
            ids = (
                "(" + ",".join([str(i) for i in ids]) + ")"
                if len(ids) > 1
                else ids[0]
            )
        byte_array = self._wrapper.api_request(
            url_name, f"fields * ; where id = {ids};"
        )
        return json.loads(byte_array)

    def retrieve_game(self, game_id: str) -> dict:
        if (data := self._read_game_json(game_id)) is not None:
            logger.info(
                "Game data finded at dest folder. Load it instead of request API."
            )
            return data
        fields = "id,aggregated_rating,artworks,genres,involved_companies,name,parent_game,platforms,rating,slug,summary,videos,game_type"
        byte_array = self._wrapper.api_request(
            "games", f"fields {fields}; offset 0; where id={game_id};"
        )
        return json.loads(byte_array)[0]

    def transform_game_data(self, game_data: dict) -> dict:
        for url, key, callback in [
            ("artworks", "artworks", self._transform_artworks),
            ("game_types", "game_type", self._transform_game_type),
            ("genres", "genres", self._transform_to_slug_list),
            (
                "involved_companies",
                "involved_companies",
                self._transform_companies,
            ),
            ("games", "parent_game", self._transform_to_slug_item),
            ("platforms", "platforms", self._transform_to_slug_list),
            ("game_videos", "videos", self._transform_to_video_list),
        ]:
            if data_transformed := self._transform_attribut_from_data(
                url, key, game_data, callback
            ):
                game_data[key] = data_transformed
        return game_data

    def _transform_attribut_from_data(
        self,
        url_name: str,
        key_name: str | list[str] | None,
        game_data: dict,
        callback: Callable[[list[dict]], list[any]] = None,
    ):
        if isinstance(key_name, list):
            ids = game_data[key_name[0]]
            for index in range(len(key_name)):
                if index != 0:
                    ids = list(map(lambda i: i[key_name[index]], ids))
        else:
            if key_name not in game_data:
                return
            ids = game_data[key_name]
        if isinstance(ids, list):
            if not all(isinstance(id, int) for id in ids):
                return
            result = self.request(url_name, key_name, ids)
            return result if not callback else callback(result)
        if isinstance(ids, int):
            result = self.request(url_name, key_name, ids)[0]
            return result if not callback else callback(result)

    def _transform_to_slug_item(self, data: dict) -> dict:
        return {"name": data["name"], "slug": data["slug"]}

    def _transform_to_slug_list(self, datas: list[dict]) -> list[dict]:
        return list(map(lambda i: self._transform_to_slug_item(i), datas))

    def _transform_artworks(self, datas: list[dict]) -> list[str]:
        return list(map(lambda i: i["image_id"], datas))

    def _transform_companies(self, involved_companies_data: list[dict]) -> list[dict]:
        for index, involved_company_data in enumerate(involved_companies_data):
            involved_companies_data[index] = self._transform_attribut_from_data(
                "companies", "company", involved_company_data, None
            )
        return self._transform_to_slug_list(involved_companies_data)

    def _transform_game_type(self, data: dict) -> str:
        return data["type"]

    def _transform_to_video_list(self, datas: list[dict]) -> list[str]:
        return list(map(lambda i: i["video_id"], datas))

    def _read_game_json(self, game_id: str) -> Any | None:
        filepath = os.path.join(self._output_dir, game_id + ".json")
        if not os.path.exists(filepath):
            return None
        with open(filepath, "r") as f:
            data = json.load(f)
        return data

    def write_game_json(self, game_id: str, game_data: dict) -> str:
        if not os.path.isdir(self._output_dir):
            os.makedirs(self._output_dir)
        filepath = os.path.join(self._output_dir, game_id + ".json")
        if os.path.exists(filepath):
            logger.warning("Override %s is planned !", filepath)
        with open(filepath, "w") as f:
            json.dump(game_data, f, indent=4)
        return filepath
