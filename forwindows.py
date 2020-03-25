import html5lib
import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
import copy
import urllib

print("Initializing...")
def connect(host='http://google.com'):
    try:
        urllib.request.urlopen(host)
        return True
    except:
        return False


# test
if(connect()):
    print("Network Connected")
    users = ['vishaldhiman', 'ag9991323', 'sumit_5836', 'mrck572']

    levels = ['School', 'Basic', 'Easy', 'Medium', 'Hard']

    main_dict = {}
    geninfo = {}
    for user in users:
        # main_dict[user] = problems_dict
        try:
            URL = r'https://auth.geeksforgeeks.org/user/{}/practice'.format(
                user)
            r = requests.get(URL)

            soup = BeautifulSoup(r.content, 'html5lib')

            # Basic Info ---

            info = soup.find(
                'div', attrs={'id': 'detail1', 'class': 'mdl-grid descDiv'})
            tempinf = []
            for inf in info.findAll('div', attrs={
                    'class': 'mdl-cell mdl-cell--9-col mdl-cell--12-col-phone textBold'}):
                tempinf.append(inf.text)
            geninfo[user] = tempinf
            for inf in info.findAll('div', attrs={'class': 'mdl-cell mdl-cell--6-col mdl-cell--12-col-phone textBold'}):
                tempinf.append(inf.text)

        # Problems Info

            problems_dict = {'School': [], 'Easy': [],
                             'Basic': [], 'Medium': [], 'Hard': []}
            for level in range(0, len(levels)):
                difficulty_level = BeautifulSoup(features="html5lib")
                if(level == 2):
                    difficulty_level = soup.find(
                        'section', attrs={'class': 'mdl-tabs__panel tabsMaxHeightDiv is-active', 'id': levels[level]})
                else:
                    difficulty_level = soup.find(
                        'section', attrs={'class': 'mdl-tabs__panel tabsMaxHeightDiv', 'id': levels[level]})
                for row in difficulty_level.findAll('li', attrs={'class': 'mdl-cell mdl-cell--6-col mdl-cell--12-col-phone'}):
                    if row.a.text not in problems_dict[levels[level]]:
                        problems_dict[levels[level]].append(row.a.text)
            main_dict[user] = problems_dict
        except Exception as e:
            print(e)

    main_dict2 = copy.deepcopy(main_dict)

    # Reading csv

    for csvuser in main_dict2.keys():
        for csvfield in main_dict2[csvuser].keys():
            try:
                f = pd.read_csv('{}.csv'.format(csvuser), usecols=[csvfield])
                for i in f.values:
                    csv_value = ''.join(i)
                    if(csv_value in main_dict2[csvuser][csvfield]):
                        main_dict2[csvuser][csvfield].remove(csv_value)
            except Exception as e:
                # print(e)
                pass

    # writing into csv
    print(main_dict2)

    for csvuser in main_dict.keys():
        try:
            temp = []
            for csvfield in main_dict[csvuser].keys():
                temp.append(main_dict[csvuser][csvfield])
            la,lb,lc,ld,le = len(temp[0]),len(temp[1]),len(temp[2]),len(temp[3]),len(temp[4])
            max_len = max(la,lb,lc)
            if not max_len == la:
              temp[0].extend(['']*(max_len-la))
            if not max_len == lb:
              temp[1].extend(['']*(max_len-lb))
            if not max_len == lc:
              temp[2].extend(['']*(max_len-lc))
            if not max_len == ld:
              temp[3].extend(['']*(max_len-ld))
            if not max_len == le:
              temp[4].extend(['']*(max_len-le))
            mydict = {'School':temp[0],'Easy': temp[1],'Basic': temp[2],'Medium': temp[3],'Hard': temp[4]}
            df = pd.DataFrame(mydict)
            df.to_csv('{}.csv'.format(csvuser))
            
        except Exception as e:
            print(e)

    # Displaying All Info

    for user in main_dict2.keys():
        print(" ")
        print("User :- " + user)
        print("College/University :- " + geninfo[user][0])
        print("Cources enrolled :- " + geninfo[user][2])
        print("Rank in Institute :- " + geninfo[user][1])
        for inf in geninfo[user][3:]:
            print(inf)
        print("New Problems Solved:- ")
        for csvfield in main_dict2[user].keys():
            if(len(main_dict2[user][csvfield]) != 0):
                print(" "*3 + csvfield)
                for problem in main_dict2[user][csvfield]:
                    print(" "*5 + problem)
        print(" ")
        print("-------------")
else:
    print("Connect Internet first")
