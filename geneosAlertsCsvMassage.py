from os import listdir
from os.path import isfile, join
from shutil import move

from pandas import DataFrame as df
import pandas as pd
import csv

import requests
import string
from datetime import datetime

from lxml import etree
from lxml import html

incomingFolder = '.\\in'
outFolder = '.\\out'
doneFolder = '.\\done'

url_1 = 'http://geneos.abc.com:7530/orb/bdos/local'
url_managed_entity_1 = 'http://geneos.abc.com:7530/orb/bdos/'

key_attribute = 'MyApplication'
managed_entity_view_name = 'Managed Entities Data'

parser = etree.HTMLParser()

r1 = requests.get(url_1)

tree_1 = etree.fromstring(r1.content, parser=parser)
trList_1 = tree_1.xpath('//table[@class=\'list bdo-list\']/tbody/tr')

for tr in trList_1 :
    if 'View=' + managed_entity_view_name in tr[1].text :
        exportID_1 = tr[2].text
        

url_me_1 = url_managed_entity_1 + exportID_1
r_me_1 = requests.get(url_me_1)
tree_me_1 = etree.fromstring(r_me_1.content, parser=parser)
trList_me_1 = tree_me_1.xpath('//tr')

me_app_mapping = []

for tr in trList_me_1:
    if len(tr.getchildren()) == 9 :
        if len(tr.getchildren()[2].getchildren()) == 1:
            if tr.getchildren()[2].getchildren()[0].text != None:
                attr_str = tr.getchildren()[8].getchildren()[0].text
                if key_attribute + '=' in attr_str :
                    for attr in attr_str.split(',') :
                        if key_attribute + '=' in attr :
                            app_name = attr.split('=')[1].strip()
                else:
                    app_name = None
                mapping = {'managedEntity': tr.getchildren()[2].getchildren()[0].text, 
                          'AppName': app_name}
                me_app_mapping.append(mapping)

dfMapping = df(me_app_mapping)

rawFileList = [f for f in listdir(incomingFolder) if isfile(join(incomingFolder , f))]
convert_yesno = lambda x : True if x == 'Yes' else False

for rawfile in rawFileList:
    
    date_time_str = rawfile.split(' ')[1].split('.')[0]
    hh = int(date_time_str.split('_')[1])
    date_str = date_time_str.split('_')[0]
    yyyy = int(date_str.split('-')[0])
    mm = int(date_str.split('-')[1])
    dd = int(date_str.split('-')[2])
    
    # print(yyyy, mm, dd, hh)
    
    with open(incomingFolder + '\\' + rawfile, 'rb') as f:
        reader = csv.reader(f)
        csvAsList = list(reader)
        csvAsList = csvAsList[2:]
        if (len(csvAsList)) <> 0 :
            with open('working\\temp.csv', 'w') as tempCsvFile:
                tempCsvWriter = csv.writer(tempCsvFile)
                for csvRow in csvAsList:
                    tempCsvWriter.writerow(csvRow)
            dfFromCsv = pd.read_csv('working\\temp.csv', 
                                    converters={'Active': convert_yesno, 
                                                'Snoozed': convert_yesno,
                                                'Knowledge Base': convert_yesno,
                                                'DirectKnowledgeBase': convert_yesno,
                                                'User Assign': convert_yesno})
            dfFromCsv['gateway'] = dfFromCsv['User Readable Path'].apply(lambda x: x.split('/ ')[1].strip())
            dfFromCsv['probe'] = dfFromCsv['User Readable Path'].apply(lambda x: x.split('/ ')[2].strip())
            dfFromCsv['managedEntity'] = dfFromCsv['User Readable Path'].apply(lambda x: x.split('/ ')[3].strip())
            dfFromCsv['sampler'] = dfFromCsv['User Readable Path'].apply(lambda x: x.split('/ ')[4].strip())
            dfFromCsv['dataview'] = dfFromCsv['User Readable Path'].apply(lambda x: x.split('/ ')[5].strip())
            dfFromCsv['snapshotDate'] = datetime(yyyy, mm, dd)
            dfFromCsv['snapshotHour'] = hh
            del dfFromCsv['User Readable Path']
            
            for I in dfFromCsv.iteritems():
                if I[0] == 'Assigned User Name' or 'Unnamed' in I[0]:
                    del dfFromCsv[I[0]]
            
            dfMergedWithApp = pd.merge(left=dfFromCsv, right=dfMapping,
                                      left_on='managedEntity', right_on='managedEntity',
                                      how='left')
            dfMergedWithApp.to_csv(outFolder + '\\ITRSAlerts_' 
                                   + yyyy.__str__() + '-' + mm.__str__() + '-' + dd.__str__()
                                   + '.' + hh.__str__() + '.csv',
                                  index=False,
                                  date_format='%Y-%m-%d')
            
    move(incomingFolder + '\\' + rawfile, doneFolder)
