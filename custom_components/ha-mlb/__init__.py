"""MLB Team Status"""
import asyncio
import logging
from datetime import timedelta
import aiohttp
import arrow

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant

from .const import (
    API_ENDPOINT,
    CONF_TIMEOUT,
    CONF_TEAM_ID,
    COORDINATOR,
    DEFAULT_TIMEOUT,
    DOMAIN,
    PLATFORMS,
    USER_AGENT,
    VERSION,
)

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up MLB integration."""
    _LOGGER.info(
        "MLB integration version %s is starting...",
        VERSION,
    )
    hass.data.setdefault(DOMAIN, {})

    # Setup the data coordinator
    coordinator = MLBDataUpdateCoordinator(
        hass, entry.data, entry.data.get(CONF_TIMEOUT)
    )

    # Fetch initial data so we have data when entities subscribe
    await coordinator.async_refresh()

    hass.data[DOMAIN][entry.entry_id] = {
        COORDINATOR: coordinator,
    }

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, config_entry: ConfigEntry) -> bool:
    """Unload the MLB integration."""
    _LOGGER.debug("Unloading MLB integration...")
    unload_ok = await asyncio.gather(
        *[hass.config_entries.async_forward_entry_unload(config_entry, platform) for platform in PLATFORMS]
    )

    if all(unload_ok):
        _LOGGER.debug("MLB integration successfully unloaded.")
        hass.data[DOMAIN].pop(config_entry.entry_id)

    return all(unload_ok)


class MLBDataUpdateCoordinator(DataUpdateCoordinator):
    """Class to manage fetching MLB game data."""

    def __init__(self, hass, config, timeout: int):
        """Initialize the coordinator."""
        self.interval = timedelta(minutes=10)
        self.name = config[CONF_NAME]
        self.timeout = timeout
        self.config = config
        self.hass = hass

        _LOGGER.debug("MLB data will be updated every %s", self.interval)

        super().__init__(hass, _LOGGER, name=self.name, update_interval=self.interval)

    async def _async_update_data(self):
        """Fetch MLB game data."""
        async with aiohttp.ClientSession() as session:
            try:
                data = await self._fetch_mlb_data(session)
                return data
            except Exception as error:
                raise UpdateFailed(error) from error

    async def _fetch_mlb_data(self, session):
        """Retrieve MLB game data from the API."""
        headers = {"User-Agent": USER_AGENT, "Accept": "application/json"}
        team_id = self.config[CONF_TEAM_ID]
        url = f"{API_ENDPOINT}?team_id={team_id}"

        async with session.get(url, headers=headers, timeout=self.timeout) as response:
            if response.status == 200:
                data = await response.json()
                return data
            else:
                raise UpdateFailed(f"Error fetching MLB data: HTTP {response.status}")


async def async_clear_states(config) -> dict:
    """Clear all MLB game state attributes."""
    values = {
        "date": None,
        "kickoff_in": None,
        "quarter": None,
        "clock": None,
        "venue": None,
        "location": None,
        "tv_network": None,
        "odds": None,
        "overunder": None,
        "last_play": None,
        "down_distance_text": None,
        "possession": None,
        "team_id": None,
        "team_record": None,
        "team_homeaway": None,
        "team_colors": None,
        "team_score": None,
        "team_rank": None, 
        "team_win_probability": None,
        "team_timeouts": None,
        "opponent_abbr": None,
        "opponent_id": None,
        "opponent_name": None,
        "opponent_record": None,
        "opponent_homeaway": None,
        "opponent_logo": None,
        "opponent_colors": None,
        "opponent_score": None,
        "opponent_rank": None,
        "opponent_win_probability": None,
        "opponent_timeouts": None,
        "last_update": None,
        "private_fast_refresh": False,
    }
    return values
