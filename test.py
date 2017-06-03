#coding=utf-8
import requests

def geocode(address):
    parameters = {'address': address, 'key': 'cb649a25c1f81c1451adbeca73623251'}
    base = 'http://restapi.amap.com/v3/geocode/geo'
    response = requests.get(base, parameters)
    answer = response.json()
    print answer['geocodes']

address = '浦东锦华花园'
geocode(address)
