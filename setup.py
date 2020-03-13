from setuptools import setup, find_packages


def get_requirements():
    with open(file="requirements.txt", mode="r") as file:
        return [line.strip() for line in file.readlines()]


setup(
    name="hackernews",
    version="0.0.1",
    packages=find_packages(exclude=["tests"]),
    install_requires=get_requirements(),
    entry_points={"console_scripts": ["hackernews=hackernews.commands:main"]},
)