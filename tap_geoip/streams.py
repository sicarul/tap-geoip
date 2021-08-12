"""Stream type classes for tap-geoip."""

import requests, zipfile, csv
from io import BytesIO, TextIOWrapper
from pathlib import Path
from typing import Any, Dict, Optional, Union, List, Iterable

from singer_sdk import typing as th  # JSON Schema typing helpers

from tap_geoip.client import GeoIPStream

# TODO: Delete this is if not using json files for schema definition
SCHEMAS_DIR = Path(__file__).parent / Path("./schemas")
# TODO: - Override `UsersStream` and `GroupsStream` with your own stream definition.
#       - Copy-paste as many times as needed to create multiple stream types.

def convertInt(value):
    retValue = None
    try:
        retValue = int(value)
    except ValueError:
        pass
    return retValue


def convertFloat(value):
    retValue = None
    try:
        retValue = float(value)
    except ValueError:
        pass
    return retValue

class CityStream(GeoIPStream):
    name = "geoip_city"
    primary_keys = ["network"]
    replication_key = None
    

    def get_records(self, context: Optional[dict]) -> Iterable[dict]:

        r = requests.get(self.url_city, stream=True)
        if r.ok:
            z = zipfile.ZipFile(BytesIO(r.content))
            files = z.namelist()
            for f in files:
                folder = f.split('/')[0]
                datefilename = folder[-8:]
                date = f"{datefilename[:4]}-{datefilename[4:6]}-{datefilename[6:8]}"
                if f.endswith("City-Blocks-IPv4.csv"):
                    with z.open(f, 'r') as infile:
                        reader = csv.DictReader(TextIOWrapper(infile, 'utf-8'))

                        for row in reader:
                            row['protocol'] = 'IPv4'
                            row['date'] = date
                            yield self.post_process(row)
                if f.endswith("City-Blocks-IPv6.csv"):
                    with z.open(f, 'r') as infile:
                        reader = csv.DictReader(TextIOWrapper(infile, 'utf-8'))

                        for row in reader:
                            row['protocol'] = 'IPv6'
                            row['date'] = date
                            yield self.post_process(row)
            
        else:
            raise ConnectionError("HTTP Status not OK")

    
    def post_process(self, row: dict, context: Optional[dict] = None) -> dict:
        """Convert numbers"""
        row['geoname_id'] = convertInt(row['geoname_id'])
        row['registered_country_geoname_id'] = convertInt(row['registered_country_geoname_id'])
        row['represented_country_geoname_id'] = convertInt(row['represented_country_geoname_id'])
        row['is_anonymous_proxy'] = convertInt(row['is_anonymous_proxy'])
        row['is_satellite_provider'] = convertInt(row['is_satellite_provider'])
        row['latitude'] = convertFloat(row['latitude'])
        row['longitude'] = convertFloat(row['longitude'])
        row['accuracy_radius'] = convertInt(row['accuracy_radius'])
        return row


    schema = th.PropertiesList(
        th.Property("network", th.StringType),
        th.Property("date", th.DateTimeType),
        th.Property("protocol", th.StringType),
        th.Property("geoname_id", th.IntegerType),
        th.Property("registered_country_geoname_id", th.IntegerType),
        th.Property("represented_country_geoname_id", th.IntegerType),
        th.Property("is_anonymous_proxy", th.IntegerType),
        th.Property("is_satellite_provider", th.IntegerType),
        th.Property("postal_code", th.StringType),
        th.Property("latitude", th.NumberType),
        th.Property("longitude", th.NumberType),
        th.Property("accuracy_radius", th.IntegerType)
    ).to_dict()



class LocationsStream(GeoIPStream):
    name = "geoip_city_locations"
    primary_keys = ["geoname_id", "locale_code"]
    replication_key = None
    

    def get_records(self, context: Optional[dict]) -> Iterable[dict]:
        languages = self.config['languages'].split(',')
        r = requests.get(self.url_city, stream=True)
        if r.ok:
            z = zipfile.ZipFile(BytesIO(r.content))
            files = z.namelist()
            for f in files:
                folder = f.split('/')[0]
                datefilename = folder[-8:]
                date = f"{datefilename[:4]}-{datefilename[4:6]}-{datefilename[6:8]}"
                for l in languages:
                    if f.endswith(f"City-Locations-{l}.csv"):
                        with z.open(f, 'r') as infile:
                            reader = csv.DictReader(TextIOWrapper(infile, 'utf-8'))

                            for row in reader:
                                row['date'] = date
                                yield self.post_process(row)
        else:
            raise ConnectionError("HTTP Status not OK")

    
    def post_process(self, row: dict, context: Optional[dict] = None) -> dict:
        """Convert numbers"""
        row['geoname_id'] = convertInt(row['geoname_id'])
        row['is_in_european_union'] = convertInt(row['is_in_european_union'])
        return row


    schema = th.PropertiesList(
        th.Property("geoname_id", th.IntegerType),
        th.Property("date", th.DateTimeType),
        th.Property("locale_code", th.StringType),
        th.Property("continent_code", th.StringType),
        th.Property("continent_name", th.StringType),
        th.Property("country_iso_code", th.StringType),
        th.Property("country_name", th.StringType),
        th.Property("subdivision_1_iso_code", th.StringType),
        th.Property("subdivision_1_name", th.StringType),
        th.Property("subdivision_2_iso_code", th.StringType),
        th.Property("subdivision_2_name", th.StringType),
        th.Property("city_name", th.StringType),
        th.Property("metro_code", th.StringType),
        th.Property("time_zone", th.StringType),
        th.Property("is_in_european_union", th.IntegerType)
    ).to_dict()
