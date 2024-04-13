"""Adds config flow for MLB."""
from __future__ import annotations

import logging
from typing import Any, Dict, Optional

import voluptuous as vol
from homeassistant import config_entries
from homeassistant.const import CONF_NAME
from homeassistant.core import HomeAssistant, callback
from homeassistant.data_entry_flow import FlowResult

from .const import (
    API_ENDPOINT,
    CONF_TIMEOUT,
    CONF_TEAM_ID,
    DEFAULT_NAME,
    DEFAULT_TIMEOUT,
    DOMAIN,
    USER_AGENT,
)

# List of MLB team abbreviations
MLB_TEAMS = [
    "HOU", "TEX", "NYY", "BOS", "LAD", "SF", "CHC", "STL", "ATL", "NYM",
    "SEA", "OAK", "CLE", "CWS", "MIL", "MIN", "TB", "TOR", "PHI", "WSH",
    "ARI", "SD", "COL", "MIA", "CIN", "PIT", "DET", "KC", "BAL", "LAA"
]

_LOGGER = logging.getLogger(__name__)

def _get_schema(
    hass: HomeAssistant,
    user_input: Optional[Dict[str, Any]],
    default_dict: Dict[str, Any]
) -> vol.Schema:
    """Get schema for configuration."""
    if user_input is None:
        user_input = {}

    def _get_default(key: str, fallback_default: Any = None) -> None:
        """Get default value for key."""
        return user_input.get(key, default_dict.get(key, fallback_default))

    return vol.Schema(
        {
            vol.Required(CONF_TEAM_ID, default=_get_default(CONF_TEAM_ID, MLB_TEAMS[0])): vol.In(MLB_TEAMS),
            vol.Optional(CONF_NAME, default=_get_default(CONF_NAME, DEFAULT_NAME)): str,
            vol.Optional(CONF_TIMEOUT, default=_get_default(CONF_TIMEOUT, DEFAULT_TIMEOUT)): int,
        }
    )

@config_entries.HANDLERS.register(DOMAIN)
class MLBScoresFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for MLB."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self):
        """Initialize the MLB config flow."""
        self._data = {}
        self._errors = {}

    async def async_step_user(self, user_input={}):
        """Handle a flow initialized by the user."""
        self._errors = {}

        if user_input is not None:
            self._data.update(user_input)
            return self.async_create_entry(title=self._data[CONF_NAME], data=self._data)
        return await self._show_config_form(user_input)

    async def _show_config_form(self, user_input):
        """Show the configuration form to edit location data."""
        defaults = {
            CONF_NAME: DEFAULT_NAME,
            CONF_TIMEOUT: DEFAULT_TIMEOUT,
            CONF_TEAM_ID: MLB_TEAMS[0],
        }

        return self.async_show_form(
            step_id="user",
            data_schema=_get_schema(self.hass, user_input, defaults),
            errors=self._errors,
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get options flow."""
        return MLBScoresOptionsFlow(config_entry)


class MLBScoresOptionsFlow(config_entries.OptionsFlow):
    """Options flow for MLB."""

    def __init__(self, config_entry):
        """Initialize MLB options flow."""
        self.config_entry = config_entry
        self._errors = {}

    async def async_step_init(self, user_input=None):
        """Handle a flow initialized by the user."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)
        return await self._show_options_form(user_input)

    async def _show_options_form(self, user_input):
        """Show the options form."""
        return self.async_show_form(
            step_id="init",
            data_schema=_get_schema(self.hass, user_input, self.config_entry.data),
            errors=self._errors,
        )
