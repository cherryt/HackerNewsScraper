import math 

from bs4 import BeautifulSoup
import urllib3
import validators


class HackerNewsScraperService:

    @classmethod
    def get_top_posts(cls, uri, number_of_posts):
        validation_messages = cls._get_validation_messages(uri, number_of_posts)
        if validation_messages:
            return validation_messages
        posts_per_page = 30
        if number_of_posts <= posts_per_page:
            return cls._get_posts(cls, uri, number_of_posts)
        pages = math.ceil(number_of_posts / posts_per_page)
        posts = []
        for page in range(pages):
            num_posts = posts_per_page
            if page + 1  == pages:
                num_posts = number_of_posts % posts_per_page
            uri_with_page = f'{uri}/news?p={page+1}'
            posts += cls._get_posts(cls, uri_with_page, num_posts)
        return posts

    @staticmethod
    def _get_validation_messages(uri, number_of_posts):
        msgs = ""
        #TODO: throw exceptions
        if not validators.url(uri):
            msgs += f"{uri} is not a valid uri. "
        if number_of_posts <= 0 or 100 < number_of_posts:
            msgs += f"{number_of_posts} is not valid. --posts must a positive integer <= 100"
        return msgs

    @staticmethod
    def _get_posts(cls, uri, number_of_posts):
        soup = cls._create_soup(uri)
        return cls.scrape(soup, number_of_posts)

    @classmethod
    def scrape(cls, soup, number_of_posts):
        table = soup.find_all("table", attrs={"class": "itemlist"}, limit=1)
        if not table:
            return "Error: hackernews UI has changed, please update scraper."
        table = table[0]
        rows_per_post = 3
        number_of_rows = int(number_of_posts) * rows_per_post
        rows = table.find_all("tr", limit=number_of_rows)
        posts = []

        for i in range(0, len(rows), rows_per_post):
            row_athing = rows[i]
            if len(row_athing) < 1:  # rows at end of table are empty
                continue
            post = {}
            td_tag = row_athing.find_all("td", attrs={"class": "title"})[1]
            a_tag = td_tag.find_all("a", attrs={"class": "storylink"}, limit=1)[0]
            post["title"] = a_tag.text[:256]
            post["rank"] = cls._get_rank(row_athing)
            post["uri"] = a_tag["href"]
            row_noclass = rows[i + 1]
            post["author"] = cls._get_author(row_noclass)
            post["points"] = cls._get_points(row_noclass)
            post["comments"] = cls._get_number_of_comments(row_noclass)
            posts.append(post)
        return posts

    @staticmethod
    def _create_soup(uri):
        http = urllib3.PoolManager()
        response = http.request("GET", uri)
        return BeautifulSoup(response.data, "html.parser")

    @staticmethod
    def _get_rank(row):
        rank_row = row.find_all("span", attrs={"class": "rank"}, limit=1)
        if rank_row:
            rank = int(rank_row[0].text[:-1])
            return max(rank, 0)

    @staticmethod
    def _get_author(row):
        user_tag = row.find_all("a", attrs={"class": "hnuser"}, limit=1)
        if not user_tag:
            return "Missing author name"
        return user_tag[0].text[:256]

    @staticmethod
    def _get_points(row):
        points =row.find_all("span", attrs={"class": "score"}, limit=1)
        number_of_points = int(points[0].text.split()[0]) if points else 0
        return max(number_of_points, 0)

    @staticmethod
    def _get_number_of_comments(row_tag):
        comment_tags = list(
            filter(lambda x: "comment" in x.text, row_tag.find_all("a"))
        )
        number_of_comments = int(comment_tags[0].text.split()[0]) if comment_tags else 0
        return max(number_of_comments, 0)