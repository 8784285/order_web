#coding:utf-8
__author__ = 'Mr. null'

from flask import Flask, request, jsonify, Response
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, BadSignature, SignatureExpired
import json
import logging
import pymysql.connections as db_connection
import pymysql.cursors
from flask_cors import CORS
# pip install flask_httpauth
from flask_httpauth import HTTPTokenAuth
auth = HTTPTokenAuth() #默认是Bearer类型， 带上headers的Authorization : Bearer token

#flask-restful中增加的装饰器
decorators = [auth.login_required]
app = Flask(__name__)
app.config["SECRET_KEY"] = "test1234567"
# pip3 install Flask-Cors
CORS(app, supports_credentials=True)  # 设置跨域

# _db = MySQLdb.connect(host="localhost",user="root",passwd="root",db="apitest",charset="utf8")
# _cursor = None
# _db = db_connection.Connection(host="localhost", port=3306,
#                                                user="root", password="sprintuu",
#                                               database="apitest", charset='utf8', init_command='SET NAMES UTF8')
# _cursor = _db.cursor(pymysql.cursors.DictCursor)


def create_token(username,password):
    """创建token令牌"""
    s = Serializer(app.config["SECRET_KEY"],expires_in = 24 * 3600)
    token = s.dumps({"username":username,"password":password})
    print(token)
    return token

@auth.verify_token
def verify_token(token):
    """校验token"""
    s = Serializer(app.config["SECRET_KEY"], expires_in=24 * 3600)
    try:
        data = s.loads(token)
    except SignatureExpired:
        # token正确但是过期了
        return False
    except BadSignature:
        # token错误
        return False
    user = data['username']
    return True

@auth.error_handler
def error_handler():
    return jsonify(code=401, message='401 未授权')


@app.route('/login',methods= ["POST"])
def login():
    data = json.loads(request.get_data(as_text=True))
    print(data)
    in_username = data['username']
    in_password = data['password']
    sql = "SELECT * FROM users WHERE name = '%s' AND password = '%s'"%(in_username, in_password)
    print(sql)
    dbservice = DBService()
    try:
        rows = dbservice.exec_with_return(sql)
        if rows:
            token = create_token(in_username,in_password)
            print(token)
            print(sql)
            is_admin = False
            if in_username == 'admin':
                is_admin = True
            return jsonify(code=4,msg="登录成功",token=token.decode(), is_admin=is_admin)
        else:
            return jsonify(code=2,msg="非法用户")
    except Exception as ex:
        return jsonify(code=400, msg="异常" + str(ex))
    finally:
        dbservice.close_connect()

@app.route('/register',methods= ["POST"])
def register():
    data = json.loads(request.get_data(as_text=True))
    print(data)
    in_username = data['username']
    in_password = data['password']
    dbservice = DBService()
    try:
        sql = "insert into users(name,password) values('%s', '%s')"%(in_username, in_password)
        print(sql)
        dbservice.exec_and_commit(sql)
        uid = dbservice.get_cursor().lastrowid
        print('uid:',uid)
        sql = "insert into userinfo(IDCard,Phone,Address,id) values('%s','%s','%s',%s)" % (data['idCard'], data['phone'], data['address'], uid)
        print(sql)
        dbservice.exec_and_commit(sql)
        return jsonify(code=4, msg="注册成功")
    except Exception as ex:
        logging.error("", ex)
        return jsonify(code=5, msg="注册失败")
    finally:
        dbservice.close_connect()


#=============商品信息===================
@app.route('/add_product',methods=['POST'])
@auth.login_required
def add_product():
    # j_data = json.loads(request.get_data())
    j_data = request.form.to_dict()
    name = j_data['name']
    price = j_data['price']
    count = j_data['count']
    dbservice = DBService()
    try:
        stock_sql = "insert into stock(name,price,count,sale,version) VALUES ('%s',%s,%s,0,1) " % (name,float(price),int(count))
        dbservice.exec_and_commit(stock_sql)
        #return u'商品添加成功：' +name+ '，'+str(price)+ '，'+ str(count)
        return jsonify(code = 2001, msg = "商品添加成功")
    except Exception:
        return jsonify(code = 2002, msg = "商品添加失败", sql = stock_sql)
    finally:
        dbservice.close_connect()

