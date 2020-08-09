#coding=utf-8
__author__ = 'Mr. Null'

from flask import Flask, request, jsonify, Response, make_response
from flask import render_template, redirect
from flask_cors import CORS
import json
import hashlib
import requests

API_URL = "http://localhost:5000"
app = Flask(__name__)
# pip3 install Flask-Cors
CORS(app, supports_credentials=True)  # 设置跨域
app.config["REMEMBER_COOKIE_SECURE"] = True

@app.route('/login',methods= ["GET"])
def to_login():
    return render_template('login.html')

@app.route('/login',methods= ["POST"])
def login():
    data = request.form.to_dict()
    input_name = hashlib.md5()  # 要加密的字符串
    password = data['password']  # 获取要加密的字符串
    input_name.update(password.encode("utf-8"))
    md5_password = input_name.hexdigest()
    del data['password']
    data['password'] = md5_password
    resp = requests.post(API_URL + "/login", json=data)
    if resp.status_code == 200:
        resp_data = json.loads(resp.text)
        print(resp_data)
        if resp_data['code'] == 4:
            print(request.host_url)
            response = make_response(redirect("/index"))
            # cookies = make_response(request.host_url)
            # headers = {
            #     'location': 'http://localhost:5000/index'
            # }
            response.set_cookie('username', data['username'])
            response.set_cookie('token', resp_data['token'])
            if resp_data['is_admin']:
                response.set_cookie('ia', '1')
            else:
                response.delete_cookie('ia')
            # response.headers = headers
            return response
        else:
            return render_template('error.html', err_msg=resp_data['msg'])
    return render_template('error.html', err_msg="登录响应错误码：" + str(resp.status_code))


@app.route('/register',methods= ["GET"])
def to_register():
    print("register")
    return render_template('register.html')

@app.route('/register',methods= ["POST"])
def register():
    data = request.form.to_dict()
    print(request.base_url)
    input_name = hashlib.md5()  # 要加密的字符串
    password = data['password']  # 获取要加密的字符串
    input_name.update(password.encode("utf-8"))
    md5_password = input_name.hexdigest()
    del data['password']
    data['password'] = md5_password
    resp = requests.post(API_URL + "/register", json=data)
    if resp.status_code == 200:
        resp_data = json.loads(resp.text)
        if resp_data['code'] == 4:
            response = make_response(redirect("/login"))
            return response
    return render_template('error.html', err_msg=resp_data['msg'])


@app.route('/index',methods= ["GET"])
@app.route('/',methods= ["GET"])
def index():
    return render_template('index.html')

@app.route('/get_product_detail/<productid>',methods= ["GET"])
def get_product_detail(productid=None):
    return render_template('product_detail.html', productid=productid)

@app.route('/to_add_product', methods=['GET'])
def to_add_product():
    return render_template('add_product.html')

@app.route('/add_product', methods=['POST'])
def add_product():
    return render_template('/index')

@app.route('/to_add_order', methods=['GET'])
def to_add_order():
    productid = request.args.get("productid")
    return render_template('add_order.html', productid=productid)

@app.route('/pay', methods=['POST'])
def pay():
    token = request.cookies.get('token')
    data = request.form.to_dict()
    orderprice = float(data['price']) * int(data['buy_count'])
    data['orderprice'] = orderprice
    headers = {
        "Authorization": "Bearer " + token
    }
    print(data)
    resp = requests.post(API_URL + "/add_order", json=data, headers=headers)
    if resp.status_code == 200:
        resp_data = json.loads(resp.text)
        if resp_data['code'] == 2003:
           return render_template('pay_mock.html', order_id=resp_data['order_id'], pay_price=orderprice)
        else:
            return render_template('error.html', err_msg=resp_data['msg'])
    return render_template('error.html', err_msg="支付失败！请重新支付！")
    # return render_template('pay_mock.html', order_id=1, pay_price=17.1)

@app.route('/pay_end', methods=['POST'])
def pay_end():
    token = request.cookies.get('token')
    data = request.form.to_dict()
    headers = {
        "Authorization": "Bearer " + token
    }
    print(data)
    resp = requests.post(API_URL + "/update_order", json=data, headers=headers)
    if resp.status_code == 200:
        resp_data = json.loads(resp.text)
        if resp_data['code'] == 4:
           return render_template('my_order.html')
        else:
            return render_template('error.html', err_msg=resp_data['msg'])
    return render_template('error.html', err_msg="订单状态更新操作失败！")
    # return render_template('pay_mock.html', order_id=1, pay_price=17.1)

@app.route('/my_order', methods=['GET'])
def my_order():
    return render_template('my_order.html')

@app.route('/my_order_detail/<orderid>', methods=['GET'])
def my_order_detail(orderid=None):
    return render_template('my_order_detail.html', orderid=orderid)


if __name__ == '__main__':
    app.run(port=5001, debug=True)
