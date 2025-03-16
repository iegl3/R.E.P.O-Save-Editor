import logging

logger = logging.getLogger(__name__)

log_app = logging.getLogger('discord.app_commands')
log_discord = logging.getLogger('discord')
log = logging.getLogger('bot')

log.warning("This is a warning message")