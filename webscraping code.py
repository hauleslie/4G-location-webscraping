import urllib
import re
import os
import time
from pandas import DataFrame
import csv
from array import array
start_time = time.time()
#all years html lines
years = ['http://www.att.com/gen/press-room?pid=4800&cdvn=news&newsfunction=searchresults&beginning_month=0&beginning_year=2014&ending_month=6&ending_year=2014',
         'http://www.att.com/gen/press-room?pid=4800&cdvn=news&newsfunction=searchresults&beginning_month=0&beginning_year=2013&ending_month=11&ending_year=2013',
        'http://www.att.com/gen/press-room?pid=4800&cdvn=news&newsfunction=searchresults&beginning_month=0&beginning_year=2012&ending_month=11&ending_year=2012',
        'http://www.att.com/gen/press-room?pid=4800&cdvn=news&newsfunction=searchresults&beginning_month=0&beginning_year=2011&ending_month=11&ending_year=2011']
city_all = []
state_w_city_all = []
date_all = []
link_all = []
#state = []
state_all = []
for y in years:
    regex = '<br><br><li>(.+?)</b>'
    pattern = re.compile(regex)
    htmlfile = urllib.urlopen(y)
    htmltext = htmlfile.read()
    substrings = re.findall(regex, htmltext) #puts each news release as an object in an array
    rollout_strings = [s for s in substrings if 'AT&T 4G LTE Available in' in s] #keep only 4G LTE rollout objects
    regex2 = '<a href="(.+?)">' #news release website link
    regex3 = 'AT&T 4G LTE Available in (.+?)</a>' #city
    regex4 = '</a><br>- (.+?) -- <b>' #state
    ##news release website link
    link = re.findall(regex2, str(rollout_strings))
    mystring = 'http://www.att.com'
    link = [mystring + l for l in link]
    ##city
    city = re.findall(regex3, str(rollout_strings))
    city = [c.strip() for c in city]
    ##state with city
    state_w_city = re.findall(regex4, str(rollout_strings))
    state_w_city = [s.strip() for s in state_w_city]
    ##state only
    for s in state_w_city:
        state_all.append(s[s.index(',')+2:])
    ##Launch Date
    date = [r.split(' -- <b>', 1)[1] for r in rollout_strings]
    ##for all years
    city_all.extend(city)
    state_w_city_all.extend(state_w_city)
    #state_all.extend(state)
    date_all.extend(date)
    link_all.extend(link)
my_data = zip(city_all, state_w_city_all, state_all, date_all, link_all)
fl = open('AT&T 4G LTE rollout dates.csv', 'wb')
writer = csv.writer(fl)
writer.writerow(['city', 'state with city', 'state', 'date', 'link']) #if needed
for values in my_data:
    writer.writerow(values)
fl.close()

"""
def out_csv(mydata, filename):
    with open('AT&T 4G LTE rollout dates.csv', 'w') as out_handle:
        out_handle.write(str('city', 'state', 'date', 'link' + '\n')) #if needed
        for line in mydata:
            out_handle.write(','.join(line) + '\n')
out_csv(my_data, 'AT&T 4G LTE rollout dates.csv')
links = re.finditer(pattern, htmltext)
results = [int(links.group(1)) for link in links]
list = []
for l in links:
http://www.att.com/gen/press-room?pid=9880
"""
