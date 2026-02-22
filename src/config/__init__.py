#!/usr/bin/env python3
"""
Configuration package for RivalSearchMCP.
"""

from .archives import ARCHIVE_FALLBACKS, get_archive_fallbacks
from .environment import get_environment_config
from .paywall import PAYWALL_INDICATORS, get_paywall_indicators
from .user_agents import DEFAULT_UA_LIST, get_user_agents

__all__ = [
    # User agents
    "get_user_agents",
    "DEFAULT_UA_LIST",
    # Paywall detection
    "get_paywall_indicators",
    "PAYWALL_INDICATORS",
    # Archive fallbacks
    "get_archive_fallbacks",
    "ARCHIVE_FALLBACKS",
    # Environment
    "get_environment_config",
]
