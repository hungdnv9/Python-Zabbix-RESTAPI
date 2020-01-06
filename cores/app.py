from flask import Flask, render_template, request, redirect, url_for, jsonify
import configparser
from .zabbix_api import ZabbixApi
import time
from .common.token_helper import vertify_token
import logging

app = Flask(__name__)

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


# LOAD DATA
Data_Backend = {
    "username": config['Backend']['username'],
    "password": config['Backend']['password'],
    "hostname": config['Backend']['hostname'],
    "hostid": config['Backend']['hostid'],
    "token": config['Backend']['token'],
}

Data_System = {
    "username": config['System']['username'],
    "password": config['System']['password'],
    "hostname": config['System']['hostname'],
    "hostid": config['System']['hostid'],
    "token": config['System']['token'],
}

Data_Database = {
    "username": config['Database']['username'],
    "password": config['Database']['password'],
    "hostname": config['Database']['hostname'],
    "hostid": config['Database']['hostid'],
    "token": config['Database']['token'],
}

Data_Frontend = {
    "username": config['Frontend']['username'],
    "password": config['Frontend']['password'],
    "hostname": config['Frontend']['hostname'],
    "hostid": config['Frontend']['hostid'],
    "token": config['Frontend']['token'],
}


# LIST ACCEPT TOKENS
accept_tokens = [
    config['Backend']['token'],  # -> INDEX 0
    config['Database']['token'], # -> INDEX 1
    config['Frontend']['token'], # -> INDEX 2
    config['System']['token']    # -> INDEX 3 
]


def get_data_by_token_index(token_id):
    if token_id == 0:
        return Data_Backend
    if token_id == 1:
        return Data_Database
    if token_id == 2:
        return Data_Frontend
    if token_id == 3:
        return Data_System




def append_new(token, message, value, tags):
    data_dict = {"token": token, "message": message, "value": value, "tags": tags}

  
    if vertify_token(token, accept_tokens) is False:
        alert = "Invaild token"
        logger.error(alert)
        return alert

    else:
        logger.info('Token[%s] is valid'%(token))
               
        # INIT ZABBIX CONSTRUCT
        api_url = config['zabbix_server']['api_url']
        auth_username = config['http_authen']['username']
        auth_password = config['http_authen']['password']
        z = ZabbixApi(auth_username, auth_password, api_url)
        # LOGING ZABBIX
        token_id = accept_tokens.index(token)
        data =  get_data_by_token_index(token_id)
        zb_username = data['username']
        zb_password = data['password']
        z.loging(zb_username, zb_password)
        
        # CREATE ITEM
        hostid = data['hostid']
        z.create_item(hostid, message)
       
        # CREATE TRIGGER
        hostname = data['hostname']
        z.create_trigger(hostname, message, tags)
        
        # LOGOUT
        z.logout()
       
        # PUSH VALUE
        zb_server = config['zabbix_server']['ip']
        zb_port = config['zabbix_server']['port']
        z.sender(zb_server, zb_port, hostname, value)
        return data_dict


@app.route('/')
@app.route('/v1/api', methods=['GET', 'POST'])
def msgFunction():
    if request.method == 'POST':
        data = request.get_json()
        token = data['token']
        message = data['message']
        value = data['value']
        tags = data['tags']
        return append_new(token, message, value, tags)
        

