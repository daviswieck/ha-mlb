import logging
from homeassistant.components.sensor import PLATFORM_SCHEMA
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

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_TEAM_ID): cv.string,
        vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
        vol.Optional(CONF_TIMEOUT, default=DEFAULT_TIMEOUT): int,
    }
)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Configuration from yaml"""
    if DOMAIN not in hass.data.keys():
        hass.data.setdefault(DOMAIN, {})
        config.entry_id = slugify(f"{config.get(CONF_TEAM_ID)}")
        config.data = config
    else:
        config.entry_id = slugify(f"{config.get(CONF_TEAM_ID)}")
        config.data = config

    # Setup the data coordinator
    coordinator = MLBBaseballDataUpdateCoordinator(
        hass,
        config,
        config[CONF_TIMEOUT],
    )

    # Fetch initial data so we have data when entities subscribe
    await coordinator.async_refresh()

    hass.data[DOMAIN][config.entry_id] = {
        COORDINATOR: coordinator,
    }
    async_add_entities([MLBBaseballScoresSensor(hass, config)], True)


async def async_setup_entry(hass, entry, async_add_entities):
    """Setup the sensor platform."""
    async_add_entities([MLBBaseballScoresSensor(hass, entry)], True)


class MLBBaseballScoresSensor(CoordinatorEntity):
    """Representation of a Sensor."""

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        super().__init__(hass.data[DOMAIN][entry.entry_id][COORDINATOR])
        self._config = entry
        self._name = entry.data[CONF_NAME]
        self._icon = DEFAULT_ICON

    @property
    def unique_id(self):
        """
        Return a unique, Home Assistant friendly identifier for this entity.
        """
        return f"{slugify(self._name)}_{self._config.entry_id}"

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def icon(self):
        """Return the icon to use in the frontend, if any."""
        return self._icon

    @property
    def state(self):
        """Return the state of the sensor."""
        if self.coordinator.data is None:
            return None
        elif "state" in self.coordinator.data.keys():
            return self.coordinator.data["state"]
        else:
            return None

    @property
    def extra_state_attributes(self):
        """Return the state message."""
        attrs = {}

        if self.coordinator.data is None:
            return attrs

        attrs[ATTR_ATTRIBUTION] = ATTRIBUTION
        # Map MLB Baseball data attributes here
        attrs["date"] = self.coordinator.data["date"]
        attrs["kickoff_in"] = self.coordinator.data["kickoff_in"]
        attrs["quarter"] = self.coordinator.data["quarter"]
        attrs["clock"] = self.coordinator.data["clock"]
        attrs["venue"] = self.coordinator.data["venue"]
        attrs["location"] = self.coordinator.data["location"]
        attrs["tv_network"] = self.coordinator.data["tv_network"]
        attrs["odds"] = self.coordinator.data["odds"]
        attrs["overunder"] = self.coordinator.data["overunder"]
        attrs["possession"] = self.coordinator.data["possession"]
        attrs["last_play"] = self.coordinator.data["last_play"]
        attrs["down_distance_text"] = self.coordinator.data["down_distance_text"]
        attrs["team_abbr"] = self.coordinator.data["team_abbr"]
        attrs["team_id"] = self.coordinator.data["team_id"]
        attrs["team_name"] = self.coordinator.data["team_name"]
        attrs["team_record"] = self.coordinator.data["team_record"]
        attrs["team_homeaway"] = self.coordinator.data["team_homeaway"]
        attrs["team_logo"] = self.coordinator.data["team_logo"]
        attrs["team_colors"] = self.coordinator.data["team_colors"]
        attrs["team_colors_rgb"] = self.team_colors(self.coordinator.data["team_colors"])
        attrs["team_score"] = self.coordinator.data["team_score"]
        attrs["team_rank"] = self.coordinator.data["team_rank"]
        attrs["team_win_probability"] = self.coordinator.data["team_win_probability"]
        attrs["team_timeouts"] = self.coordinator.data["team_timeouts"]
        attrs["opponent_abbr"] = self.coordinator.data["opponent_abbr"]
        attrs["opponent_id"] = self.coordinator.data["opponent_id"]
        attrs["opponent_name"] = self.coordinator.data["opponent_name"]
        attrs["opponent_record"] = self.coordinator.data["opponent_record"]
        attrs["opponent_homeaway"] = self.coordinator.data["opponent_homeaway"]
        attrs["opponent_logo"] = self.coordinator.data["opponent_logo"]
        attrs["opponent_colors"] = self.coordinator.data["opponent_colors"]
        attrs["opponent_colors_rgb"] = self.team_colors(
            self.coordinator.data["opponent_colors"]
        )
        attrs["opponent_score"] = self.coordinator.data["opponent_score"]
        attrs["opponent_rank"] = self.coordinator.data["opponent_rank"]
        attrs["opponent_win_probability"] = self.coordinator.data[
            "opponent_win_probability"
        ]
        attrs["opponent_timeouts"] = self.coordinator.data["opponent_timeouts"]
        attrs["last_update"] = self.coordinator.data["last_update"]

        return attrs

    @property
    def available(self) -> bool:
        """Return if entity is available."""
        return self.coordinator.last_update_success
