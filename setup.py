from setuptools import find_packages
from setuptools import setup


setup(
    name='abita.policy',
    version='0.1',
    description="Turns Plone Site into Abita Site.",
    long_description=open("README.rst").read(),
    # Get more strings from
    # http://pypi.python.org/pypi?:action=list_classifiers
    classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 4.1",
        "Framework :: Plone :: 4.2",
        "Framework :: Plone :: 4.3",
        "Programming Language :: Python",
    ],
    keywords='',
    author='ABITA',
    author_email='taito.horiuchi@abita.fi',
    url='http://abita.fi/',
    license='Non-free',
    packages=find_packages(exclude=['ez_setup']),
    namespace_packages=['abita'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        # 'abita.theme',
        'Products.PloneFormGen',
        'hexagonit.testing',
        'plone.browserlayer',
        'setuptools',
        'z3c.autoinclude',
        'z3c.jbot',
        'zope.i18nmessageid',
    ],
    entry_points="""
    # -*- Entry points: -*-

    [z3c.autoinclude.plugin]
    target = plone
    """,
)
