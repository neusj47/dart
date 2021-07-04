# -*- coding: utf-8 -*-

from urllib.request import urlopen
from io import BytesIO
from zipfile import ZipFile
import pandas as pd
from bs4 import BeautifulSoup
import xml.etree.ElementTree as Etree
import ssl


context = ssl._create_unverified_context()

api_key = '....'
url_code = 'https://opendart.fss.or.kr/api/corpCode.xml?crtfc_key=' + api_key

resp = urlopen(url_code, context=context)
result = resp.read()
xmlsoup = BeautifulSoup(result, 'html.parser')

with urlopen(url_code, context=context) as zip_response:
    with ZipFile(BytesIO(zip_response.read())) as zfile:
        zfile.extractall('corpCode')

tree = Etree.parse('corpCode/CORPCODE.xml')
root = tree.getroot()

corp_df = pd.DataFrame(columns=['corp_code', 'corp_name', 'stock_code', 'modify_date'])

for company in root.iter('list'):

    stock_code = company.findtext('stock_code')
    stock_code = stock_code.strip()

    if stock_code:
        company_dict = {
            'corp_code': company.findtext('corp_code'),
            'corp_name': company.findtext('corp_name'),
            'stock_code': company.findtext('stock_code'),
            'industry_code': company.findtext('induty_code')
        }

        corp_df = corp_df.append(company_dict, ignore_index=True)

corp_df.to_csv('corpCode.csv', index=False, encoding = 'CP949')