@app.route('/get_product',methods= ["GET"])
def get_product():
    """获取商品列表"""
    productid = request.args.get("productid")
    name = request.args.get("name")
    if productid != None and name == None:
        sql = "SELECT id,name,price,count FROM stock WHERE id = %d "%(int(productid))
    elif productid == None and name != None:
        sql = "SELECT id,name,price,count FROM stock WHERE name = '%d' order by id desc limit 20" % (name)
    else:
        sql = "SELECT id,name,price,count FROM stock order by id desc limit 20"
    print(sql)
    dbservice = DBService()
    try:
        rows = dbservice.exec_with_return(sql)
        if rows:
            data = dbservice.get_cursor().fetchall()
            # result = dict(zip(('name', 'count', 'price'), data[0]))
            return jsonify(code=5, msg="查询成功", data=data)
        else:
            return jsonify(code=6, msg="未查询到数据", sql=sql)
    except Exception as ex:
        return jsonify(code=400, msg="异常" + str(ex))
    finally:
        dbservice.close_connect()

@app.route('/get_product_detail/<productid>',methods= ["GET"])
def get_product_detail(productid=None):
    """获取商品详情"""
    sql = "SELECT id,name,price,count FROM stock where id = '%s'" % (int(productid))
    print(sql)
    dbservice = DBService()
    try:
        rows = dbservice.exec_with_return(sql)
        if rows:
            data = dbservice.get_cursor().fetchall()
            print(data)
            result = dict(zip(('id', 'name', 'price', 'count'), data[0]))
            return jsonify(code = 5, msg = "查询成功", data = result)
        else:
            return jsonify(code = 6, msg = "未查询到数据", sql = sql)
    except Exception as ex:
        return jsonify(code=6, msg="异常" + str(ex))
    finally:
        dbservice.close_connect()

@app.route('/add_order',methods=['POST'])
@auth.login_required
def add_order():
    j_data = json.loads(request.get_data())
    print(j_data)
    sid = j_data['sid']
    orderprice = j_data['orderprice']
    # username = j_data['username']
    token = request.headers['Authorization']
    username = get_username(token[len('Bearer '):])
    receiver = j_data['receiver']
    phone = j_data['phone']
    address = j_data['address']
    checkstock_sql = "SELECT count FROM stock WHERE id = %d"%(int(sid))
    print(checkstock_sql)
    dbservice = DBService()
    try:
        checkstock_result = dbservice.exec_with_return(checkstock_sql)
        data = dbservice.get_cursor().fetchone()
        if data[0] > 0:
            try:
                order_sql = "insert into stock_order(sid,orderprice,username,receiver,phone,address) VALUES (%d,%f,'%s','%s','%s','%s')" % (int(sid),float(orderprice),username,receiver,phone,address)
                stock_sql = "update stock set count = count - 1 where id = %d" %(int(sid))
                print(order_sql)
                print(stock_sql)
                dbservice.exec_and_commit(order_sql)
                order_id = dbservice.get_cursor().lastrowid
                dbservice.exec_and_commit(stock_sql)
                return jsonify(code = 2003, msg = "创建订单成功", order_id = order_id)
            except Exception:
                return jsonify(code = 2004, msg = "创建订单失败", data = order_sql)
        else:
            return jsonify(code = 2005, msg = "库存不足", data = data[0])
    except Exception as e:
        return jsonify(code=2006, msg="抛异常了", data=e)
    finally:
        dbservice.close_connect()

@app.route('/update_order',methods= ["POST"])
@auth.login_required
def update_order():
    j_data = json.loads(request.get_data())
    print(j_data)
    order_id = j_data['order_id']
    token = request.headers['Authorization']
    username = get_username(token[len('Bearer '):])
    dbservice = DBService()
    try:
        sql = "update stock_order set status=1 where id = %s and username = '%s'and status=0" % (order_id, username)
        print(sql)
        dbservice.exec_and_commit(sql)
        return jsonify(code = 4, msg="订单状态更新成功")
    except:
        return jsonify(code = 5, msg="订单状态更新失败")
    finally:
        dbservice.close_connect()


