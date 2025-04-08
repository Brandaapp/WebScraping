from bs4 import BeautifulSoup
import requests
import json

headers = {
    "User-Agent": "Mozilla/5.0"
}
session = requests.Session()
NUMBER_OF_ARTICLES = 7

SECTIONS = {
    "News": "news",
    "Features": "features",
    "Forum": "forum",
    "Sports": "sports",
    "Arts and Culture": "arts"
}

def get_section_articles(section_url: str) -> list:
    response = session.get(section_url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    articles = []
    
    # Find all article elements
    article_elements = soup.find_all('article', class_='art-left', limit=NUMBER_OF_ARTICLES)
    
    for article in article_elements:
        # Extract title and link
        title_tag = article.find('h4', class_='art-left-headline').find('a')
        title = title_tag.get_text(strip=True) if title_tag else None
        link = title_tag['href'] if title_tag else None
        
        # Extract author
        author_tag = article.find('span', class_='author-name')
        author = author_tag.find('a').get_text(strip=True) if author_tag else None
        
        # Extract date
        date_tag = article.find('span', class_='published-date')
        date = date_tag.get_text(strip=True).replace('|', '').strip() if date_tag else None
        
        # Extract description (if available)
        description_tag = article.find('p', class_='article-abstract')
        description = description_tag.get_text(strip=True) if description_tag else ""
        
        articles.append({
            "title": title,
            "author": author,
            "description": description,
            "date_published": date,
            "link": link
        })
    
    return articles

def get_articles() -> str:
    all_sections = {}
    
    for section_name, section_path in SECTIONS.items():
        url = f"https://www.thejustice.org/section/{section_path}"
        section_articles = get_section_articles(url)
        all_sections[section_name] = section_articles
    
    return json.dumps(all_sections, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    print(get_articles())