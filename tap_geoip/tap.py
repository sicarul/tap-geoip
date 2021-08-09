"""GeoIP tap class."""

from typing import List

from singer_sdk import Tap, Stream
from singer_sdk import typing as th  # JSON schema typing helpers

# TODO: Import your custom stream types here:
from tap_geoip.streams import (
    GeoIPStream,
    CityStream,
    LocationsStream,
)

STREAM_TYPES = [
    CityStream,
    LocationsStream,
]


class TapGeoIP(Tap):
    """GeoIP tap class."""
    name = "tap-geoip"

    # TODO: Update this section with the actual config values you expect:
    config_jsonschema = th.PropertiesList(
        th.Property("license_key", th.StringType, required=True),
        th.Property("city_url", th.StringType, default="https://download.maxmind.com/app/geoip_download?edition_id=GeoLite2-City-CSV&suffix=zip&license_key="),
        th.Property("languages", th.StringType, default="en"),
    ).to_dict()

    def discover_streams(self) -> List[Stream]:
        """Return a list of discovered streams."""
        return [stream_class(tap=self) for stream_class in STREAM_TYPES]
