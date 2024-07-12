import os
from logging import getLogger
from typing import Any, Dict

from src.ui.enums.interface_mode import mode_to_interface
from src.ui.interaction_chat import AInteractionChat
from src.utils import read_config

logger = getLogger(__name__)


def main(app_config: Dict[str, Any]):
    interface_mode = app_config['Application']['interface_mode']
    logger.info(f"Starting interface in {interface_mode} mode...")
    interface: AInteractionChat = mode_to_interface[interface_mode](config)
    interface.run()


if __name__ == "__main__":
    config: Dict[str, Any] = read_config(os.path.join(os.getcwd(), 'config.ini'))
    main(config)
