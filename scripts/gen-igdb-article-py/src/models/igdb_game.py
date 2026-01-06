from dataclasses import dataclass
from typing import List


@dataclass
class IGDBGame:
    """Simple model for IGDB game verification"""

    id: str
    name: str
    alternative_names: List[str] = None

    @classmethod
    def from_api_response(cls, data: dict):
        """Create IGDBGame from API response"""
        # Extract alternative names if available
        alternative_names = []
        if "alternative_names" in data:
            for alt_name_data in data["alternative_names"]:
                if isinstance(alt_name_data, dict) and "name" in alt_name_data:
                    alternative_names.append(alt_name_data["name"])

        return cls(
            id=str(data["id"]),
            name=data.get("name", ""),
            alternative_names=alternative_names if alternative_names else None,
        )
