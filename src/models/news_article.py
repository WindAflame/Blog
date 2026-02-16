from dataclasses import dataclass
from typing import List, Optional


@dataclass
class NewsArticle:
    """Model for news article from api.ennead.cc"""

    id: str
    title: str
    description: str
    url: str
    banner: List[str]
    created_at: int
    article_type: str

    @classmethod
    def from_api_response(cls, data: dict):
        """Create NewsArticle from API response"""
        return cls(
            id=data["id"],
            title=data["title"],
            description=data["description"],
            url=data["url"],
            banner=data.get("banner", []),
            created_at=data["createdAt"],
            article_type=data.get("type", "notice"),
        )

    @property
    def banner_url(self) -> Optional[str]:
        """Get the first banner URL if available"""
        return self.banner[0] if self.banner else None

    @property
    def banner_webp_url(self) -> Optional[str]:
        """Get the banner URL with webp format if available"""
        if not self.banner_url:
            return None

        # If the URL already has webp processing, return as is
        if "x-oss-process=image/format,webp" in self.banner_url:
            return self.banner_url

        # Add webp processing if not present
        separator = "?" if "?" not in self.banner_url else "&"
        return f"{self.banner_url}{separator}x-oss-process=image/format,webp/quality,Q_90"
