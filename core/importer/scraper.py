import re
import requests
from bs4 import BeautifulSoup
from ..importer.time_func import time_func


@time_func
def search_vuln(vulnObjID: str):
    base_url = "https://www.rapid7.com/db/vulnerabilities/"
    result = requests.get(f"{base_url}{vulnObjID}")
    # reference for optimizing BeautifulSoup:
    # https://beautiful-soup-4.readthedocs.io/en/latest/#improving-performance
    html = BeautifulSoup(result.text, "lxml")

    # remove script tags that they put in the middle of the lyrics
    [h.extract() for h in html(['style', 'script'])]

    vulnObj = {'Detail': "", 'Solution': "", 'References': ""}

    try:
        detailTag = html.find('div', class_='vulndb__detail-content')
        for tag in detailTag.findAll('p'):
            if tag.text != "":
                vulnObj['Detail'] += tag.text
        vulnObj['Detail'] = re.sub("\n", "", vulnObj['Detail']).strip()
        vulnObj['Detail'] = re.sub(" +", " ", vulnObj['Detail'])
    except AttributeError:
        pass

    try:
        solTag = html.find('section', class_='vulndb__references').find("ul")
        for tag in solTag.findAll('li'):
            if tag.text != "":
                vulnObj['Solution'] += tag.text + ", "
        vulnObj['Solution'] = re.sub("\n", "", vulnObj['Solution']).strip()
        vulnObj['Solution'] = re.sub(" +", " ", vulnObj['Solution'])
    except AttributeError:
        pass

    try:
        refTag = html.find('div', class_='vulndb__related-list').find("ul")
        for tag in refTag.findAll('li'):
            if tag.text != "":
                vulnObj['References'] += tag.text + " \n"
        #ref = re.sub("\n", "", ref).strip()
        vulnObj['References'] = re.sub(" +", " ", vulnObj['References'])
    except AttributeError:
        pass

    return vulnObj

