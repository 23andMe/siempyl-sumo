"""Setup config used for PIP"""
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='siempyl_sumo',
    version='1.0.0',
    author='23andMe',
    author_email='security@23andme.com',
    description='Python library for SumoLogic Cloud SIEM Enterprise',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/23andme/siempyl-sumo',
    project_urls = {
        "Bug Tracker": "https://github.com/23andme/siempyl-sumo/issues"
    },
    license='apache',
    packages=['siempyl_sumo'],
    install_requires=['requests'],
)
