import argparse
import logging
import sys
from .article_generator import ArticleGenerator
from .modules import get_module, MODULES

logger = logging.getLogger(__name__)


def main():
    """Main CLI entry point"""
    parser = argparse.ArgumentParser(
        description="Generate IGDB game update articles",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""\
Examples:
  # Generic mode (any IGDB game):
  python -m src.main 378320

  # With a module (e.g., mihoyo):
  python -m src.main --module mihoyo genshin 378320
  python -m src.main --module mihoyo starrail 123456

Available modules: %(modules)s
""" % {"modules": ", ".join(MODULES.keys()) or "(none)"},
    )

    parser.add_argument(
        "--module", "-m",
        type=str,
        default=None,
        help="Module to use (e.g., mihoyo). Without a module, works generically with any IGDB game.",
    )
    parser.add_argument(
        "--output", "-o",
        type=str,
        default=None,
        help="Output directory (overrides .env output_dir). Default: output/",
    )
    parser.add_argument(
        "args",
        nargs="+",
        help="Without --module: <update_igdb_id>. With --module: <game_key> <update_igdb_id>",
    )

    parsed = parser.parse_args()

    # Resolve module
    try:
        module = get_module(parsed.module)
    except ValueError as e:
        logger.error("%s", e)
        sys.exit(1)

    # Parse positional args based on whether a module is used
    if parsed.module:
        # With module: expect <game_key> <update_igdb_id>
        if len(parsed.args) < 2:
            logger.error("With --module %s, expected: <game_key> <update_igdb_id>", parsed.module)
            available = module.get_available_games()
            if available:
                logger.info("Available games: %s", ", ".join(available.keys()))
            sys.exit(1)
        game_key = parsed.args[0]
        update_igdb_id = parsed.args[1]
    else:
        # Without module: expect <update_igdb_id>
        game_key = None
        update_igdb_id = parsed.args[0]

    try:
        game_label = f"{game_key} " if game_key else ""
        logger.info("Generating article for %supdate (IGDB ID: %s)...", game_label, update_igdb_id)

        generator = ArticleGenerator(module, output_dir=parsed.output)
        generator.generate_article(update_igdb_id, game_key=game_key)

        logger.info("Done!")

    except Exception as e:
        logger.error("%s", e)
        sys.exit(1)


if __name__ == "__main__":
    main()
