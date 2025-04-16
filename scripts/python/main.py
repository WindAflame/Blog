import json
import os
from typing import Any
from dotenv import load_dotenv
from igdb.wrapper import IGDBWrapper
import logging

# Configure the logger
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

# Constants
DESTINATION_DIRECTORY = 'static'

# Methods
def __retrieve_game_information(wrapper: IGDBWrapper, game_id: str) -> Any:
    if (data := __read_game_json(game_id)) != None:
        logger.info('Game data finded at dest folder. Load it instead of request API.')
        return data
    full_fields = 'age_ratings,aggregated_rating,aggregated_rating_count,alternative_names,artworks,bundles,category,checksum,collection,collections,cover,created_at,dlcs,expanded_games,expansions,external_games,first_release_date,follows,forks,franchise,franchises,game_engines,game_localizations,game_modes,game_status,game_type,genres,hypes,involved_companies,keywords,language_supports,multiplayer_modes,name,parent_game,platforms,player_perspectives,ports,rating,rating_count,release_dates,remakes,remasters,screenshots,similar_games,slug,standalone_expansions,status,storyline,summary,tags,themes,total_rating,total_rating_count,updated_at,url,version_parent,version_title,videos,websites' 
    blog_fields = 'aggregated_rating,artworks,category,genres,involved_companies,name,platforms,rating,summary,url,videos,websites,game_type'
    byte_array = wrapper.api_request(
        'games',
        f'fields {blog_fields}; offset 0; where id={game_id};'
    )
    return json.loads(byte_array)[0]

def __search_and_replace_artworks(wrapper: IGDBWrapper, ids: list[int]):
    if all(isinstance(id, str) for id in ids) :
        return ids
    byte_array = wrapper.api_request(
        'artworks',
        f'fields *; where id={','.join([str(i) for i in ids])};'
    )
    return list(map(lambda artwork: artwork['image_id'], json.loads(byte_array)))

def __search_and_replace_by_url_for_websites(wrapper: IGDBWrapper, id: str | list[str]):
    requests_id = id
    if isinstance(id,list):
        requests_id = ','.join([str(i) for i in id])
    byte_array = wrapper.api_request(
        'websites',
        f'fields *; where id={requests_id};'
    )
    return json.loads(byte_array)

def __search_and_replace_by_url_for_videos(wrapper: IGDBWrapper, id: str | list[str]):
    requests_id = id
    if isinstance(id,list):
        requests_id = ','.join([str(i) for i in id])
    byte_array = wrapper.api_request(
        'game_videos',
        f'fields *; where id={requests_id};'
    )
    return json.loads(byte_array)

def __read_game_json(game_id: str) -> Any | None:
    filepath = os.path.join(DESTINATION_DIRECTORY, game_id + '.json')
    if not os.path.exists(filepath):
        return None
    data = None
    with open(filepath, 'r') as f:
        data = json.load(f)
    return data

def __write_game_json(data: Any, game_id: str) -> str:
    if not os.path.isdir(DESTINATION_DIRECTORY):
        os.makedirs(DESTINATION_DIRECTORY)
    filepath = os.path.join(DESTINATION_DIRECTORY, game_id + '.json')
    if os.path.exists(filepath):
        logger.warning('Override %s is planned !', filepath)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)
    return filepath

# Application
def main():
    load_dotenv()
    logger.info('Environment variable is loaded.')
    if (
        not (client_id := os.getenv('client')) 
        or not (access_token := os.getenv('token'))
        or not (game_id := os.getenv('game'))
    ):
        raise Exception('Env file not completed')
    wrapper = IGDBWrapper(client_id, access_token)    
    logger.info('Search game %s on IGDB API.', game_id)
    game_json_object = __retrieve_game_information(wrapper, game_id)
    game_json_object['artworks'] = __search_and_replace_artworks(wrapper, game_json_object['artworks'])
    # game_json_object['videos'] = __search_and_replace_x(wrapper, game_json_object['x'])
    # game_json_object['category'] = __search_and_replace_x(wrapper, game_json_object['x'])
    # game_json_object['websites'] = __search_and_replace_x(wrapper, game_json_object['x'])

    filepath = __write_game_json(game_json_object, game_id)
    logger.info('Game information of id=%s is available in file at %s', game_id, filepath)



if __name__ == "__main__":
    main()
