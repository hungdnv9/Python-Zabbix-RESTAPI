# Simple Zabbix REST API by using Pythn3 Flask and Zabbix API
```sh
WARRNING: This project just for my self learning. If you want to setup in your system, plz be carefull.
Support auto create item, trigger and push value to zabbix server via REST API.
Requirements: You have a lot of experence with Zabbix and Python script. If you want some detail, please contact me by email hungdnv9@gmail.com. Thanks
```
## Setup enviroment
```sh
/build/python3/bin/pyvenv env
. env/bin/activate
pip install -r requirements.txt
```
## REST API
```sh
/bin/curl -X POST -H "Content-Type: application/json" -d '{"token":"2c67020a8133a17b4763518ee77abb77", "message":"Just test msg, created by system", "value": "123", "tags": "system"}' -u "user":"password" https://zabbix-domain.com/v1/api
```
## Output
```sh
2020-01-06 16:15:55,488 - loging - INFO - Log in to the API
2020-01-06 16:15:55,488 - loging - DEBUG - Requests: {'jsonrpc': '2.0', 'method': 'user.login', 'params': {'user': 'api_system', 'password': 'gU7BhFB'}, 'id': 1, 'auth': None}
2020-01-06 16:15:55,684 - loging - DEBUG - Response: {'jsonrpc': '2.0', 'result': 'a22ee6157aea48cfca20eef0cea2fe8e', 'id': 1}
2020-01-06 16:15:55,684 - loging - INFO - Get authentication token a22ee6157aea48cfca20eef0cea2fe8e
2020-01-06 16:15:55,684 - create_item - INFO - Create new item
2020-01-06 16:15:55,684 - create_item - DEBUG - Requests: {'jsonrpc': '2.0', 'method': 'item.create', 'params': {'name': 'SE 12313 | Just test msg, created by system', 'key_': '8e417be4498e9ff2d5263d23de1fa0ae', 'hostid': '10386', 'type': 2, 'value_type': 3}, 'auth': 'a22ee6157aea48cfca20eef0cea2fe8e', 'id': 1}
2020-01-06 16:15:55,951 - create_item - DEBUG - Response: {'jsonrpc': '2.0', 'result': {'itemids': ['52629']}, 'id': 1}
2020-01-06 16:15:55,951 - create_trigger - INFO - Create the trigger
2020-01-06 16:15:55,952 - create_trigger - DEBUG - Tags: [{'tag': 'system', 'value': ''}]
2020-01-06 16:15:55,952 - create_trigger - DEBUG - Requests: {'jsonrpc': '2.0', 'method': 'trigger.create', 'params': [{'description': 'SE 12313 | Just test msg, created by system', 'expression': '{ZBAPI-System:8e417be4498e9ff2d5263d23de1fa0ae.last()}=1', 'priority': 4, 'tags': [{'tag': 'system', 'value': ''}]}], 'auth': 'a22ee6157aea48cfca20eef0cea2fe8e', 'id': 1}
2020-01-06 16:15:56,204 - logout - INFO - Log out to the API
2020-01-06 16:15:56,204 - logout - DEBUG - Requests: {'jsonrpc': '2.0', 'method': 'user.logout', 'params': [], 'id': 1, 'auth': 'a22ee6157aea48cfca20eef0cea2fe8e'}
2020-01-06 16:15:56,307 - logout - DEBUG - Response: {'jsonrpc': '2.0', 'result': True, 'id': 1}
2020-01-06 16:15:56,307 - sender - INFO - Send value to Zabbix server
2020-01-06 16:15:56,307 - sender - DEBUG - /build/zabbix/bin/zabbix_sender -z 10.199.0.110 -s ZBAPI-System -p 10051 -k 8e417be4498e9ff2d5263d23de1fa0ae -o 123
2020-01-06 16:15:56,314 - sender - WARNING - Push value faild, retry[1]
2020-01-06 16:15:57,331 - sender - WARNING - Push value faild, retry[2]
2020-01-06 16:15:58,344 - sender - WARNING - Push value faild, retry[3]
2020-01-06 16:15:59,356 - sender - WARNING - Push value faild, retry[4]
2020-01-06 16:16:00,368 - sender - WARNING - Push value faild, retry[5]
2020-01-06 16:16:01,381 - sender - WARNING - Push value faild, retry[6]
2020-01-06 16:16:02,395 - sender - WARNING - Push value faild, retry[7]
2020-01-06 16:16:03,408 - sender - WARNING - Push value faild, retry[8]
2020-01-06 16:16:04,427 - sender - WARNING - Push value faild, retry[9]
2020-01-06 16:16:05,446 - sender - WARNING - Push value faild, retry[10]
2020-01-06 16:16:06,499 - sender - WARNING - Push value faild, retry[11]
2020-01-06 16:16:07,556 - sender - WARNING - Push value faild, retry[12]
2020-01-06 16:16:08,592 - sender - WARNING - Push value faild, retry[13]
2020-01-06 16:16:09,646 - sender - WARNING - Push value faild, retry[14]
2020-01-06 16:16:10,665 - sender - WARNING - Push value faild, retry[15]
2020-01-06 16:16:11,689 - sender - WARNING - Push value faild, retry[16]
2020-01-06 16:16:12,737 - sender - WARNING - Push value faild, retry[17]
2020-01-06 16:16:13,782 - sender - WARNING - Push value faild, retry[18]
2020-01-06 16:16:14,818 - sender - WARNING - Push value faild, retry[19]
2020-01-06 16:16:15,838 - sender - WARNING - Push value faild, retry[20]
2020-01-06 16:16:16,852 - sender - WARNING - Push value faild, retry[21]
2020-01-06 16:16:17,878 - sender - WARNING - Push value faild, retry[22]
2020-01-06 16:16:18,897 - sender - WARNING - Push value faild, retry[23]
2020-01-06 16:16:19,912 - sender - WARNING - Push value faild, retry[24]
2020-01-06 16:16:20,931 - sender - WARNING - Push value faild, retry[25]
2020-01-06 16:16:21,945 - sender - WARNING - Push value faild, retry[26]
2020-01-06 16:16:22,959 - sender - WARNING - Push value faild, retry[27]
2020-01-06 16:16:23,973 - sender - WARNING - Push value faild, retry[28]
2020-01-06 16:16:24,988 - sender - WARNING - Push value faild, retry[29]
2020-01-06 16:16:26,003 - sender - WARNING - Push value faild, retry[30]
2020-01-06 16:16:27,015 - sender - WARNING - Push value faild, retry[31]
2020-01-06 16:16:28,030 - sender - WARNING - Push value faild, retry[32]
2020-01-06 16:16:29,044 - sender - WARNING - Push value faild, retry[33]
2020-01-06 16:16:30,058 - sender - WARNING - Push value faild, retry[34]
2020-01-06 16:16:31,070 - sender - WARNING - Push value faild, retry[35]
2020-01-06 16:16:32,084 - sender - WARNING - Push value faild, retry[36]
2020-01-06 16:16:33,098 - sender - WARNING - Push value faild, retry[37]
2020-01-06 16:16:34,112 - sender - WARNING - Push value faild, retry[38]
2020-01-06 16:16:35,125 - sender - WARNING - Push value faild, retry[39]
2020-01-06 16:16:36,138 - sender - WARNING - Push value faild, retry[40]
2020-01-06 16:16:37,151 - sender - WARNING - Push value faild, retry[41]
2020-01-06 16:16:38,162 - sender - WARNING - Push value faild, retry[42]
2020-01-06 16:16:39,174 - sender - WARNING - Push value faild, retry[43]
2020-01-06 16:16:40,188 - sender - WARNING - Push value faild, retry[44]
2020-01-06 16:16:41,203 - sender - WARNING - Push value faild, retry[45]
2020-01-06 16:16:42,216 - sender - WARNING - Push value faild, retry[46]
2020-01-06 16:16:43,228 - sender - WARNING - Push value faild, retry[47]
2020-01-06 16:16:44,240 - sender - WARNING - Push value faild, retry[48]
2020-01-06 16:16:45,253 - sender - WARNING - Push value faild, retry[49]
2020-01-06 16:16:46,266 - sender - WARNING - Push value faild, retry[50]
2020-01-06 16:16:47,277 - sender - WARNING - Push value faild, retry[51]
2020-01-06 16:16:48,289 - sender - WARNING - Push value faild, retry[52]
2020-01-06 16:16:49,301 - sender - WARNING - Push value faild, retry[53]
2020-01-06 16:16:50,314 - sender - WARNING - Push value faild, retry[54]
2020-01-06 16:16:51,329 - sender - WARNING - Push value faild, retry[55]
2020-01-06 16:16:52,342 - sender - WARNING - Push value faild, retry[56]
2020-01-06 16:16:53,358 - sender - WARNING - Push value faild, retry[57]
2020-01-06 16:16:54,370 - sender - INFO - Success
2020-01-06 16:16:54,370 - sender - DEBUG - b'info from server: "processed: 1; failed: 0; total: 1; seconds spent: 0.000181"\nsent: 1; skipped: 0; total: 1\n'

```

![alt text](https://github.com/hungdnv9/Python-Zabbix-RESTAPI/blob/master/docs/item.png)

![alt text](https://github.com/hungdnv9/Python-Zabbix-RESTAPI/blob/master/docs/trigger.png)
