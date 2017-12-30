import json
import time
import itertools
import os
import sys
from influxdb import InfluxDBClient
from .nibeapi import NibeApi

_CONFIG_DIR  = sys.prefix+'/etc/nibe2influx/'
_CONFIG_FILE = _CONFIG_DIR+'config.json'
_SENSOR_FILE = _CONFIG_DIR+'sensors.json'
_TOKEN_FILE  = _CONFIG_DIR+'token.json'

class InfluxDatabase():

    def __init__(self, conf):
        addr = conf['addr']
        port = conf['port']
        self.dbname = conf['dbname']
        
        self.client = InfluxDBClient(addr, port)
        self.client.create_database(self.dbname)

    def persist(self, measurement):
        self.client.write_points(measurement, database=self.dbname)


def update_measurement(measurements, sensors, apiresp):
    for i in range(len(apiresp)):
        if sensors[i]['id'] != apiresp[i]['parameterId']:
            return False

        raw_value = float(apiresp[i]['rawValue'])
        scale = float(sensors[i]['scale'])
        value = raw_value*scale

        measurements[i]['fields']['value'] = value

    return True

def config_template():
    template = {
        "nibeapi" : {
            "client" : {
                "client_id":"",
                "client_secret":""
            },
            "system_id" : 1234,
            "update_interval_seconds" : 30,
            "redirect_uri" : ""
        },

        "influx" : {
            "addr"   : "127.0.0.1",
            "port"   : 8086,
            "dbname" : "nibe"
        }
    }
    with open(_CONFIG_FILE, 'w') as cf:
        json.dump(template, cf, indent=4)

def sensor_template():
    template = {
        "measurement1": [
            {"id" : 1234, "scale":0.1, "tags":{
                "name1": "value1",
                "name2": "value2",
            }},
            {"id" : 4321, "scale":1, "tags":{
                "name1": "value1",
                "name2": "value2",
            }}
        ],
        "measurement2": [
            {"id" : 1234, "scale":0.1, "tags":{
                "name1": "value1",
                "name2": "value2",
            }},
            {"id" : 4321, "scale":1, "tags":{
                "name1": "value1",
                "name2": "value2",
            }}
        ]
    }
    with open(_SENSOR_FILE, 'w') as sf:
        json.dump(template, sf, indent=4)


def config_files():
    config_ok = True

    # Check config dir
    if not os.path.isdir(_CONFIG_DIR):
        try:
            os.makedirs(_CONFIG_DIR)
            print('Created {}'.format(_CONFIG_DIR))
        except:
            print('ERROR: Could not create {}'.format(_CONFIG_DIR))

    # Check config file
    try:
        with open(_CONFIG_FILE) as cf:
            conf = json.load(cf)
    except:
        print('{} not found. Creating template.'.format(_CONFIG_FILE))
        config_template()
        config_ok = False

    try:
        with open(_SENSOR_FILE) as sf:
            sensors = json.load(sf)
    except:
        print('{} not found. Creating template.'.format(_SENSOR_FILE))
        sensor_template()
        config_ok = False

    if config_ok:
        return conf, sensors
    else:
        print('Update templates with proper data before running the application.')
        exit(0)


def main(db=None):

    conf, sensors = config_files()

    idlists={}
    measurements={}
    
    for group in sensors:
        # Generate list of IDs as required by Nibe API.
        idlists[group] = [sensor['id'] for sensor in sensors[group]]
        
        measurements[group] = []
        # Generate structure required by InfluxDB.
        for sensor in sensors[group]:
            measurements[group].append({'measurement':group, 'fields':{'value':''}, 'tags':sensor['tags']})

    update_interval = conf['nibeapi']['update_interval_seconds']
    api = NibeApi(conf['nibeapi'], _TOKEN_FILE)
    
    if db is None:
        db = InfluxDatabase(conf['influx'])

    for m in itertools.cycle(measurements):
        apiresp = api.get_parameters(idlists[m])

        if update_measurement(measurements[m], sensors[m], apiresp):
            db.persist(measurements[m])
        else:
            print('ERROR: api returndata mismatch')
            exit(1)

        time.sleep(update_interval)
