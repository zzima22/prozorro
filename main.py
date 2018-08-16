# -*- coding: utf-8 -*-
import requests
import re
from bs4 import BeautifulSoup
import gc


# Любое слово в поиске
class SearchWord:
    string = []

    def __init__(self, value=''):
        self.value = value

    @classmethod
    def getinstances(cls):
        for obj in gc.get_objects():
            if isinstance(obj, SearchWord):
                print(obj.value)

    @classmethod
    def full_request(cls):
        result = []
        for obj in gc.get_objects():
            if isinstance(obj, SearchWord):
                n_string = "&" + str(obj.string) + "=" + obj.value
                result.append(n_string)
        return ''.join(result)[1:]


class Keyword(SearchWord):
    string = 'query'

    def __init__(self, value=''):
        super().__init__(value)


# Статус
class Status(SearchWord):
    string = 'status'

    def __init__(self, value):
        super().__init__(value)

# st1 = Status("Аукціон", "active.auction")
# st2 = Status("Подання пропозицій", "active.tendering")
# st3 = Status("Період уточнень", "active.enquiries")


    # decoder
def decoder(cod):
    return (cod.decode('cp1251')).encode('utf8')


# Суп
def get_links(key_):
    links = []
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0'
        }
        url = 'https://prozorro.gov.ua/tender/search/?%s' % key_
        # return url
        soup = BeautifulSoup(requests.get(url, headers=headers).text, "html.parser")

        for link in soup.find_all('a', {'class': 'items-list--header'}):
            if re.findall(r'/tender/', link.get('href')):
                links.append('https://prozorro.gov.ua' + link.get('href'))
    finally:
        return links


def get_docs(links):
    docs = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:61.0) Gecko/20100101 Firefox/61.0'
    }
    for i in links:
        soup = BeautifulSoup(requests.get(i, headers=headers).text, "html.parser")
        for doc in soup.find_all('a', {'class': 'word-break', 'href': re.compile("^https://")}):
            docs.append(doc.get('href'))
    return docs


# def make_dict(links, docs):
#     for i in links:
#         if
#     my_dict = {links: {links: docs}}
#     return my_dict

    # var my_dict = {
    #     "my_key": {
    #         "key_1": value_1,
    #         "key_2": value_2
    #     }


def main():
    keywords = ['printer']
    statuses = ["active.auction", "active.tendering", "active.enquiries"]
    k = [Keyword(i) for i in keywords]
    s = [Status(i) for i in statuses]
    # print(s)
    key_ = SearchWord.full_request()

    links = get_links(key_)
    print(links)
    docs = get_docs(links)
    print(docs)
    # rez = make_dict(links, docs)
    # print(rez)


if __name__ == '__main__':
    main()
