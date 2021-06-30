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


#부채비율, 당좌비율, 자본유보율
url = "http://companyinfo.stock.naver.com/company/cF4002.aspx?cmp_cd={}&frq=0&rpt=3&finGubun=MAIN&frqTyp=0&cn=&encparam={}".format(code, encparam)
headers = {"Referer": "HACK"}
json = requests.get(url, headers=headers).json()



for dic in json['DATA']:
    if dic['ACC_NM'] == '부채비율':
        부채비율 = []
        부채비율.append(dic['DATA1'])
        부채비율.append(dic['DATA2'])
        부채비율.append(dic['DATA3'])
        부채비율.append(dic['DATA4'])
        부채비율.append(dic['DATA5'])
        부채비율.append(dic['DATA6'])
    if dic['ACC_NM'] == '당좌비율':
        당좌비율 = []
        당좌비율.append(dic['DATA1'])
        당좌비율.append(dic['DATA2'])
        당좌비율.append(dic['DATA3'])
        당좌비율.append(dic['DATA4'])
        당좌비율.append(dic['DATA5'])     
    if dic['ACC_NM'] == '자본유보율':
        자본유보율 = []
        자본유보율.append(dic['DATA1'])
        자본유보율.append(dic['DATA2'])
        자본유보율.append(dic['DATA3'])
        자본유보율.append(dic['DATA4'])
        자본유보율.append(dic['DATA5'])

print(부채비율)
print(당좌비율)
print(자본유보율)

#매출채권회전율, 재고자산회전율
url = "http://companyinfo.stock.naver.com/company/cF4002.aspx?cmp_cd={}&frq=0&rpt=4&finGubun=MAIN&frqTyp=0&cn=&encparam={}".format(code, encparam)
headers = {"Referer": "HACK"}
json = requests.get(url, headers=headers).json()

for dic in json['DATA']:
    if dic['ACC_NM'] == '매출채권회전율':
        매출채권회전율 = []
        매출채권회전율.append(dic['DATA1'])
        매출채권회전율.append(dic['DATA2'])
        매출채권회전율.append(dic['DATA3'])
        매출채권회전율.append(dic['DATA4'])
        매출채권회전율.append(dic['DATA5'])
    if dic['ACC_NM'] == '재고자산회전율':
        재고자산회전율 = []
        재고자산회전율.append(dic['DATA1'])
        재고자산회전율.append(dic['DATA2'])
        재고자산회전율.append(dic['DATA3'])
        재고자산회전율.append(dic['DATA4'])
        재고자산회전율.append(dic['DATA5'])
        
        
print(매출채권회전율)
print(재고자산회전율)


import pymysql

conn = None
cur = None

sql="desc BASIC_STACK_INFO"

conn = pymysql.connect(host="springboot2-webservice.ctsnx9zgivip.ap-northeast-2.rds.amazonaws.com",
                      user="admin",
                      password="",
                      db='stackinfo',
                      charset='utf8')
cur = conn.cursor()
print(cur.execute(sql))

