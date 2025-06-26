import logging
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_ATTRIBUTION, CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.util import slugify

from . import MLBBaseballDataUpdateCoordinator
from .const import (
    ATTRIBUTION,
    CONF_TIMEOUT,
    CONF_TEAM_ID,
    COORDINATOR,
    DEFAULT_ICON,
    DEFAULT_NAME,
    DEFAULT_TIMEOUT,
    DOMAIN,
)

_LOGGER = logging.getLogger(__name__)

# Remove async_setup_platform to enforce config entries only
# async_setup_platform deprecated for config entries integration


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities):
    """Set up the sensor platform from a config entry."""
    async_add_entities([MLBBaseballScoresSensor(hass, entry)], True)


class MLBBaseballScoresSensor(CoordinatorEntity):
    """Representation of a MLB Baseball Score sensor."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        super().__init__(hass.data[DOMAIN][entry.entry_id][COORDINATOR])
        self._config = entry
        self._name = entry.data.get(CONF_NAME, DEFAULT_NAME)
        self._icon = DEFAULT_ICON

        # Initialize state attributes to None
        self._state = "PRE"

        self._team_id = entry.data.get(CONF_TEAM_ID)
        self.coordinator = hass.data[DOMAIN][entry.entry_id][COORDINATOR]

    @property
    def unique_id(self) -> str:
        """Return a unique, Home Assistant friendly identifier for this entity."""
        return f"{slugify(self._name)}_{self._config.entry_id}"

    @property
    def name(self) -> str:
        """Return the name of the sensor."""
        return self._name

    @property
    def icon(self) -> str:
        """Return the icon to use in the frontend, if any."""
        return self._icon

    @property
    def state(self):
        """Return the state of the sensor."""
        if self.coordinator.data is None:
            return None
        return self.coordinator.data.get("state")

    @property
    def extra_state_attributes(self) -> dict:
        """Return the state attributes."""
        attrs = {}

        if self.coordinator.data is None:
            return attrs

        data = self.coordinator.data

        attrs[ATTR_ATTRIBUTION] = ATTRIBUTION
        attrs["date"] = data.get("date")
        attrs["first_pitch_in"] = data.get("first_pitch_in")
        attrs["inning"] = data.get("inning")
        attrs["clock"] = data.get("clock")
        attrs["venue"] = data.get("venue")
        attrs["location"] = data.get("location")
        attrs["tv_network"] = data.get("tv_network")
        attrs["odds"] = data.get("odds")
        attrs["overunder"] = data.get("overunder")
        attrs["spread"] = data.get("spread")
        attrs["indoor"] = data.get("indoor")
        attrs["weather"] = data.get("weather")
        attrs["temperature"] = data.get("temperature")
        attrs["attendance"] = data.get("attendance")
        attrs["notes"] = data.get("notes")
        attrs["outs"] = data.get("outs")
        attrs["balls"] = data.get("balls")
        attrs["strikes"] = data.get("strikes")
        attrs["last_play"] = data.get("last_play")
        attrs["alt_last_play"] = data.get("alt_last_play")
        attrs["onFirst"] = data.get("onFirst")
        attrs["onSecond"] = data.get("onSecond")
        attrs["onThird"] = data.get("onThird")
        attrs["team_abbr"] = data.get("team_abbr")
        attrs["team_id"] = data.get("team_id")
        attrs["team_name"] = data.get("team_name")
        attrs["team_record"] = data.get("team_record")
        attrs["team_homeaway"] = data.get("team_homeaway")
        attrs["team_logo"] = data.get("team_logo")
        attrs["team_colors"] = data.get("team_colors")
        attrs["team_colors_rgb"] = self.team_colors(data.get("team_colors"))
        attrs["team_score"] = data.get("team_score")
        attrs["team_hits"] = data.get("team_hits")
        attrs["team_errors"] = data.get("team_errors")
        attrs["team_win_probability"] = data.get("team_win_probability")
        attrs["opponent_abbr"] = data.get("opponent_abbr")
        attrs["opponent_id"] = data.get("opponent_id")
        attrs["opponent_name"] = data.get("opponent_name")
        attrs["opponent_record"] = data.get("opponent_record")
        attrs["opponent_homeaway"] = data.get("opponent_homeaway")
        attrs["opponent_logo"] = data.get("opponent_logo")
        attrs["opponent_colors"] = data.get("opponent_colors")
        attrs["opponent_colors_rgb"] = self.team_colors(data.get("opponent_colors"))
        attrs["opponent_score"] = data.get("opponent_score")
        attrs["opponent_hits"] = data.get("opponent_hits")
        attrs["opponent_errors"] = data.get("opponent_errors")
        attrs["opponent_win_probability"] = data.get("opponent_win_probability")
        attrs["last_update"] = data.get("last_update")

        return attrs

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success

    @staticmethod
    def team_colors(colors) -> list | None:
        """Convert team colors hex list to RGB list."""
        if not colors or len(colors) < 2:
            return None
        try:
            return [MLBBaseballScoresSensor.hex_to_rgb(c) for c in colors]
        except Exception as e:
            _LOGGER.warning("Failed to parse team colors: %s", e)
            return None

    @staticmethod
    def hex_to_rgb(hexa: str) -> tuple[int, int, int]:
        """Convert hex color string to RGB tuple."""
        hexa = hexa.lstrip("#")
        return tuple(int(hexa[i : i + 2], 16) for i in (0, 2, 4))
