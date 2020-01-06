import json
import hashlib
import socket
import os
from subprocess import call, Popen, PIPE
import time
import logging
import configparser
import os
from .common.helper import check_file_exit, check_item_trigger_exist, http_post

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


class ZabbixApi():

    def __init__(self, auth_username, auth_password, api_url):
        self.auth_username= auth_username
        self.auth_password = auth_password
        self.api_url = api_url
        self._key = None

    def loging(self, zabbix_user, zabbix_passowrd):
        """ Log in to the API and generate an authentication token """
        
        data = {
            "jsonrpc": "2.0",
            "method": "user.login",
            "params": {
                "user": zabbix_user,
                "password": zabbix_passowrd
            },
            "id": 1,
            "auth": None
        }
        logger.info('Log in to the API')
        logger.debug('Requests: %s'%(data))
        res = http_post(self.api_url, data, self.auth_username, self.auth_password)
        logger.debug('Response: %s'%(res.json()))
        self.auth = res.json()['result']
        logger.info('Get authentication token %s'%(self.auth))

    def logout(self):
        """ Log out to the API """

        data = {
            "jsonrpc": "2.0",
            "method": "user.logout",
            "params": [],
            "id": 1,
            "auth": self.auth
        }
        logger.info('Log out to the API')
        logger.debug('Requests: %s'%(data))
        res = http_post(self.api_url, data, self.auth_username, self.auth_password)
        logger.debug('Response: %s'%(res.json()))


    def create_item(self, hostid, item_name, item_type=2, item_value_type=3):
        """
        CREATE THE ITEM
        ----------------------------
        hostid get from config file
        Default item type is trappter
        Default value type is integer
        Gernerate item key by hash the item name
        
        Document: https://www.zabbix.com/documentation/3.2/manual/api/reference/item/create
        """

        self.key = hashlib.md5(item_name.encode('utf-8')).hexdigest()

        data = {
            "jsonrpc": "2.0",
            "method": "item.create",
            "params": {
                "name": item_name,
                "key_": self.key,
                "hostid": hostid,
                "type": item_type,
                "value_type": item_value_type,
            },
            "auth": self.auth,
            "id": 1
        }
        logger.info('Create new item')
        logger.debug('Requests: %s'%(data))
        res = http_post(self.api_url, data, self.auth_username, self.auth_password)
        logger.debug('Response: %s'%(res.json()))
        check_item_trigger_exist(res)        

    def create_trigger(self, hostname,_description, tags):
        """
        CREATE THE TRIGGER
        -----------------------
        hostname is get from config file
        expression:
            - if last value is equal 1 -> Trigger is being activation
        tags is the strings, and will be convert into list

        """

        logger.info('Create the trigger')
        tags = tags.split(',')
        generate_dict_tags = []
        for tag in tags:    
            generate_dict_tags.append({"tag": tag.strip(), "value": ""})
        logger.debug('Tags: %s'%(generate_dict_tags))
        expression_format = "{%s:%s.last()}=1"%(hostname,self.key)
        data = {
            "jsonrpc": "2.0",
            "method": "trigger.create",
            "params": [
                {                    
                    "description": _description,
                    "expression": expression_format,
                    "priority": 4,
                    "tags": generate_dict_tags
                },
              ],     
            "auth": self.auth,
            "id": 1
        }
        logger.debug('Requests: %s'%(data))
        res = http_post(self.api_url, data, self.auth_username, self.auth_password)
        check_item_trigger_exist(res)

    def sender(self,zabbix_server, zabbix_port, host, value):
        """
        Send value to Zabbix server via Zabbi Trapper
        """
        logger.info('Send value to Zabbix server')
        zabbix_sender = config['zabbix_server']['zabbix_sender']
        if not check_file_exit(zabbix_sender):
            logger.error('File not found %s'%(zabbix_server))
        else:
            cmd = "{zabbix_sender} -z {zabbix_server} -s {host} -p {zabbix_port} -k {key} -o {value}".format(
                zabbix_sender=zabbix_sender,
                zabbix_server=zabbix_server,
                host=host,
                zabbix_port=zabbix_port,
                key=self.key,
                value=value
                )
            
            logger.debug(cmd)

            counter = 0
            while True:
                p = Popen(cmd, shell=True, stdout=PIPE, stderr=PIPE)
                (stdout, stderr) = p.communicate()
                exit_code = p.returncode
                if exit_code == 0:
                    logger.info("Success")
                    logger.debug(stdout)
                    break
                else:
                    counter += 1
                    if counter == 65:
                        logger.error("Unable to push value to zabbix server")
                        break
                    logger.warning("Push value faild, retry[{}]".format(counter))
                    logger.warning("Exit code: ",exit_code)
                    logger.warning("Stdout: ",stdout)
                    logger.warning("Stderr: ",stderr)
                    time.sleep(1)


