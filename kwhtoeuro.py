#!/usr/bin/python3

from influxdb import InfluxDBClient
from time import sleep
import configparser
 
config = configparser.ConfigParser()
config.read_file(open('./token.config', mode='r'))
host = config.get('config', 'host')
user = config.get('config', 'user')
password = config.get('config', 'password')
dbname = config.get('config', 'dbname')

client = InfluxDBClient(host, 8086, user, password, dbname)

def strom(data):
    euro = data*0.4
    return euro

def shelly():
    data = client.query('SELECT sum("mean")/3600/1000 FROM (SELECT mean("total_act_power") FROM "shelly" GROUP BY time(1s) fill(previous))')
    data = data.raw
    data = data["series"]
    data = data[0]
    data = data["values"]
    data = data[0]
    data = data[1]
    euro = strom(data)
    write_data = {}
    write_data['measurement'] = 'euro'
    write_data['fields'] = {"euro_gesamtWG": euro}
    client.write_points([write_data])    
    write_data = {}
    write_data['measurement'] = 'euro'
    write_data['fields'] = {"Verbrauch_gesamtWG": data}
    if client.write_points([write_data]):
        return
    else:
        print("Daten konnten nicht gesendet werden.") 

if __name__ == '__main__':
    while True:
        shelly()
        print("Daten wurden gesendet.")
        sleep(60)
