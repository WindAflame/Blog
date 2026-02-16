import sys
from .article_generator import ArticleGenerator
from .config import MIHOYO_GAMES


def print_usage():
    """Print usage information"""
    print("Usage: python -m src.main <game_key> <update_igdb_id>")
    print()
    print("Arguments:")
    print("  game_key        Game identifier (required)")
    print("                  Available: genshin, starrail, zzz")
    print("  update_igdb_id  IGDB ID of the game update/version (required)")
    print()
    print("Examples:")
    print("  python -m src.main genshin 378320")
    print("  python -m src.main starrail 123456")
    print("  python -m src.main zzz 654321")
    print()
    print("How it works:")
    print("  1. Fetches update details from IGDB using the update_igdb_id")
    print("  2. Extracts version name from the IGDB data (e.g., 'Luna III', '6.2')")
    print("  3. Searches for news article containing the version and update keywords")
    print("  4. Generates bilingual articles (EN/FR) with banner and links")


def main():
    """Main CLI entry point"""
    if len(sys.argv) < 3 or sys.argv[1] in ["-h", "--help"]:
        print_usage()
        return

    game_key = sys.argv[1]
    update_igdb_id = sys.argv[2]

    # Validate game key
    if game_key not in MIHOYO_GAMES:
        print(f"Error: Unknown game '{game_key}'")
        print(f"Available games: {', '.join(MIHOYO_GAMES.keys())}")
        sys.exit(1)

    try:
        print(f"Generating article for {MIHOYO_GAMES[game_key].game_name} update...")
        print(f"Update IGDB ID: {update_igdb_id}")
        print()

        generator = ArticleGenerator()
        generator.generate_article(game_key, update_igdb_id)

        print()
        print("✓ Article generation completed successfully!")

    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
