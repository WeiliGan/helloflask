from flask import Flask
app = Flask(__name__)


# 创建实例程序
@app.route('/')
def index():
    return '<h1>Hello Flask!</h1>'


# 动态URL
@app.route('/greet/<name>')
def greet(name):
    return '<h1>Hello, %s!</h1>' % name
