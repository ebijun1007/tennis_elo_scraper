import json

import requests  # to get image from the web
from bs4 import BeautifulSoup
import pandas as pd


class EloScraper:
    link_atp_elo = "https://tennisabstract.com/reports/atp_elo_ratings.html"
    link_atp_yelo = "http://tennisabstract.com/reports/atp_season_yelo_ratings.html"
    link_wta_elo = "https://tennisabstract.com/reports/wta_elo_ratings.html"
    link_wta_yelo = "http://tennisabstract.com/reports/wta_season_yelo_ratings.html"

    def get_html_table(self, url):
        soup = BeautifulSoup(requests.get(url).content, "lxml")
        return soup.find("table", {"id": "reportable"})

    def convert_html_table_to_csv(self, table):
        # empty list
        data = []
        name_list = json.load(open('name_list.json', 'r'))

        # for getting the header from the HTML table
        list_header = []
        header = table.find("tr")

        for items in header:
            try:
                list_header.append(items.get_text())
            except:
                continue

        # for getting the data
        HTML_data = table.find_all("tr")[1:]

        for element in HTML_data:
            sub_data = []
            for sub_element in element:
                try:
                    sub_data.append(sub_element.get_text(strip=True))
                except:
                    continue
            sub_data[1] = sub_data[1].replace('\xa0', ' ')
            if(sub_data[1] in name_list.keys()):
                sub_data[1] = name_list[sub_data[1]]
            data.append(sub_data)

        return pd.DataFrame(data=data, columns=list_header)
