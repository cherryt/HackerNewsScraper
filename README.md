# HackerNewsScraper

A Python command line application that scraps [Hacker News](https://news.ycombinator.com/) and returns the top posts.

## Installation

Firstly, make sure [Python](https://www.python.org/downloads/) is installed.

Then install the package:

```bash
pip install -e .
```

## Run Tests

To install requirements and run tests:

```bash
pip install -r test_requirements
pytest tests
```

## Usage

Command to run in the CLI (where n is the number of posts and is a positive integer <= 100):

```bash
$ hackernews --posts n
```

For CLI help:

```bash
$ hackernews --help
```

## Libraries Used

BeautifulSoup4: Used to scrape HackerNews  
Click: A package for creating command line interfaces with minimal code  
Urllib3: An Http client to retrieve html to be scraped  
Validators: Used to validate the URI  

Pytest: A testing framework for testing applications and libraries  
Pytest-Mock: Mocking library for testing, can mock objects to increase ease of testing  