import requests
import re
import json
import os

headers = {
    "User-Agent": "Mozilla/5.0"
}
session = requests.Session()
response = session.get("https://www.thejustice.org/section/features", headers=headers)
article_pattern = "https://www.thejustice.org/article"
html = response.content.decode('utf-8')
NUMBER_OF_ARTICLES = 7

def extract_article(html: str) -> tuple:
    html_in_parts = re.split(article_pattern, html, maxsplit=2)
    match = re.match(r'^[^\'"]*', html_in_parts[1])  # until "
    article_link = (article_pattern + match.group(0))
    html = html_in_parts[2]
    
    title_pattern = r'>([^<]+)<\/a>'  # between ">" and "</a>"
    author_pattern = r'<span class="author-name byline"><a [^>]+>([^<]+)</a>'  # inside the <a> tag within the span
    description_pattern = r'<p class="article-abstract has-photo">([^<]+)'  # inside <p> tag with class "article-abstract has-photo"
    date_pattern = r'<span class="published-date">\s*\|\s*([\d/]+)\s*</span>'  # inside the <span class="published-date">
    
    title_match = re.search(title_pattern, html)
    title = title_match.group(1).strip()
    
    author_match = re.search(author_pattern, html)
    author = author_match.group(1).strip()

    description_match = re.search(description_pattern, html)
    description = description_match.group(1).strip()
    description = re.sub(r'&nbsp;', '', description)  # replace &nbsp; with a regular space

    date_match = re.search(date_pattern, html)
    date = date_match.group(1).strip()

    article = {
        "title": title,
        "author": author,
        "description": description,
        "date_published": date,
        "link": article_link
    }
    
    # remaining html after this article
    html = "https://www.thejustice.org/article/" + html.split("https://www.thejustice.org/article/", 1)[1]

    return article, html

def get_articles() -> str:
    articles = []
    remaining_html = html
    for _ in range(NUMBER_OF_ARTICLES):  # number of articles
        article, remaining_html = extract_article(remaining_html)
        articles.append(article)
        if not remaining_html:
            break
    return json.dumps(articles, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    # for testing purposes, print the result
    print(get_articles())