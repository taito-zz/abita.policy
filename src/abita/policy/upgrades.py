PROFILE_ID = 'profile-abita.policy:default'


def reimport_actions(setup):
    """Reimport actions"""
    setup.runImportStepFromProfile(PROFILE_ID, 'actions', run_dependencies=False, purge_old=False)


def reimport_propertiestool(setup):
    """Reimport propertiestool"""
    setup.runImportStepFromProfile('profile-Products.CMFPlone:plone', 'propertiestool', run_dependencies=False, purge_old=False)
    setup.runImportStepFromProfile(PROFILE_ID, 'propertiestool', run_dependencies=False, purge_old=False)


def reimport_languagetool(setup):
    """Reimport languagetool"""
    setup.runImportStepFromProfile(PROFILE_ID, 'languagetool', run_dependencies=False, purge_old=False)
