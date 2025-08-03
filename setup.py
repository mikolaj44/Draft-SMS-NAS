from setuptools import setup, find_packages

setup(
    name='sms-nas',
    version='1.0',
    author='mikolaj44',
    description="This package turns the TL-MR150 router's draft SMS inbox (or maybe other MR routers, untested) into a very simple, extremely small and really slow file storage system. Just for fun.",
    packages=find_packages(),
    # install_requires=[
    #     'tplinkrouterc6udraftsms @ git+ssh://git@github.com/mikolaj44/TP-Link-Archer-C6U-Draft-SMS.git'
    # ],
    entry_points={
        "console_scripts": ["smsnas=nasms.managers.console_handler:main"],
    },
)
