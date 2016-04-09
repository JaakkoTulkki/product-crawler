# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests
import json
import sys


def get_start_page_links(page_content):
    soup = BeautifulSoup(page_content, 'lxml')
    links = []
    for l in soup.findAll("div", {"class": "productInfo"}):
        links.extend(e['href'] for e in l.find_all("a") if e.has_attr("href"))
    # if we don't have links, then something is wrong
    if not links:
        raise Exception("No links!!")
    return links


def scrape_product_page(page_content):
    data = {}
    soup = BeautifulSoup(page_content, 'lxml')
    data['title'] = soup.find_all("div", {"class": "productTitleDescriptionContainer"})[0].get_text().replace("\n", "")
    data['description'] = ""
    # go through the meta tags, and take the one with "description"
    for m in soup.find_all("meta"):
        if m.has_attr("name") and m['name'] == "description":
            data['description'] = m['content']
            break
    # take unitprice and remove line breaks, pound sign etc
    unit_price = soup.find_all("p", {"class": "pricePerUnit"})
    # this is the most important data, and raise error if we don't have it
    if not unit_price:
        raise Exception("No unit price!!")
    unit_price = unit_price[0].get_text()
    unit_price = unit_price.replace(u"\n", "").replace(u"£", "").replace(u"/unit", "")
    data['unit_price'] = float(unit_price)
    # page content length into KB
    data['size'] = "{0:.2f} KB".format(len(page_content) / 1024)
    return data


def calculate_total_unit_costs(data):
    return sum([i['unit_price'] for i in data if 'unit_price' in i])


def run(start_url):
    response = requests.get(start_url)
    links = get_start_page_links(response.content)

    data = []
    for link in links:
        response = requests.get(link)
        data.append(scrape_product_page(response.content))

    total_unit_costs = calculate_total_unit_costs(data)

    final_data = {
        'results': data,
        'total': total_unit_costs
    }

    # dump into json
    final_data = json.dumps(final_data)
    sys.stdout.write(final_data)

if __name__ == "__main__":
    start_url = sys.argv[1]
    # start_url = "http://hiring-tests.s3-website-eu-west-1.amazonaws.com/2015_Developer_Scrape/5_products.html"
    run(start_url)