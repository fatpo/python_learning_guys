import json
import time
import requests
from flask import Flask
from flask import jsonify
from flask import request

app = Flask(__name__)
database_api_url = r'http://my.app.com/core/api/search/'


def get_db_from_code(code):
    """
    根据 某个 code，比如 "04"，返回具体点数据库类型： db2，如果是 08，那么就要返回 db3
    :param code: 某个 code
    :return: 某个 db
    """
    DATABASE_CODE_DICT = {
        'db1': ['01', '02'],
        'db2': ['03', '04', '05'],
        'db3': ['06', '07', '08', '09']
    }

    for k, v in DATABASE_CODE_DICT.items():  # 字典的遍历
        # k 是？ v 是？
        # k: db1, v: ['01', '02']
        # k: db2, v: ['03', '04', '05']
        # k: db3, v: ['06', '07', '08', '09']

        for _code in v:  # 列表的遍历，遍历  ['03', '04', '05']这个列表
            if code == _code:
                return k
    return None


# 构造请求头
headers = {'"Content-Type': 'application/json', 'Authorization': 'eips_token %s'}

# 获取要查询的DB
db = ""


@app.route('/my_test_api/', methods=['post'])
def query():
    # 全局变量
    global headers

    # 全局变量
    global db

    # 参数校验
    data = request.json  # dict

    # app.logger 是 flask 框架自带的日志处理，你可以直接用 app.logger.info("xx"), app.logger.error("mm"), app.logger.debug("yy")
    app.logger.error("请求参数:%s" % json.dumps(data))

    param1 = data.get('param1')
    param2 = data.get('param2')
    if not param1:
        return jsonify({"code": "-1", "msg": "no param1"})
    if not param2:
        return jsonify({"code": "-1", "msg": "no param2"})

    # 构造请求头 some_token 是我们内部要的 token 入参，写在请求的 headers 中
    headers = {'"Content-Type': 'application/json', 'Authorization': 'some_token %s' % param2}

    # 获取要查询的DB，因为有很多个 DB，要根据入参的第 1到 3 个字符串，判断属于第几个 DB
    db = get_db_from_code(param1[1:3])
    return step0(param1)


def step0(param1):
    app.logger.error("######################### step0 #########################")
    # 组建一个 sql
    sql = f""" select * from table_1 where param1 = '{param1}'"""

    # 去数据库拿这个 sql 的结果
    res = getDBData(sql)

    # 如果没有结果，就直接返回某句话：状态停效
    if not isHasResult(res):
        return warpReturnMsg("状态停效。")

    # 能走到这一步，说明是有结果的，判断结果的某个状态是不是 A
    sts = res['rows'][0]['STS']
    if sts == 'A':
        return warpReturnMsg("有效状态了。")

    # 能走到这一步，说明是有结果的，判断结果的某个状态是不是 I, L
    if sts in ['I', 'L']:
        return step1(param1)
    else:
        return warpReturnMsg(f"原因不明，请报IT应用系统问题咨询。")


def step1(param1):
    app.logger.error("######################### step1 #########################")
    sql = f"""select * from table_2 where param1 = '{param1}'"""
    res = getDBData(sql)
    if isHasResult(res):
        # app.logger.error("有数据，订单有效。")
        # return json.dumps({'message':"有数据，订单有效。"})
        return warpReturnMsg("有数据，订单有效。")
    else:
        return warpReturnMsg("没数据，订单无效。")


def warpReturnMsg(msg):
    """
    包装下返回值，顺便打印
    :param msg:
    :return:
    """
    app.logger.error("message:%s" % msg)
    return json.dumps({'message': msg})


def isHasResult(res):
    """
    判断一个DB的返回值是否有数据
    :param res:
    :return:
    """
    if not res:
        return False

    if ('success' not in res or res["success"] == False) or ('rowcount' not in res or res["rowcount"] == 0):
        return False

    return True


def getDBData(sql):
    """
    我们当初的 sql 都是发到某个服务器去查询的，不是直接操作数据库，这个地址是 http://my.app.com/core/api/search/

    这里就用到了 request 这个高频的轮子

    :param sql:
    :return:
    """
    params = dict()  # 初始化一个字典，和 my_list = list() 初始化一个列表 一样的
    params['db'] = db  # 放键值对 "db"=db2
    params['sql'] = sql  # 放键值对 "sql"="select xxx"

    res = requests.post(url=database_api_url, headers=headers, json=params)
    if res:
        app.logger.error("db content:%s" % res.content)
        try:
            res = res.json()
        except Exception as ex:
            app.logger.error(ex)
            return None

        app.logger.error("db查询:%s" % params['sql'].encode("utf-8"))
        app.logger.error("db查询返回:%s" % res)
        return res
    else:
        return None


def get_days_between(day1: str, day2: str):
    """
    获取两个日期之间的间隔了多少天，比如2022-07-01 和 2022-07-20，间隔了 19 天
    :param day1: 日期 1
    :param day2: 日期 2
    :return: 两个日期之间的间隔的天数
    """
    # 把 str 格式的日期 转成 time 类型 的日期
    time_array1 = time.strptime(day1, "%Y-%m-%d")

    # time 类型的日期 -> 转成时间戳：就是从 1970 年7 月 1 号到此时此刻，一共度过了多少秒
    timestamp_day1 = int(time.mktime(time_array1))

    # 把 str 格式的日期 转成 time 类型 的日期，day2 可能有点小特殊，它格式不一定是"%Y-%m-%d"，还可能是"%Y-%m-%d %H:%M:%S"
    if ":" in day2:
        time_array2 = time.strptime(day2, "%Y-%m-%d %H:%M:%S")
    else:
        time_array2 = time.strptime(day2, "%Y-%m-%d")

    # time 类型的日期 -> 转成时间戳：就是从 1970 年7 月 1 号到此时此刻，一共度过了多少秒
    timestamp_day2 = int(time.mktime(time_array2))

    # 两个秒数相减后，除以 一天 86400 秒，就是间隔了多少天
    result = (timestamp_day2 - timestamp_day1) // 60 // 60 // 24
    return result


if __name__ == '__main__':
    # 创建一个服务器
    app.run(host='0.0.0.0', port=8893)