@app.route('/user_orderid',methods= ["GET"])
@auth.login_required
def user_orderid():
    # username = request.args.get("username")
    token = request.headers['Authorization']
    username = get_username(token[len('Bearer '):])
    sql = "select id from stock_order where username = '%s' order by id desc limit 20;" %(username)
    print(sql)
    dbservice = DBService()
    try:
        rows = dbservice.exec_with_return(sql)
        if rows:
            data = dbservice.get_cursor().fetchall()
            print([data[i][0] for i in range(0,len(data))])
            return jsonify(code = 5, msg = "查询成功", orderid = [data[i][0] for i in range(0,len(data))])
        else:
            return jsonify(code = 6, msg = "未查询到数据", sql = sql)
    except Exception as ex:
        return jsonify(code=400, msg="异常" + str(ex))
    finally:
        dbservice.close_connect()

@app.route('/get_order',methods= ["GET"])
@auth.login_required
def get_order():
    orderid = request.args.get("orderid")
    sql = "select t1.id,t1.sid,t1.orderprice,t2.name,t1.receiver,t1.phone,t1.address,date_format(t1.create_time, '%Y-%c-%d %H:%i:%s') as create_time,t1.status from stock_order t1,stock t2 where t1.sid = t2.id and t1.id = {0} limit 20".format(orderid)
    print(sql)
    dbservice = DBService()
    try:
        rows = dbservice.exec_with_return(sql)
        if rows:
            data = dbservice.get_cursor().fetchall()
            result = dict(zip(('order_id', 'stock_id', 'orderprice', 'name', 'receiver', 'phone', 'address', 'create_time', 'status'), data[0]))
            return jsonify(code = 5, msg = "查询成功",sql = sql, data = result)
        else:
            return jsonify(code = 6, msg = "未查询到数据", sql = sql)
    except Exception as ex:
        return jsonify(code=6, msg="异常" + str(ex))
    finally:
        dbservice.close_connect()

def get_username(token):
    """校验token"""
    s = Serializer(app.config["SECRET_KEY"], expires_in=24 * 3600)
    try:
        data = s.loads(token)
    except SignatureExpired:
        # token正确但是过期了
        return None
    except BadSignature:
        # token错误
        return None
    user = data['username']
    return user

@app.route('/get_address',methods= ["GET"])
@auth.login_required
def get_address():
    print("========get_address")
    token = request.headers['Authorization']
    username = get_username(token[len('Bearer '):])
    print(username)
    sql = "select phone,address from userinfo uinfo LEFT JOIN users u on uinfo.uid =  u.id where u.`name` = '%s' order by uinfo.id desc limit 1" % (
        username)
    print(sql)
    dbservice = DBService()
    try:
        rows = dbservice.exec_with_return(sql)
        if rows:
            data = dbservice.get_cursor().fetchall()
            result = dict(zip(('phone', 'address'), data[0]))
            return jsonify(code=5, msg="查询成功", data=result)
        else:
            return jsonify(code=6, msg="未查询到数据", sql=sql)
    except Exception as ex:
        return jsonify(code=400, msg="异常" + str(ex))
    finally:
        dbservice.close_connect()

class DBService:
    _db = None
    _cursor = None

    def __init__(self):
        try:
            self._db = db_connection.Connection(host="localhost", port=3306,
                                                user="root", password="root",
                                                database="apitest", charset='utf8', init_command='SET NAMES UTF8')
        except:
            self._db = None
            pass

    def get_cursor(self):
        if self._cursor == None:
            self._cursor = self._db.cursor()
        return self._cursor

    def exec_with_return(self, sql):
        if self._cursor == None:
            self._cursor = self._db.cursor()
        return self._cursor.execute(sql)

    def exec_and_commit(self, sql):
        if self._cursor == None:
            self._cursor = self._db.cursor()
        self._cursor.execute(sql)
        self._db.commit()

    def commit(self):
        self._db.commit()

    def close_connect(self):
        if self._cursor != None:
            self._cursor.close()
        if self._db != None:
            self._db.close()

if __name__ == '__main__':
	app.run(host='0.0.0.0',debug=True)

