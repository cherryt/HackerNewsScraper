import json

from click.testing import CliRunner

from hackernews.services import HackerNewsScraperService
from hackernews.commands import main


def test_main_using_valid_inputs(mocker):
    # given
    posts = 2
    hackernews_uri = "https://news.ycombinator.com/"
    mocker.patch.object(HackerNewsScraperService, "get_top_posts")

    # when
    runner = CliRunner()
    result = runner.invoke(cli=main, args=["--posts", posts])

    # then
    HackerNewsScraperService.get_top_posts.assert_called_once_with(
        uri=hackernews_uri, number_of_posts=posts
    )

def test_main_with_100_posts():
    # given
    posts = 100

    # when
    runner = CliRunner()
    result = runner.invoke(cli=main, args=["--posts", posts])
    
    # then
    assert len(json.loads(result.output)) == posts

def test_main_with_negative_post_num():
    # given
    posts = -1

    # when
    runner = CliRunner()
    result = runner.invoke(cli=main, args=["--posts", posts])

    # then
    assert f"{posts} is not valid. --posts must a positive integer <= 100" in result.output

def test_main_with_post_num_greater_than_100():
    # given
    posts = 200

    # when
    runner = CliRunner()
    result = runner.invoke(cli=main, args=["--posts", posts])

    # then
    assert f"{posts} is not valid. --posts must a positive integer <= 100" in result.output

def test_main_with_post_num_0():
    # given zero is not a positive integer
    posts = 0

    # when
    runner = CliRunner()
    result = runner.invoke(cli=main, args=["--posts", posts])

    # then
    assert f"{posts} is not valid. --posts must a positive integer <= 100" in result.output
   