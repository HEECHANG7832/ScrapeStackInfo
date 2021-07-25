#!/usr/bin/env python
# coding: utf-8

# In[99]:


import requests 
import re
import pandas as pd
from bs4 import BeautifulSoup
import time
from datetime import datetime


# In[19]:



pd.options.display.float_format = '{:.2f}'.format #소수 둘째까지 


# In[29]:


### 코스피 200 기업, 정보 가져오기

KOSPI200_df = pd.read_excel('KOSPI200LIST.xlsx')


# In[30]:


KOSPI200_df


# In[59]:


stock_code = KOSPI200_df.loc[0,"종목코드"]
stock_name = KOSPI200_df.loc[0,"종목명"]
print(stock_code, stock_name)


# In[70]:


data_table_sum = pd.DataFrame(index=range(0,1))


for i in range(0, 10):

    stock_code = KOSPI200_df.loc[i,"종목코드"]
    stock_name = KOSPI200_df.loc[i,"종목명"]
    code = str(stock_code)
    code = code.zfill(6)
    print(str(i), code, stock_name)


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


    #컬럼명 년도만 추출
    df_columns = list(map(lambda x: ' '.join(x[1:]),data_table.columns))
    df_columns = [column[0:4] for column in df_columns]
    data_table.columns = df_columns
    
    #옛날 연도별 정보가 없는 경우 중복 제거
    data_table = data_table.loc[:, ~data_table.columns.duplicated(keep=False)]
        
    #매출액, 영업이익, 당기순이익, PER, PBR, 현금배당수익률
    data_table = data_table.loc[[0,1,4,26,28,30],]
    
    # + 종목코드, 종목명
    print(data_table)


    #부채비율, 당좌비율, 자본유보율
    url = "http://companyinfo.stock.naver.com/company/cF4002.aspx?cmp_cd={}&frq=0&rpt=3&finGubun=MAIN&frqTyp=0&cn=&encparam={}".format(code, encparam)
    headers = {"Referer": "HACK"}
    json = requests.get(url, headers=headers).json()

    for dic in json['DATA']:
        if dic['ACC_NM'] == '부채비율':
            부채비율 = []
            부채비율.append('부채비율')
            부채비율.append(dic['DATA1'])
            부채비율.append(dic['DATA2'])
            부채비율.append(dic['DATA3'])
            부채비율.append(dic['DATA4'])
            부채비율.append(dic['DATA5'])
        if dic['ACC_NM'] == '당좌비율':
            당좌비율 = []
            당좌비율.append('당좌비율')
            당좌비율.append(dic['DATA1'])
            당좌비율.append(dic['DATA2'])
            당좌비율.append(dic['DATA3'])
            당좌비율.append(dic['DATA4'])
            당좌비율.append(dic['DATA5'])     
        if dic['ACC_NM'] == '자본유보율':
            자본유보율 = []
            자본유보율.append('자본유보율')
            자본유보율.append(dic['DATA1'])
            자본유보율.append(dic['DATA2'])
            자본유보율.append(dic['DATA3'])
            자본유보율.append(dic['DATA4'])
            자본유보율.append(dic['DATA5'])

    #매출채권회전율, 재고자산회전율
    url = "http://companyinfo.stock.naver.com/company/cF4002.aspx?cmp_cd={}&frq=0&rpt=4&finGubun=MAIN&frqTyp=0&cn=&encparam={}".format(code, encparam)
    headers = {"Referer": "HACK"}
    json = requests.get(url, headers=headers).json()

    for dic in json['DATA']:
        if dic['ACC_NM'] == '매출채권회전율':
            매출채권회전율 = []
            매출채권회전율.append('매출채권회전율')
            매출채권회전율.append(dic['DATA1'])
            매출채권회전율.append(dic['DATA2'])
            매출채권회전율.append(dic['DATA3'])
            매출채권회전율.append(dic['DATA4'])
            매출채권회전율.append(dic['DATA5'])
        if dic['ACC_NM'] == '재고자산회전율':
            재고자산회전율 = []
            재고자산회전율.append('재고자산회전율')
            재고자산회전율.append(dic['DATA1'])
            재고자산회전율.append(dic['DATA2'])
            재고자산회전율.append(dic['DATA3'])
            재고자산회전율.append(dic['DATA4'])
            재고자산회전율.append(dic['DATA5'])

    df = pd.DataFrame([부채비율, 당좌비율, 자본유보율, 매출채권회전율, 재고자산회전율], columns = df_columns[0:6])
    df = df.loc[:, ~df.columns.duplicated(keep=False)]
    print(df)
    
    data_table = data_table.append(df, sort=False)
    data_table['종목코드'] = code
    data_table['종목명'] = stock_name
    
    data_table_sum = data_table_sum.append(data_table, sort=False)
    time.sleep(0.5)  # 0.5초 기다림
    

data_table_sum.reset_index(drop=True, inplace=True)
data_table_sum


# In[13]:





# 
# 
# 매출액
# 매출액 성장률 낮은
# 
# 배당금
# 적자면서 배당금
# 
# PER, PBR, PSR, PCR
# ROE ROA
# 
# 영업이익률 / 매출액
# 당기순이익률
# 
# 부채비율
# NCAV
# 

# In[102]:


#기본값


year = datetime.today().year        # 현재 연도 가져오기
post_post_year = year - 2
post_year = year - 1

year, post_year, post_post_year = map(str, [year, post_year, post_post_year])


print(year, post_year, post_post_year)


# In[103]:


#당기순이익 흑자 전환형
#20년도 적자 21년도 흑자
df_org = data_table_sum
df_org = df_org[df_org.loc[:,"주요재무"] == "당기순이익"]
df_org = df_org[df_org.loc[:,post_year] < 0]
df_org[df_org.loc[:,year] > 0].head(50)


# In[104]:



#영업이익 흑자 지속형
#20 흑자 21 흑자
df_org = data_table_sum
df_org = df_org[df_org.loc[:,"주요재무"] == "영업이익"]
df_org = df_org[df_org.loc[:,post_year] > 0]
df_org[df_org.loc[:,year] > 0].head(50)


# In[144]:


#직전 2개년도 영업이익 흑자인 기업
df_org = data_table_sum

df_org = df_org[(df_org['주요재무'] == "영업이익") | (df_org["주요재무"] == "매출액")]

df_org = df_org[df_org.loc[:,post_post_year] > 0]
df_org = df_org[df_org.loc[:,post_year] > 0]

#직전년도 매출액 감소 영업이익 증가
#df_org[(df_org['주요재무'] == "매출액") & ()]
df_매출 = df_org[(df_org['주요재무'] == "매출액")]
df_매출 = df_매출[df_매출[post_year] > df_매출[year]]
print(df_매출)

df_영업이익 = df_org[(df_org['주요재무'] == "영업이익")]
df_영업이익 = df_영업이익[df_영업이익[post_year] < df_영업이익[year]]
print(df_영업이익)

merge_inner = pd.merge(df_매출, df_영업이익, how='left')
merge_inner


# In[ ]:




