import requests
import json


url = "http://127.0.0.1:9000/posts/"

 
headers = {
    "Content-Type": "application/json"
}  

params = {
    "title": "安江二完小, 秋季运动会",
    "content": "正式开幕...",
    "user_id": 1
}

try:
    response = requests.request('POST', url, headers=headers, data=json.dumps(params))
    if response.status_code == 200:
        print("请求成功，响应内容如下：".format(json.loads(response.text)))
    else:
        print("请求失败，状态码：{}，响应内容：{}".format(response.status_code, json.loads(response.text)))

except requests.exceptions.RequestException as e:
    print("请求过程中出现错误：{}".format(e))
    
    