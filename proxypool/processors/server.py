from flask import Flask, g, request, jsonify
from proxypool.storages.redis import RedisClient
from proxypool.setting import API_HOST, API_PORT, API_THREADED, IS_DEV
import pymysql
from loguru import logger

H_TAG = 'ABZL*CT052YEUSOK'

__all__ = ['app']

app = Flask(__name__)
if IS_DEV:
    app.debug = True

SELECT_ONCE_ADDR = """
SELECT * FROM `mmzztt_all_page_note` WHERE get_count = %s LIMIT 1
"""


def get_conn():
    """
    get redis client object
    :return:
    """
    if not hasattr(g, 'redis'):
        g.redis = RedisClient()
    return g.redis


def get_mysql_conn():
    if not hasattr(g, 'mysql'):
        g.mysql = pymysql.connect(
            host="81.70.149.97",
            user="sunjianfeng",
            password="558Sjf...",
            database='tools',
            port=4300,
            charset='utf8',
            autocommit=True,
            cursorclass=pymysql.cursors.DictCursor
        )
    return g.mysql


@app.route('/')
def index():
    """
    get home page, you can define your own templates
    :return:
    """
    return '<h2>Welcome to Proxy Pool System</h2>'


@app.route('/random')
def get_proxy():
    """
    get a random proxy
    :return: get a random proxy
    """
    conn = get_conn()
    return conn.random().string()


@app.route('/all')
def get_proxy_all():
    """
    get a random proxy
    :return: get a random proxy
    """
    conn = get_conn()
    proxies = conn.all()
    proxies_string = ''
    if proxies:
        for proxy in proxies:
            proxies_string += str(proxy) + '\n'

    return proxies_string


@app.route('/count')
def get_count():
    """
    get the count of proxies
    :return: count, int
    """
    conn = get_conn()
    return str(conn.count())


@app.route('/getOnceEntry')
def get_mmzztt_page():
    conn = get_mysql_conn()
    tag = request.args.get('tag')
    if tag == H_TAG:
        try:
            with conn.cursor() as cursor:
                cursor.execute(SELECT_ONCE_ADDR, 0)
                data = cursor.fetchall()
                logger.info(f'get info {data} ')
                cursor.close()
                return jsonify(data)
        except pymysql.MySQLError as err:
            print("数据库嗝屁了！～")
            print(err)
    return '^-^'


@app.route('/registerEntryOnce', methods=["POST"])
def update_register_ertry_once():
    conn = get_mysql_conn()
    id = request.body.id
    tag = request.body.tag
    if tag == H_TAG:
        print(id)
        try:
            with conn.cursor() as cursor:
                get_once = cursor.execute(SELECT_ONCE_ADDR, 0)
        except pymysql.MySQLError as err:
            print("数据库嗝屁了！～")
            print(err)
        return ''
    else:
        return '^-^'


if __name__ == '__main__':
    app.run(host=API_HOST, port=API_PORT, threaded=False)
