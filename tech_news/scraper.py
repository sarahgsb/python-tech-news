import requests
import time
from parsel import Selector
from tech_news.database import create_news


# Requisito 1
def fetch(url):
    try:
        response = requests.get(url, timeout=3)
        time.sleep(1)
        if response.status_code == 200:
            return response.text
    except requests.Timeout:
        return None


# Requisito 2
def scrape_novidades(html_content):
    selector = Selector(text=html_content)
    return selector.css("h3.tec--card__title a::attr(href)").getall()


# Requisito 3
def scrape_next_page_link(html_content):
    selector = Selector(text=html_content)
    return selector.css("a.tec--btn::attr(href)").get()


def get_writer(selector):
    writer = selector.css(".z--font-bold *::text").get()
    if writer:
        return writer.strip()
    return None


def get_share_counts(selector):
    share_counts = selector.css(".tec--toolbar__item::text").get()
    if share_counts:
        return int(share_counts.split()[0])
    return 0


def get_comments_counts(selector):
    comments_counts = selector.css("#js-comments-btn::attr(data-count)").get()
    if comments_counts:
        return int(comments_counts)
    return None


def get_summary(selector):
    summary = selector.css(
        ".tec--article__body > p:nth-child(1) *::text"
    ).getall()
    return "".join(summary)


def get_categories(selector):
    categories = selector.css("#js-categories a::text").getall()
    return categories


def get_sources(selector, _):
    sources = selector.css("div.z--mb-16 a::text").getall()
    return sources


def strip(list):
    list_items = []
    for item in list:
        list_items.append(item.strip())
    return list_items


def scrape_noticia(html_content):

    selector = Selector(html_content)
    url = selector.css("head link[rel=canonical]::attr(href)").get()
    title = selector.css("body .tec--article__header__title::text").get()
    datetime = selector.css(
        "div .tec--timestamp__item time::attr(datetime)"
    ).get()
    writer = get_writer(selector)
    shares_count = get_share_counts(selector)
    comments_count = get_comments_counts(selector)
    summary = get_summary(selector)
    categories = get_categories(selector)
    sources = get_sources(selector, categories)

    news_dict = {
        "url": url,
        "title": title,
        "timestamp": datetime,
        "writer": writer,
        "shares_count": shares_count,
        "comments_count": comments_count,
        "summary": summary,
        "sources": strip(sources),
        "categories": strip(categories),
    }
    return news_dict


# Requisito 5
def get_tech_news(amount):
    tech_news_list = []
    BASE_URL = "https://www.tecmundo.com.br/novidades"
    while BASE_URL:
        response = fetch(BASE_URL)
        scrape_news = scrape_novidades(response)

        for news in scrape_news:
            response_news = fetch(news)
            scrape = scrape_noticia(response_news)
            tech_news_list.append(scrape)
            if amount == len(tech_news_list):
                create_news(tech_news_list)
                return tech_news_list
        BASE_URL = scrape_next_page_link(response)
