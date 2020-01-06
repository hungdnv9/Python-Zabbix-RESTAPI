import os
import logging
import configparser
import json
import requests
from requests.auth import HTTPBasicAuth


# LOAD CONFIG FILE
config_file = '/data/www/public_html/v2.api.zabbix.adx.vn/cores/data/zabbix_config.ini'
config = configparser.RawConfigParser()
config.read(config_file)

# SETTING LOGGER 
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
f_handler = logging.FileHandler(config['Log']['file'])
f_format = logging.Formatter('%(asctime)s - %(funcName)s - %(levelname)s - %(message)s')
f_handler.setFormatter(f_format)
logger.addHandler(f_handler)


def check_file_exit(file):  
    if os.path.isfile(file):
        return  True
    else:
        return False

def check_item_trigger_exist(response):
    """ If item or trigger is existing, raise alert """
    if 'error' in response.json():
        if 'already exists' in response.json()['error']['data']:
            logger.warning(response.json()['error']['data'])
        else:
            logger.error(response.json()['error']['data'])


def http_post(url, data, user_authen, password_authen):

    headers = {
        'content-type': 'application/json',
    }

    response = requests.post(url, data=json.dumps(data), headers=headers, auth=HTTPBasicAuth(user_authen, password_authen))
    return response  

