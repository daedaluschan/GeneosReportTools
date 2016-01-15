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
dfMapping.head()
