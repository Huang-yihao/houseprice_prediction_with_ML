# coding:utf-8    ctrl+/  注释
import urllib2
import time
import bs4
from bs4 import BeautifulSoup
import sys
import pymongo
import requests

def geocode(address):
    parameters = {'address': address, 'key': '8ac4f59c23c73f503f350494ff9310d3'}
    base = 'http://restapi.amap.com/v3/geocode/geo'
    response = requests.get(base, parameters)
    answer = response.json()
    print answer["geocodes"][0]['location'].encode('utf-8')
    print "geocodes" in {}.keys()

geocode("浦东春晖苑")
