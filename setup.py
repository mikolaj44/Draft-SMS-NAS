from setuptools import setup, find_packages

setup(
    name='smsnas',
    author='mikolaj44',
    description="This package turns the TL-MR150 router's draft SMS inbox (or maybe other MR routers, untested) into a very simple, extremely small and really slow file storage system. Just for fun. Console command is 'smsnas'",
    packages=find_packages(),
    install_requires=[
        'tplinkrouterc6udraftsms @ git+ssh://git@github.com/mikolaj44/TP-Link-Archer-C6U-Draft-SMS.git',
        'tqdm',
        'stdiomask',
        "python-magic ; sys_platform == 'linux'",
        "python-magic ; sys_platform == 'darwin'",
        "python-magic-bin ; sys_platform == 'win32'",
    ],
    package_data={
        'smsnas': ['user_config.json', 'program_config.json'],
    },
    entry_points={
        "console_scripts": ["smsnas=smsnas.managers.console_handler:main"],
    },
)