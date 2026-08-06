# API
API_ENDPOINT = "https://site.api.espn.com/apis/site/v2/sports/baseball/mlb/scoreboard"
USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_6) "
    "AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Safari/605.1.15"
)

# Config keys
CONF_TIMEOUT = "timeout"
CONF_TEAM_ID = "team_id"

# Defaults
DEFAULT_ICON = "mdi:baseball"
DEFAULT_NAME = "MLB"
DEFAULT_TIMEOUT = 240  # seconds

# Miscellaneous constants
DOMAIN = "ha-mlb"
PLATFORM = "sensor"
PLATFORMS = [PLATFORM]
COORDINATOR = "coordinator"
ATTRIBUTION = "Data provided by ESPN"
VERSION = "0.7.1"
ISSUE_URL = "https://github.com/daviswieck/ha-mlb"
TEAM_ID = ""  # placeholder or default, probably unused
