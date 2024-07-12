import logging

import coloredlogs

coloredlogs.install(level='INFO', fmt='%(asctime)s %(name)s %(levelname)s %(message)s')


def get_logger(name):
    return logging.getLogger(name)
