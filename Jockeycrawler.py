#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu Jan 18 14:12:47 2018

@author: ZeyangBao
"""

from bs4 import BeautifulSoup
import requests
import time
import re
import numpy as np
import pandas as pd
from tqdm import tqdm
from multiprocessing import Pool, cpu_count

data = {'Date':[],
            'race number':[],
            'Turf':[],
            'Type':[],
            'Distance':[],
            'Horse ID':[],
            'Horse number in this race':[],
            'rider（Jocky) id':[],
            'Race rank':[]}
matrix_1 = pd.DataFrame(data)

data_2 = {'8 minutes': [],
                 '2 minutes': [],
                 '0 minutes': []}

matrix_2 = pd.DataFrame(data_2)

data_3 = {'0 minutes': [],
          '2 minutes': [],
          '5 minutes': [],
          '10 minutes': [],
          '15 minutes': []}
matrix_3 = pd.DataFrame(data_3)

data_4 = {'0 minutes': [],
          '2 minutes': [],
          '5 minutes': [],
          '10 minutes': [],
          '15 minutes': []}
matrix_4 = pd.DataFrame(data_4)

data_5 = {'0 minutes': [],
          '2 minutes': [],
          '5 minutes': [],
          '10 minutes': [],
          '15 minutes': []}
matrix_5 = pd.DataFrame(data_5)

dates = []
allurls = []
Odd_wburls = []
order = []
numberofhorse = 0
racenumber = ''
pair = {}
def login(url):  
    #wburl = urls
    session = requests.session()  
    # res = session.get('http://www.hkhorsedb.com/cseh/clist_result.php?vref=37347').content  
  
    login_data = {  
        'uname': 'yican',  
        'pass': '123456',  
        'op': 'login'  
    }  
    user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36"
    headers={"User-Agent":user_agent}
    session.post('http://www.hkhorsedb.com/cseh/user.php', data=login_data)  
    res = session.get(url, headers=headers)
    res.encoding = 'big5'
    #print(res.text)  
    return res
    print(res.text)  
    """
    soup = BeautifulSoup(res.text, 'html.parser')
    name = soup.find('font', "name")
    namestr = name.get_text()
    print (namestr)
    file = open("title.txt","w")  
    file.write(str(name))  
    file.close() 
    """
    
def get_url():
    wb_data = login('http://www.hkhorsedb.com/cseh/ctop.php?vdate=20180117')
    soup = BeautifulSoup(wb_data.text, 'lxml')
    LinksofDates = soup.find_all('select')[0]
    lod = LinksofDates.find_all('option')
    
    oddswbdata = login('http://www.hkhorsedb.com/cseh/passodds.php')
    soup =BeautifulSoup(oddswbdata.text, 'lxml')
    Alldays = soup.find_all('a', {"onclick":re.compile("poddsleftxml.php\?pcode=2\&rdate=\d\d\d\d\d\d\d\d\&vrecno=\d")})
    
    count = 0
    #print (LinksofDates)
    for i in range (204,205): #161 101
        urls = 'http://www.hkhorsedb.com/cseh/'+((lod[i])['value'])
        dates.append(urls)
        w = urls[len(urls)-8:len(urls)]
        w = w[len(w)-2:len(w)]+w[len(w)-4:len(w)-2]+w[0:len(w)-4]
        print (w)
#        print urls
        wbx_data = requests.get(urls)
        soupx = BeautifulSoup(wbx_data.text, 'lxml')
        links = soupx.find_all('a', {"href":re.compile("clist_result\.php\?vref=\d\d\d\d")}) #regular expression for urls of each competition
        for link in links:
            count = count +1
            fullurl = 'http://www.hkhorsedb.com/cseh/'+link['href']
#            print fullurl
            allurls.append(fullurl) 
    
    #url = re.findall(re"poddsleftxml.php\?pcode=2\&rdate=\d\d\d\d\d\d\d\d\&vrecno=\d", url_2min)[0]
#        x = Alldays[i-1]['onclick']
#        y = "http://www.hkhorsedb.com/cseh/"+re.findall(r'poddsleftxml.php\?pcode=2\&rdate=\d\d\d\d\d\d\d\d\&vrecno=', x)[0]
        y = "http://www.hkhorsedb.com/cseh/poddsleftxml.php?pcode=2&rdate="+w+"&vrecno="
        for j in range(1,count+1):
            Odd_wburls.append(y+str(j))
#            print y+str(j)
        count = 0
    
def get_info(url):
    global numberofhorse 
    numberofhorse = 0
    wb_data = login(url)
    soup =BeautifulSoup(wb_data.text, 'lxml')
    table = soup.find_all('table', attrs={"width": "100%", "border": "0","cellspacing": "1","cellpadding": "0" ,"bgcolor": "#D6DFF7"})
    #four = table.find_all('td', attrs={"width": "20%", "height": "45"})
    tr = (table[2].find_all('tr'))[2]
    Date = soup.find('font', "name").get_text()
    Number = soup.find('font', "lfont").get_text()
    win_name = (tr.find_all('td')[3]).find('a').get_text()
    rider = (tr.find_all('td')[5]).find('a').get_text()
    trainer = (tr.find_all('td')[7]).find('a').get_text()
    odds_8minutes = (tr.find_all('td')[16]).get_text()
    odds_2minutes = (tr.find_all('td')[17]).get_text()
    odds_0minutes = (tr.find_all('td')[18]).get_text()
    data = {'Date':[],
            'race number':[],
            'Turf':[],
            'Type':[],
            'Distance':[],
            'Horse ID':[],
            'Weight':[],
            'Horse number in this race':[],
            'rider id':[],
            'Race rank':[]}
    matrix1 = pd.DataFrame(data)

    length = len(table[2].find_all('tr'))
    global pair
    pair = {}
    global order
    order = []
    k = []
    for i in range (2, length):
        tr = (table[2].find_all('tr'))[i]
#        w = (tr.find_all('td')[15]).find('img')
#        if w is None:
#            numberofhorse = numberofhorse+1
#            continue
#        numberofhorse = numberofhorse+1
        rawdate = soup.find('font', "name").get_text()
        Date = re.findall(r"\d\d\d\d-\d\d-\d\d",rawdate)[0]
        Date = Date.replace('-', '')
        number = (soup.find('span', "Chin").get_text())
        global racenumber
        racenumber = re.findall(r"\d\d\d", number)
        distanceclass = soup.find('font', 'nfont').get_text()
        distance = re.findall(r"\d\d\d\d", distanceclass)[0]+'m'
        Horsenumber = (tr.find_all('td')[4]).find('div').get_text()
        rawnumbernow = (tr.find_all('td')[2]).find('img')['src']
        numbernow = re.findall(r"\d+", rawnumbernow)[0]
        if numbernow not in k:
            numberofhorse = numberofhorse+1
            k.append(numbernow)
            print (numbernow)
        rider = (tr.find_all('td')[5]).find('a').get_text()
        trainer = (tr.find_all('td')[7]).find('a').get_text()
        typetd = (soup.find_all('span', 'Chin')[2]).get_text()
        Type = typetd[0]+typetd[1]
        Type = Type.encode('utf-8')
        Turf = typetd[3]+typetd[4]
        Turf = Turf.encode('utf-8')
        Weight = (tr.find_all('td')[12]).find('div').get_text()
        CarryWeight = (tr.find_all('td')[6]).find('div').get_text()
        data1 = {'Date':Date,
            'race number':racenumber[0],
            'Turf':Turf,
            'Type':Type,
            'Distance':distance,
            'Horse ID':Horsenumber,
            'Weight':Weight.encode('utf-8'),
            'CarryWeight': CarryWeight.encode('utf-8'),
            'Horse number in this race':numbernow,
            'rider（Jocky) id':'NA',
            'Race rank':i-1,
            'Rider': rider.encode('utf-8'),
            'Trainer': trainer.encode('utf-8')}
        global matrix_1
        matrix_1 = matrix_1.append(data1,ignore_index=True)
        
#        eightminutes = (tr.find_all('td')[16]).get_text()
#        twominutes = (tr.find_all('td')[17]).get_text()
#        zerominutes = (tr.find_all('td')[18]).get_text()
        
        global order
        name = (tr.find_all('td')[3]).get_text().strip()
        name = name.encode('utf-8')
        order.append(name)
        if not pair.has_key(numbernow):
            pair[numbernow] = Horsenumber
#        data_2 = {'8 minutes': eightminutes,
#                 '2 minutes': twominutes,
#                 '0 minutes': zerominutes}
#        global matrix_2
#        matrix_2 = matrix_2.append(data_2,ignore_index=True)
    
    columns = ['Date','race number','Turf','Type','Distance','Horse ID', 'Weight', 'CarryWeight','Horse number in this race','Rider','Trainer' ,'Race rank']
    matrix_1.to_csv('/Users/ZeyangBao/Desktop/info1.csv', columns=columns)
    print len(pair), "order length"
    return order
#    columns_2 = ['0 minutes', '2 minutes', '8 minutes']
#    matrix_2.to_csv('/Users/ZeyangBao/Desktop/winodds.csv', columns=columns_2)


        
    
def get_placeodds(urls, order):
    wb_data = login(urls)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    d = {}
    d_winodd = {}
    tr = soup.find_all('tr', {"height":"30"})
    for x in tr:
        num = x.find_all('td', {"class": "Header2"})
        if len(num)>0:
            if num[0].get_text().strip()!='':
                #print num[0].get_text().strip()
                numberofhorse = int(num[0].get_text().strip())
        y = x.find_all('td')
        name = y[1].get_text().strip()
        if x.find_all('td')[3].get_text().strip()!='':
            placeodd_0 = y[4].get_text().strip()
            winodd_0 = y[2].get_text().strip()
            d[name] = [placeodd_0]
            d_winodd[name] = [winodd_0]
        else:
            placeodd_0 = 'NAN'
            winodd_0 = 'NAN'
            d[name] = [placeodd_0]
            d_winodd[name] = [winodd_0]
        
    wb_data = login(urls+'&ptime=2')
    soup = BeautifulSoup(wb_data.text, 'lxml')
    tr = soup.find_all('tr', {"height":"30"})
    if(len(tr)==0):
        for n in d:
            d[n].append('NAN')
            d_winodd[n].append('NAN')
    else:
        for x in tr:
            y = x.find_all('td')
            name = y[1].get_text().strip()
            placeodd_2 = y[7].get_text().strip()
            winodd_2 = y[5].get_text().strip()
            if x.find_all('td')[3].get_text().strip()!='':
                d[name].append(placeodd_2)
                d_winodd[name].append(winodd_2)
            else:
                d[name].append('NAN')
                d_winodd[name].append('NAN')
    
    wb_data = login(urls+'&ptime=5')
    soup = BeautifulSoup(wb_data.text, 'lxml')
    tr = soup.find_all('tr', {"height":"30"})
    if(len(tr)==0):
        for n in d:
            d[n].append('NAN')
            d_winodd[n].append('NAN')
    else:
        for x in tr:
            y = x.find_all('td')
            name = y[1].get_text().strip()
            placeodd_5 = y[7].get_text().strip()
            winodd_5 = y[5].get_text().strip()
            if x.find_all('td')[3].get_text().strip()!='':
                d[name].append(placeodd_5)
                d_winodd[name].append(winodd_5)
            else:
                d[name].append('NAN')
                d_winodd[name].append('NAN')
    
    wb_data = login(urls+'&ptime=10')
    soup = BeautifulSoup(wb_data.text, 'lxml')
    tr = soup.find_all('tr', {"height":"30"})
    if(len(tr)==0):
        for n in d:
            d[n].append('NAN')
            d_winodd[n].append('NAN')
    else:
        for x in tr:
            y = x.find_all('td')
            name = y[1].get_text().strip()
            placeodd_10 = y[7].get_text().strip()
            winodd_10 = y[5].get_text().strip()
            if x.find_all('td')[3].get_text().strip()!='':
                d[name].append(placeodd_10)
                d_winodd[name].append(winodd_10)
            else:
                d[name].append('NAN')
                d_winodd[name].append('NAN')
    
    wb_data = login(urls+'&ptime=15')
    soup = BeautifulSoup(wb_data.text, 'lxml')
    tr = soup.find_all('tr', {"height":"30"})
    if(len(tr)==0):
        for n in d:
            d[n].append('NAN')
            d_winodd[n].append('NAN')
    else:
        for x in tr:
            y = x.find_all('td')
            name = y[1].get_text().strip()
            placeodd_15 = y[7].get_text().strip()
            winodd_15 = y[5].get_text().strip()
            if x.find_all('td')[3].get_text().strip()!='':
                d[name].append(placeodd_15)
                d_winodd[name].append(winodd_15)
            else:
                d[name].append('NAN')
                d_winodd[name].append('NAN')
        
    for x in order:
        x = x.decode('utf-8')
        if d.has_key(x):
#            print d[x]
            z = d[x]
            w = d_winodd[x]
            z[0] = z[0].encode('utf-8')
            w[0] = w[0].encode('utf-8')
            if z[0] != u'0':
                data_3 = {'0 minutes': z[0],
                          '2 minutes': z[1],
                          '5 minutes': z[2],
                          '10 minutes': z[3],
                          '15 minutes': z[4]}
                data_2 = {'0 minutes': w[0],
                          '2 minutes': w[1],
                          '5 minutes': w[2],
                          '10 minutes': w[3],
                          '15 minutes': w[4]}
                
#                print x.encode('utf-8'), "is", z[0], z[1], z[2]
        else:
            data_3 = {'0 minutes': 'NAN',
                      '2 minutes': 'NAN',
                      '5 minutes': 'NAN',
                      '10 minutes': 'NAN',
                      '15 minutes': 'NAN'}
            data_2 = {'0 minutes': 'NAN',
                      '2 minutes': 'NAN',
                      '5 minutes': 'NAN',
                      '10 minutes': 'NAN',
                      '15 minutes': 'NAN'}
#            print x.encode('utf-8'), "is", "NAN"
        global matrix_3
        global matrix_2
        columns = ['0 minutes', '2 minutes', '5 minutes', '10 minutes', '15 minutes']
        matrix_3 = matrix_3.append(data_3,ignore_index=True)
        matrix_3.to_csv('/Users/ZeyangBao/Desktop/placeodds1.csv', columns = columns)
        matrix_2 = matrix_2.append(data_2,ignore_index=True)
        matrix_2.to_csv('/Users/ZeyangBao/Desktop/winodds1.csv', columns = columns)
        order = []

def get_q(urls):
    global pair
    Pair = []
    Pair2 = []
    wb_data = wb_data = login(urls)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    global numberofhorse
    numofhorse = numberofhorse
    if numberofhorse>14:
        numofhorse = 14
    if numofhorse <= 8:
        for i in range (1, numofhorse):
            for j in range (i+1, numofhorse+1):
                str1 = str(i)
                str2 = str(j)
                Pair.append(str1)
                Pair2.append(str2)
    else:
        print (numofhorse)
        for i in range (1, 8):
            for j in range (i+1, numofhorse+1):
                str1 = str(i)
                str2 = str(j)
                Pair.append(str1)
                Pair2.append(str2)
        if(numofhorse>8):
            for i in range(1, numofhorse-7):
                for j in range(1, i+1):
                    Pair.insert((numofhorse-1)*i, str((8+i)-j))
                    Pair2.insert((numofhorse-1)*i, str(i+8))
    #    print len(Pair)
    q_0minlist = []
    q_2minlist = []
    q_5minlist = []
    q_10minlist = []
    q_15minlist = []
    date = urls[urls.find("rdate")+6:urls.find("rdate")+14]
    date = date[4:8]+date[2:4]+date[0:2]
    global racenumber
    numofcomp = racenumber
    wb_data = login(urls)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    
    if len(soup.find_all('table', {"cellpadding": "-1"}))==0:
        print len(Pair2), 'and', len(Pair)
        for i in range(0, len(Pair)):
            data_4 = {'0 minutes': 'NA',
                          '2 minutes': 'NA',
                          '5 minutes': 'NA',
                          '10 minutes': 'NA',
                          '15 minutes': 'NA',
                          'Date': date,
                          'race number': numofcomp[0],
                          'Pair': pair[Pair[i]],
                          'Pair2': pair[Pair2[i]]}
            
            global matrix_4
            matrix_4 = matrix_4.append(data_4,ignore_index=True)
            columns = ['Date','race number','Pair','Pair2','0 minutes', '2 minutes', '5 minutes', '10 minutes', '15 minutes']
            matrix_4.to_csv('/Users/ZeyangBao/Desktop/qodds1.csv', columns = columns)
            
    else:   
        table = soup.find_all('table', {"cellpadding": "-1"})[0]
        tr = table.find_all('tr')
        for t in tr:
            td = t.find_all('td', {'class':re.compile("GridData(\d)*")})
            for d in td:
                num = d.get_text().strip()
                num = num.replace(u'\xa0', u' ') 
                lst = num.split(' ')
                if num == '':
                    continue
                else:
                    q_0min = lst[0]
                    q_0minlist.append(q_0min)
    #                print "0 minutes"+q_0min
                    
        wb_data = login(urls+'&ptime=2')
        soup = BeautifulSoup(wb_data.text, 'lxml')
        if(len(soup.find_all('table', {"cellpadding": "-1"}))==0):
            q_2min = 'NAN'
            for i in range(1, ((numofhorse-1)*numofhorse/2)+1):
                q_2minlist.append(q_2min)
    #            print "2 minutes" + q_2min
        else:
            table = soup.find_all('table', {"cellpadding": "-1"})[0]
            tr = table.find_all('tr')
            for t in tr:
                td = t.find_all('td', {'class':re.compile("GridData(\d)*")})
                for d in td:
                    num = d.get_text().strip()
                    num = num.replace(u'\xa0', u' ') 
                    lst = num.split(' ')
                    if num == '':
                        continue
                    else:
                        q_2min = lst[0]
                        q_2minlist.append(q_2min)
    #                    print "2 minutes"+q_2min
                    
        wb_data = login(urls+'&ptime=5')
        soup = BeautifulSoup(wb_data.text, 'lxml')
        if(len(soup.find_all('table', {"cellpadding": "-1"}))==0):
            q_5min = 'NAN'
            for i in range(1, ((numofhorse-1)*numofhorse/2)+1):
                q_5minlist.append(q_5min)
    #            print "5 minutes" + q_5min
        else: 
            table = soup.find_all('table', {"cellpadding": "-1"})[0]
            tr = table.find_all('tr')
            for t in tr:
                td = t.find_all('td', {'class':re.compile("GridData(\d)*")})
                for d in td:
                    num = d.get_text().strip()
                    num = num.replace(u'\xa0', u' ')  
                    if num == '':
                        continue
                    else:
                        q_5min = num[0: num.find(' ')]
                        q_5minlist.append(q_5min)
    #                    print "5 minutes" + q_5min
                        
        wb_data = login(urls+'&ptime=10')
        soup = BeautifulSoup(wb_data.text, 'lxml')
        if(len(soup.find_all('table', {"cellpadding": "-1"}))==0):
            q_10min = 'NAN'
            for i in range(1, ((numofhorse-1)*numofhorse/2)+1):
                q_10minlist.append(q_10min)  
    #            print "10 minutes" + q_10min
        else:
            table = soup.find_all('table', {"cellpadding": "-1"})[0]
            tr = table.find_all('tr')
            for t in tr:
                td = t.find_all('td', {'class':re.compile("GridData(\d)*")})
                for d in td:
                    num = d.get_text().strip()
                    num = num.replace(u'\xa0', u' ')  
                    if num == '':
                        continue
                    else:
                        q_10min = num[0: num.find(' ')]
                        q_10minlist.append(q_10min)
    #                    print "10 minutes" + q_10min
                    
        wb_data = login(urls+'&ptime=15')
        soup = BeautifulSoup(wb_data.text, 'lxml')
        if(len(soup.find_all('table', {"cellpadding": "-1"}))==0):
            q_15min = 'NAN'
            for i in range(1, ((numofhorse-1)*numofhorse/2)+1):
                q_15minlist.append(q_15min)  
    #            print "15 minutes" + q_15min
        else:
            table = soup.find_all('table', {"cellpadding": "-1"})[0]
            tr = table.find_all('tr')
            for t in tr:
                td = t.find_all('td', {'class':re.compile("GridData(\d)*")})
                for d in td:
                    num = d.get_text().strip()
                    num = num.replace(u'\xa0', u' ')  
                    if num == '':
                        continue
                    else:
                        q_15min = num[0: num.find(' ')]
                        q_15minlist.append(q_15min)
    #                    print "15 minutes" + q_15min
        print "hello ", len(Pair)
        for i in range(0, len(q_0minlist)):
            data_4 = {'0 minutes': q_0minlist[i],
                          '2 minutes': q_2minlist[i],
                          '5 minutes': q_5minlist[i],
                          '10 minutes': q_10minlist[i],
                          '15 minutes': q_15minlist[i],
                          'Date': date,
                          'race number': numofcomp[0],
                          'Pair': pair[Pair[i]],
                          'Pair2': pair[Pair2[i]]}
            
            global matrix_4
            matrix_4 = matrix_4.append(data_4,ignore_index=True)
            columns = ['Date','race number','Pair','Pair2','0 minutes', '2 minutes', '5 minutes', '10 minutes', '15 minutes']
            matrix_4.to_csv('/Users/ZeyangBao/Desktop/qodds1.csv', columns = columns)


def get_pq(urls):
    global pair
    Pair = []
    Pair2 = []
    wb_data = wb_data = login(urls)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    global numberofhorse
    numofhorse = numberofhorse
    if numberofhorse>14:
        numofhorse = 14
    if numofhorse <= 8:
        for i in range (1, numofhorse):
            for j in range (i+1, numofhorse+1):
                str1 = str(i)
                str2 = str(j)
                Pair.append(str1)
                Pair2.append(str2)
    else:
        print (numofhorse)
        for i in range (1, 8):
            for j in range (i+1, numofhorse+1):
                str1 = str(i)
                str2 = str(j)
                Pair.append(str1)
                Pair2.append(str2)
        if(numofhorse>8):
            for i in range(1, numofhorse-7):
                for j in range(1, i+1):
                    Pair.insert((numofhorse-1)*i, str((8+i)-j))
                    Pair2.insert((numofhorse-1)*i, str(i+8))
    #    print len(Pair)
    q_0minlist = []
    q_2minlist = []
    q_5minlist = []
    q_10minlist = []
    q_15minlist = []
    date = urls[urls.find("rdate")+6:urls.find("rdate")+14]
    date = date[4:8]+date[2:4]+date[0:2]
    global racenumber
    numofcomp = racenumber
    wb_data = login(urls)
    soup = BeautifulSoup(wb_data.text, 'lxml')
    
    if len(soup.find_all('table', {"cellpadding": "-1"}))==0:
        print len(Pair2), 'and', len(Pair)
        for i in range(0, len(Pair)):
            data_5 = {'0 minutes': 'NA',
                          '2 minutes': 'NA',
                          '5 minutes': 'NA',
                          '10 minutes': 'NA',
                          '15 minutes': 'NA',
                          'Date': date,
                          'race number': numofcomp[0],
                          'Pair': pair[Pair[i]],
                          'Pair2': pair[Pair2[i]]}
            
            global matrix_5
            matrix_5 = matrix_5.append(data_5,ignore_index=True)
            columns = ['Date','race number','Pair','Pair2','0 minutes', '2 minutes', '5 minutes', '10 minutes', '15 minutes']
            matrix_5.to_csv('/Users/ZeyangBao/Desktop/qodds1.csv', columns = columns)
            
    else:   
        table = soup.find_all('table', {"cellpadding": "-1"})[1]
        tr = table.find_all('tr')
        for t in tr:
            td = t.find_all('td', {'class':re.compile("GridData(\d)*")})
            for d in td:
                num = d.get_text().strip()
                num = num.replace(u'\xa0', u' ') 
                lst = num.split(' ')
                if num == '':
                    continue
                else:
                    q_0min = lst[0]
                    q_0minlist.append(q_0min)
    #                print "0 minutes"+q_0min
                    
        wb_data = login(urls+'&ptime=2')
        soup = BeautifulSoup(wb_data.text, 'lxml')
        if(len(soup.find_all('table', {"cellpadding": "-1"}))==0):
            q_2min = 'NAN'
            for i in range(1, ((numofhorse-1)*numofhorse/2)+1):
                q_2minlist.append(q_2min)
    #            print "2 minutes" + q_2min
        else:
            table = soup.find_all('table', {"cellpadding": "-1"})[1]
            tr = table.find_all('tr')
            for t in tr:
                td = t.find_all('td', {'class':re.compile("GridData(\d)*")})
                for d in td:
                    num = d.get_text().strip()
                    num = num.replace(u'\xa0', u' ') 
                    lst = num.split(' ')
                    if num == '':
                        continue
                    else:
                        q_2min = lst[0]
                        q_2minlist.append(q_2min)
    #                    print "2 minutes"+q_2min
                    
        wb_data = login(urls+'&ptime=5')
        soup = BeautifulSoup(wb_data.text, 'lxml')
        if(len(soup.find_all('table', {"cellpadding": "-1"}))==0):
            q_5min = 'NAN'
            for i in range(1, ((numofhorse-1)*numofhorse/2)+1):
                q_5minlist.append(q_5min)
    #            print "5 minutes" + q_5min
        else: 
            table = soup.find_all('table', {"cellpadding": "-1"})[1]
            tr = table.find_all('tr')
            for t in tr:
                td = t.find_all('td', {'class':re.compile("GridData(\d)*")})
                for d in td:
                    num = d.get_text().strip()
                    num = num.replace(u'\xa0', u' ')  
                    if num == '':
                        continue
                    else:
                        q_5min = num[0: num.find(' ')]
                        q_5minlist.append(q_5min)
    #                    print "5 minutes" + q_5min
                        
        wb_data = login(urls+'&ptime=10')
        soup = BeautifulSoup(wb_data.text, 'lxml')
        if(len(soup.find_all('table', {"cellpadding": "-1"}))==0):
            q_10min = 'NAN'
            for i in range(1, ((numofhorse-1)*numofhorse/2)+1):
                q_10minlist.append(q_10min)  
    #            print "10 minutes" + q_10min
        else:
            table = soup.find_all('table', {"cellpadding": "-1"})[1]
            tr = table.find_all('tr')
            for t in tr:
                td = t.find_all('td', {'class':re.compile("GridData(\d)*")})
                for d in td:
                    num = d.get_text().strip()
                    num = num.replace(u'\xa0', u' ')  
                    if num == '':
                        continue
                    else:
                        q_10min = num[0: num.find(' ')]
                        q_10minlist.append(q_10min)
    #                    print "10 minutes" + q_10min
                    
        wb_data = login(urls+'&ptime=15')
        soup = BeautifulSoup(wb_data.text, 'lxml')
        if(len(soup.find_all('table', {"cellpadding": "-1"}))==0):
            q_15min = 'NAN'
            for i in range(1, ((numofhorse-1)*numofhorse/2)+1):
                q_15minlist.append(q_15min)  
    #            print "15 minutes" + q_15min
        else:
            table = soup.find_all('table', {"cellpadding": "-1"})[1]
            tr = table.find_all('tr')
            for t in tr:
                td = t.find_all('td', {'class':re.compile("GridData(\d)*")})
                for d in td:
                    num = d.get_text().strip()
                    num = num.replace(u'\xa0', u' ')  
                    if num == '':
                        continue
                    else:
                        q_15min = num[0: num.find(' ')]
                        q_15minlist.append(q_15min)
    #                    print "15 minutes" + q_15min
        print "hello ", len(Pair)
        for i in range(0, len(q_0minlist)):
            data_5 = {'0 minutes': q_0minlist[i],
                          '2 minutes': q_2minlist[i],
                          '5 minutes': q_5minlist[i],
                          '10 minutes': q_10minlist[i],
                          '15 minutes': q_15minlist[i],
                          'Date': date,
                          'race number': numofcomp[0],
                          'Pair': pair[Pair[i]],
                          'Pair2': pair[Pair2[i]]}
            
            global matrix_5
            matrix_5 = matrix_5.append(data_5,ignore_index=True)
            columns = ['Date','race number','Pair','Pair2','0 minutes', '2 minutes', '5 minutes', '10 minutes', '15 minutes']
            matrix_5.to_csv('/Users/ZeyangBao/Desktop/pqodds1.csv', columns = columns)

#def main(x):
#    try:
#        print ("Day"+" "+str(x))
#        get_info(allurls[x])
#        get_placeodds(Odd_wburls[x], order)
#        get_q(Odd_wburls[x])
##        get_pq(Odd_wburls[x])
#    except BaseException:
#        print ("ERROR")
#        
#    if x>0 and x%5==0:
#        time.sleep(3)
#    time.sleep(0.1)

get_url()
#pool = Pool(cpu_count())
#pool.map(main, (x for x in range(0, len(allurls))))
##pool.map(get_q, (urls for urls in Odd_wburls))
#pool.close()
#pool.join()

for x in tqdm(range(0, len(allurls))):
    try:
        print ("Day"+" "+str(x))
        get_info(allurls[x])
        get_placeodds(Odd_wburls[x], order)
        get_q(Odd_wburls[x])
        get_pq(Odd_wburls[x])
    except:
        print "ERROR"
    else:
        continue
 
    if x>0 and x%5==0:
        time.sleep(3)
    time.sleep(0.1)
