from plone.browserlayer import utils

import logging


def remove_browser_layer(context, logger=None):
    """Show path bar"""
    if logger is None:
        logger = logging.getLogger(__name__)
    utils.unregister_layer('abita.policy')
