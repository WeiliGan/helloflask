from flask import Flask, request
app = Flask(__name__)


# 创建实例程序
@app.route('/')
def index():
    return '<h1>Hello Flask!</h1>'


# 动态URL
@app.route('/greet/<name>')
def greet(name):
    return '<h1>Hello, %s!</h1>' % name


# 获取请求URL中的查询字符串
@app.route('/hello')
def hello():
    # 获取参数name的值，并且插入返回值中
    name = request.args.get('name', 'Human')
    return '<h1>Hello, %s!</h1>' % name


# 使用int转换器，转换器使用规则<转换器:变量名>
@app.route('/goback/<int:year>')
def go_back(year):
    return 'Welcome to %d!' % (2019 - year)


# 使用any转换器，使用负责<any(可选值):变量名>
@app.route('/colors/<any(blue, white, red):color>')
def three_colors(color):
    return '<p> have three color!</p>'


# 另一种写法
colors = ['blue', 'white', 'red']
@app.route('/colors/<any(%s):color>' % str(colors)[1:-1]) 
def three_colors(color):
    return '<p> have three color!</p>'
