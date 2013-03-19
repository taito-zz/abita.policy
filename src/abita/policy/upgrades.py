from abita.utils.utils import reimport_profile
from plone.browserlayer import utils

import logging


PROFILE_ID = 'profile-abita.policy:default'


def remove_browser_layer(context, logger=None):
    """Show path bar"""
    if logger is None:
        logger = logging.getLogger(__name__)
    utils.unregister_layer('abita.policy')


def reimport_actions(context):
    """Reimport actions"""
    reimport_profile(context, PROFILE_ID, 'actions')
