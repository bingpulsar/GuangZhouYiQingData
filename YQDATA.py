#coding:utf-8
import requests
from lxml import etree
import re
import pandas as pd
import matplotlib.pylab as plt

def GetData():
    headers0 = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0'}

    A=requests.get(url='http://wsjkw.gd.gov.cn/xxgzbdfk/yqtb/',headers=headers0)

    B=etree.HTML(A.text)

    C=B.xpath("//div[@class='section list']")[0]
    C_name = C.xpath("//div[@class='section list']/ul/li/a/text()")
    C_url = C.xpath("//div[@class='section list']/ul/li/a/@href")
    df=pd.DataFrame(columns=['Date', 'Confirmed', 'Infected', 'I2C'])
    for n in range(0,len(C_name)):
        
        C1=requests.get(url=C_url[n],headers=headers0).text

        print(n)
        pattern = re.compile(r'广州[0-9]*例')
        Total=pattern.findall(C1)
        df_=pd.DataFrame({\
            'Date':[C_name[n].replace('广东省新冠肺炎疫情情况','').replace('2022年','').replace('月','.').replace('日','')],\
            'Confirmed':[int(Total[0].replace('广州','').replace('例',''))],\
            'Infected':[int(Total[1].replace('广州','').replace('例',''))],\
            'I2C':[int(Total[2].replace('广州','').replace('例',''))]})
        df=pd.concat([df,df_],ignore_index=True)
    df.to_csv('17day.csv')
    return df

# GetData() 
plt.figure(figsize = (10,7))
plt.rcParams['font.sans-serif']= ['Heiti TC']#防止中文乱码
plt.rcParams['axes.unicode_minus']=False#解决负号'-'显示为方块的问题
df=pd.read_csv('17day.csv')
I=list(df['Infected'])[::-1]
C=list(df['Confirmed'])[::-1]
I2C=list(df['I2C'])[::-1]


plt.title('广州市11月新冠肺炎疫情情况')
plt.xlabel('日期')
plt.ylabel('病例数')
plt.yticks(range(0,max(I)+1000,1000))
plt.text(3,6000,'数据来源:广东省卫健委',fontdict={'fontsize':35},alpha = 0.2)
plt.text(5,4000,'By:bingCLeo',fontdict={'fontsize':35},alpha = 0.2)
# plt.text(6,4000,'By:bingCLeo',fontdict={'fontsize':35},alpha = 0.2)

for n in range(len(I)):
    plt.text(n-0.38,I[n]+75,str(I[n])+'例',fontdict={'fontsize':9},alpha = 0.7)
    if len(I)-2<=n:
        plt.text(n-0.38,C[n]+75,str(C[n])+'例',fontdict={'fontsize':8},alpha = 0.7)
        plt.text(n-0.38,I2C[n]+75,str(I2C[n])+'例',fontdict={'fontsize':8},alpha = 0.7)
plt.hlines(0,0,17,colors='r',linestyle='-',linewidth=1.5)
plt.fill_between(range(len(I)),I,I2C,facecolor = 'm',alpha = 0.2)
plt.fill_between(range(len(I)),I2C,C,facecolor = 'c',alpha = 0.2)
plt.plot(I,label='无症',color='m',linestyle='--',marker='h', linewidth=2.5, alpha = 0.8)
plt.plot(C,label='确诊',color='c',linestyle='--',marker='h', linewidth=2.5, alpha = 0.8)
plt.plot(I2C,label='无症状转确诊',color='g',linestyle='--',marker='h', linewidth=2.5, alpha = 0.8)
plt.xticks(range(len(df['Date'])),list(df['Date'])[::-1])
plt.legend()
plt.savefig('17day.jpg',dpi=600)
# plt.show()
