import requests
import json


url = "http://127.0.0.1:9000/admin/posts/1"

try:
    response = requests.request('DELETE', url)
    if response.status_code == 200:
        print("请求成功，响应内容如下：".format(json.loads(response.text)))
    else:
        print("请求失败，状态码：{}，响应内容：{}".format(response.status_code, json.loads(response.text)))

except requests.exceptions.RequestException as e:
    print("请求过程中出现错误：{}".format(e))
    