from setuptools import find_packages
from setuptools import setup


setup(
    name='abita.policy',
    version='0.7.4',
    description="Turns Plone Site into Abita Site.",
    long_description=open("README.rst").read(),
    classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 4.2",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7"],
    keywords='',
    author='ABITA',
    author_email='taito.horiuchi@abita.fi',
    url='http://abita.fi/',
    license='Non-free',
    packages=find_packages('src', exclude=['ez_setup']),
    package_dir={'': 'src'},
    namespace_packages=['abita'],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        'Products.LinguaPlone',
        'abita.development',
        'abita.locales',
        'abita.theme',
        'hexagonit.testing',
        'setuptools'],
    entry_points="""
    # -*- Entry points: -*-

    [z3c.autoinclude.plugin]
    target = plone
    """)
