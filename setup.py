try:
    from setuptools import setup, find_packages
except ImportError:
    from ez_setup import use_setuptools
    use_setuptools()
    from setuptools import setup, find_packages

setup(
    name='lazydm',
    version='0.1',
    description='',
    author='',
    author_email='',
    url='',
    install_requires=[
        "Pylons>=1.0",
        "SQLAlchemy>=0.6",
        "Jinja2",
        "MySQL-python",
        "pytz",
        "pygments",
        "repoze.what-pylons",
        "repoze.what-quickstart"
    ],
    setup_requires=["PasteScript>=1.6.3"],
    packages=find_packages(exclude=['ez_setup']),
    include_package_data=True,
    test_suite='nose.collector',
    package_data={'lazydm': ['i18n/*/LC_MESSAGES/*.mo']},
    #message_extractors={'lazydm': [
    #        ('**.py', 'python', None),
    #        ('public/**', 'ignore', None)]},
    zip_safe=False,
    paster_plugins=['PasteScript', 'Pylons'],
    entry_points="""
    [paste.app_factory]
    main = lazydm.config.middleware:make_app

    [paste.app_install]
    main = pylons.util:PylonsInstaller
    """,
)
