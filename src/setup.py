from setuptools import setup

setup(
    name="nibe2influx",
    packages=["nibe2influx"],
    version="0.1",

    # Dependencies
    install_requires=['requests_oauthlib>=0.8.0', 'influxdb>=4.1'],

    package_data={
        # Additional files to include
        '': ['sensors.json', 'config.json.template'],
    },

    entry_points = {
        "console_scripts": ["nibe2influx = nibe2influx.nibe2influx:main"]
    },

    author="Martin Sträng",
    author_email="martin@tilljorden.com",
    description="Read parameters from Nibe Uplink and store in InfluxDB.",
    license="MIT",
    keywords="",
    url="",
)