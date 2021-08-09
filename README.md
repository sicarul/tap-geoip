# tap-geoip

`tap-geoip` is a Singer tap for [Maxmind's GeoIP2 Lite](https://dev.maxmind.com/geoip/geolite2-free-geolocation-data?lang=en) - Theoretically it should also work with the commercial version because they share the same data format, but i didn't test it. To locally test this tap, you can download the database once from maxmind, and use a local HTTP server, in this case, set the license key to "none".

Built with the Meltano [SDK](https://gitlab.com/meltano/sdk) for Singer Taps.

## Configuration

### Accepted Config Options

A full list of supported settings and capabilities for this
tap is available by running:

```bash
tap-geoip --about
```

You should specifiy the following configuration variables to properly import this database:

* url_city: URL to obtain the cities database, it can be left as the default if you are using the Lite database.
* license_key: Your license key to access the database
* languages: Which languages to load into the database, from the ones provided in the zip file

## Usage

You can easily run `tap-geoip` by itself or in a pipeline using [Meltano](www.meltano.com).

### Executing the Tap Directly

```bash
tap-geoip --version
tap-geoip --help
tap-geoip --config CONFIG --discover > ./catalog.json
```

## Developer Resources

### Initialize your Development Environment

```bash
pipx install poetry
poetry install
```


### Using with [Meltano](https://www.meltano.com)

_**Note:** This tap will work in any Singer environment and does not require Meltano._

Install Meltano (if you haven't already) and any needed plugins:

```bash
# Install meltano
pipx install meltano
# Initialize meltano within this directory
cd tap-geoip
meltano install
```

Now you can test and orchestrate using Meltano:

```bash
# Run a test `elt` pipeline:
meltano elt tap-geoip target-jsonl
```

### SDK Dev Guide

See the [dev guide](https://sdk.meltano.com/en/latest/dev_guide.html) for more instructions on how to use the SDK to 
develop your own taps and targets.
