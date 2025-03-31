from bs4 import BeautifulSoup
import requests
import json

def scrape_news_page(url, result, section):
    # Fetch the page
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Find the articles for the section
    articles = soup.find_all("div", class_="jet-listing-grid__item", limit=8)
    articles = articles[1:]  # The first div class returns is not a formal article
    for article in articles:
        # Extract title, author, date, description, and link fields
        title_tag = article.find("h4", class_="elementor-heading-title")
        title = title_tag.get_text(strip=True) if title_tag else None
        link = title_tag.find("a")["href"] if title_tag and title_tag.find("a") else None
        
        author_tag = article.find("h2", class_="elementor-heading-title")
        author = author_tag.get_text(strip=True) if author_tag else None
        
        date_tag = article.find("time")
        # return date in this format ("2024-12-06T06:00:43-05:00")
        date_published = date_tag["datetime"] if date_tag else None
        # Preprocess the date field to turn it into a meaningful date format (mm/dd/yyyy)
        date_published = date_published[5:7] + "/" + date_published[8:10] + "/" + date_published[0:4]

        description_tag = article.find("div", class_="jet-listing-dynamic-field__content")
        description = description_tag.get_text(strip=True) if description_tag else None

        # Append to the section
        result[section].append({
            "title": title,
            "author": author,
            "description": description,
            "date_published": date_published,
            "link": link
        })

    # Return the JSON result
    return result

def main():
    # URL of the hoot news
    url = "https://Brandeishoot.com"
    sections = ['News', 'Arts', 'Opinions', 'Editorials', 'Features', 'Sports']
    result = {section: [] for section in sections}

    # Loop through each section
    for section in sections:
        result = scrape_news_page(f"{url}/category/{section}", result, section)
    
    # Serialize to JSON and print out the output
    json_output = json.dumps(result, indent=2, ensure_ascii=False)
    print(json_output)
    
    # Save to news_data.json
    with open('news_data.json', 'w', encoding='utf-8') as f:
        f.write(json_output)


if __name__ == "__main__":
    main()
