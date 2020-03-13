import json

from bs4 import BeautifulSoup

from hackernews.services import HackerNewsScraperService


def test_get_top_posts_when_valid_params_return_valid_dicts():
    # given
    hackernews_uri = "https://news.ycombinator.com/"
    posts = 5

    # when
    result = HackerNewsScraperService.get_top_posts(hackernews_uri, posts)

    # then
    assert result
    assert result[0]["title"]
    assert result[0]["uri"]
    assert result[0]["author"]
    assert result[0]["points"]
    assert result[0]["comments"]
    assert result[0]["rank"]

def test_get_top_posts_when_invalid_uri():
    # given
    hackernews_uri = "https://news.ycombi[]nator.com/"
    posts = 5

    # when 
    result = HackerNewsScraperService.get_top_posts(hackernews_uri, posts)

    # then
    assert result == f"{hackernews_uri} is not a valid uri. "

def test_scrape_when_hackernews_ui_changes_return_error():
    # given
    changed_elements_soup = BeautifulSoup("<div></div>", "html.parser")
    posts = 5

    # when
    result = HackerNewsScraperService.scrape(changed_elements_soup, posts)

    # then
    assert result == "Error: hackernews UI has changed, please update scraper."

def test_scrape_when_points_are_negative_return_0_points():
    # given
    soup = _create_test_soup(1, "test", -2, "author", 1)
    posts = 1

    # when
    result = HackerNewsScraperService.scrape(soup, posts)

    # then
    assert 0 <= result[0]["points"]

def _create_test_soup(rank, title, points, author, comments):
    html = f'''<table class="itemlist">
            <tr class="athing">
                <td class="title"><span class="rank">{rank}.</span></td>
                <td class="title">
                    <a href="test.link" class="storylink">{title}</a> (
                </td>
            </tr>
            <tr>
                <td class="subtext">
                    <span class="score">{points} points</span>
                    <a class="hnuser">{author}</a> 
                    <a>{comments}&nbsp;comments</a>              
                </td>
            </tr>
        </table>'''
    return BeautifulSoup(html, "html.parser")

def test_scrape_when_rank_are_negative_return_0_comments():
    # given
    soup = _create_test_soup(-1, "test", 2, "author", 1)
    posts = 1

    # when
    result = HackerNewsScraperService.scrape(soup, posts)

    # then
    assert 0 <= result[0]["rank"]

def test_scrape_when_comments_is_negative_return_0_rank():
    # given
    soup = _create_test_soup(1, "test", 2, "author", -3)
    posts = 1

    # when
    result = HackerNewsScraperService.scrape(soup, posts)

    # then
    assert 0 <= result[0]["comments"]

def test_scrape_when_title_is_longer_than_256_shorten_title():
    # given
    title = "t"*300
    soup = _create_test_soup(1,title, 2, "author", -3)
    posts = 1

    # when
    result = HackerNewsScraperService.scrape(soup, posts)

    # then
    assert len(result[0]["title"]) == 256

def test_scrape_when_author_is_256_characters_author_is_unchanged():
    # given
    author = "t"*256
    soup = _create_test_soup(1, "title", 2, author, -3)
    posts = 1

    # when
    result = HackerNewsScraperService.scrape(soup, posts)

    # then
    assert len(result[0]["author"]) == 256

def test_scrape_when_author_less_than_256_characters_author_is_unchanged():
    # given
    author = "author"
    soup = _create_test_soup(1, "title", 2, author, -3)
    posts = 1

    # when
    result = HackerNewsScraperService.scrape(soup, posts)

    # then
    assert len(result[0]["author"]) == len(author)