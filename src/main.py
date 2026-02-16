import logging

from src.config import load_config, parse_args
from src.igdb_client import IGDBClient

logger = logging.getLogger(__name__)


def main():
    args = parse_args()
    config = load_config(game_id_override=args.game_id, output_dir_override=args.output)
    client = IGDBClient(config["client_id"], config["access_token"], config["output_dir"])
    game_id = config["game_id"]

    logger.info("Search game %s on IGDB API.", game_id)
    game_data = client.retrieve_game(game_id)

    logger.info(
        "Process game information so that it can be processed by the application"
    )
    client.transform_game_data(game_data)

    logger.info("Save in progress ...")
    filepath = client.write_game_json(game_id, game_data)
    logger.info(
        "Game information of id=%s is available in file at %s", game_id, filepath
    )


if __name__ == "__main__":
    main()
