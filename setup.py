from setuptools import setup, find_packages

setup(
    name='sms-nas',
    version='1.0',
    author='mikolaj44',
    description="This package turns the TL-MR150 router's draft SMS inbox (or maybe other MR routers, untested) into a very simple, extremely small and really slow file storage system. Just for fun.",
    packages=find_packages(),
    entry_points={
        "console_scripts": ["nasms=nasms.managers.console_handler:main"],
    },
)
