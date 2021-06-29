import requests 
import re
import pandas as pd
from bs4 import BeautifulSoup


code = "035720"

#요청할때마다 encparam, id가 필요하기 때문에 추출
re_enc = re.compile("encparam: '(.*)'", re.IGNORECASE) 
re_id = re.compile("id: '([a-zA-Z0-9]*)' ?", re.IGNORECASE)

url = "http://companyinfo.stock.naver.com/v1/company/c1010001.aspx?cmp_cd={}".format(code) 
html = requests.get(url).text 
encparam = re_enc.search(html).group(1) 
encid = re_id.search(html).group(1)


#영업이익, 당기순이익, 미래PER, 매출액, 현금배당수익율, ,PBR, PER
url = "http://companyinfo.stock.naver.com/v1/company/ajax/cF1001.aspx?cmp_cd={}&fin_typ=0&freq_typ=Y&encparam={}&id={}".format(code, encparam, encid) 
headers = {"Referer": "HACK"}
html = requests.get(url, headers=headers).text 
#print(html)
html = pd.read_html(html)
data_table = html[1]


df_columns = list(map(lambda x: ' '.join(x[1:]),data_table.columns))
data_table.columns = df_columns


매출액 = data_table.loc[0,:]
영업이익 = data_table.loc[1,:]
당기순이익 = data_table.loc[4,:]
PER = data_table.loc[26,:]
PBR = data_table.loc[28,:]
현금배당수익율 = data_table.loc[30,:]



