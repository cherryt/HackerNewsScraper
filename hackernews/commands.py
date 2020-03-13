import json

import click

from hackernews.services import HackerNewsScraperService


@click.command(help="Retrieve posts from HackerNews")
@click.option(
    "-p",
    "--posts",
    default=1,
    type=click.INT,
    show_default=True,
    help="Number of posts to retrieve",
)
def main(posts):
    hackernews_uri = "https://news.ycombinator.com/"
    results = HackerNewsScraperService.get_top_posts(
        uri=hackernews_uri, number_of_posts=posts
    )
    formatted_results = json.dumps(results, indent=4) if type(results) != str else results
    print(formatted_results)
