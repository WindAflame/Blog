import requests
from typing import Optional
from ...models.news_article import NewsArticle


class EnneadAPIClient:
    """Client for interacting with api.ennead.cc"""

    def __init__(self, api_url: str):
        """
        Initialize the Ennead API client

        Args:
            api_url: Base URL for the news API
        """
        self.api_url = api_url

    def get_latest_news(self) -> Optional[NewsArticle]:
        """
        Fetch the latest news article

        Returns:
            NewsArticle instance or None if no articles found
        """
        try:
            response = requests.get(self.api_url, timeout=10)
            response.raise_for_status()

            articles = response.json()

            if not articles or not isinstance(articles, list):
                return None

            # Return the first (most recent) article
            return NewsArticle.from_api_response(articles[0])

        except (requests.RequestException, KeyError, IndexError) as e:
            print(f"Error fetching news from Ennead API: {e}")
            return None

    def get_news_by_title_keyword(self, keyword: str) -> Optional[NewsArticle]:
        """
        Fetch a news article by searching for a keyword in the title

        Args:
            keyword: Keyword to search for in article titles

        Returns:
            NewsArticle instance or None if not found
        """
        try:
            response = requests.get(self.api_url, timeout=10)
            response.raise_for_status()

            articles = response.json()

            if not articles or not isinstance(articles, list):
                return None

            # Search for article with keyword in title
            for article_data in articles:
                if keyword.lower() in article_data.get("title", "").lower():
                    return NewsArticle.from_api_response(article_data)

            # If no match found, return latest article
            return NewsArticle.from_api_response(articles[0])

        except (requests.RequestException, KeyError, IndexError) as e:
            print(f"Error fetching news from Ennead API: {e}")
            return None

    def get_update_news_by_version(self, version_keywords) -> Optional[NewsArticle]:
        """
        Fetch update news article by version keywords

        Searches for articles containing both the version keyword and
        "update details" keywords, prioritizing them over maintenance announcements

        Args:
            version_keywords: Version keyword(s) to search (string or list)
                            (e.g., "Luna III", ["Luna III", "6.2", "A Nocturne of the Far North"])

        Returns:
            NewsArticle instance or None if not found
        """
        try:
            # Ensure version_keywords is a list
            if isinstance(version_keywords, str):
                version_keywords = [version_keywords]

            response = requests.get(self.api_url, timeout=10)
            response.raise_for_status()

            articles = response.json()

            if not articles or not isinstance(articles, list):
                return None

            # Priority keywords for update details (highest priority)
            # Must be exact match
            details_keywords = [
                "update details",
                "détails de la mise à jour",
            ]

            # Secondary keywords (lower priority)
            update_keywords = [
                "version",
                "update",
                "mise à jour",
            ]

            # Keywords to avoid (maintenance, preview, version details, what's new, etc.)
            avoid_keywords = [
                "maintenance",
                "preview",
                "version details",  # Avoid "Version Details", we want "Update Details"
                "what's new",       # Avoid "What's New"
            ]

            version_keywords_lower = [kw.lower() for kw in version_keywords]

            # First pass: Look for articles with version + "update details" (highest priority)
            # ONLY check title, NOT description (to avoid false matches)
            for article_data in articles:  # Check ALL articles
                title_lower = article_data.get("title", "").lower()

                # Check if ANY version keyword is in TITLE ONLY
                has_version = any(
                    version_kw in title_lower
                    for version_kw in version_keywords_lower
                )

                # Check if "update details" keywords are in TITLE ONLY
                has_details_keyword = any(
                    keyword in title_lower
                    for keyword in details_keywords
                )

                # Skip if contains avoid keywords (title only)
                has_avoid_keyword = any(
                    keyword in title_lower
                    for keyword in avoid_keywords
                )
                if has_avoid_keyword:
                    continue

                if has_version and has_details_keyword:
                    return NewsArticle.from_api_response(article_data)

            # Second pass: Look for articles with version + update keywords (medium priority)
            # ONLY check title
            for article_data in articles:
                title_lower = article_data.get("title", "").lower()

                # Skip if contains avoid keywords
                has_avoid_keyword = any(
                    keyword in title_lower
                    for keyword in avoid_keywords
                )
                if has_avoid_keyword:
                    continue

                # Check if ANY version keyword is in TITLE ONLY
                has_version = any(
                    version_kw in title_lower
                    for version_kw in version_keywords_lower
                )

                # Check if any update keyword is in TITLE ONLY
                has_update_keyword = any(
                    keyword in title_lower
                    for keyword in update_keywords
                )

                if has_version and has_update_keyword:
                    return NewsArticle.from_api_response(article_data)

            # Third pass: Just look for version keyword (lowest priority, still filter avoid keywords)
            # ONLY check title
            for article_data in articles:
                title_lower = article_data.get("title", "").lower()

                # Skip if contains avoid keywords
                has_avoid_keyword = any(
                    keyword in title_lower
                    for keyword in avoid_keywords
                )
                if has_avoid_keyword:
                    continue

                if any(version_kw in title_lower
                       for version_kw in version_keywords_lower):
                    return NewsArticle.from_api_response(article_data)

            # If no match found, return None (don't fall back to latest)
            print(f"Warning: No news article found for versions {version_keywords}")
            return None

        except (requests.RequestException, KeyError, IndexError) as e:
            print(f"Error fetching news from Ennead API: {e}")
            return None
