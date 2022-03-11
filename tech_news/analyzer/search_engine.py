from tech_news.database import search_news
import datetime


# Requisito 6
def search_by_title(title):
    title_list = []
    search_title = search_news({"title": {"$regex": title.capitalize()}})

    for titles in search_title:
        title_list.append((titles["title"], titles["url"]))
    return title_list


# Requisito 7
def search_by_date(date):
    date_list = []
    search_date = search_news({"timestamp": {"$regex": date}})

    try:
        datetime.date.fromisoformat(date)

        for dates in search_date:
            date_list.append((dates["title"], dates["url"]))
        return date_list
    except ValueError:
        raise ValueError("Data inválida")


# Requisito 8
def search_by_source(source):
    source_list = []
    source_news = search_news({"sources": {"$regex": source, "$options": "i"}})

    for sources in source_news:
        source_list.append((sources["title"], sources["url"]))
    return source_list


# Requisito 9
def search_by_category(category):
    category_list = []
    category_news = search_news(
        {"categories": {"$regex": category, "$options": "i"}}
    )

    for categories in category_news:
        category_list.append((categories["title"], categories["url"]))
    return category_list
