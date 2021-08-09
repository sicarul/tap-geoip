"""Custom client handling, including GeoIPStream base class."""

from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable

from singer_sdk.streams import Stream


class GeoIPStream(Stream):
    """Stream class for GeoIP streams."""

    @property
    def url_city(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        city_url = self.config["city_url"]
        license_key = self.config["license_key"]
        if license_key == 'none':
            license_key = ''
        return f"{city_url}{license_key}"

