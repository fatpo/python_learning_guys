import requests

if __name__ == '__main__':
    ret = requests.get("https://www.baidu.com")
    print(ret.content)
    # 存到html文件中
    with open("tmp_baidu.html", "wb") as f:
        f.write(ret.content)
