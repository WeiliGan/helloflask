import os
import click
from flask import Flask, request, redirect, url_for, session, abort, json
from flask import make_response
from flask import jsonify
from urllib.parse import urlparse, urljoin
from jinja2.utils import generate_lorem_ipsum
# from flask import g
app = Flask(__name__)


app.secret_key = os.getenv('SECRET_KEY', 'secret string')


# 创建实例程序
@app.route('/')
def index():
    return '<h1>Hello Flask!</h1>'


# 动态URL
@app.route('/greet/<name>')
def greet(name):
    return '<h1>Hello, %s!</h1>' % name


# 创建自定义命令
@app.cli.command()
def tries():
    click.echo('Hello, hushuo!')


# 重定向到/hello
@app.route('/hi')
def hi():
    return redirect(url_for('hello'))


# 获取请求URL中的查询字符串
@app.route('/hello', methods=['GET', 'POST'])
def hello():
    # 获取参数name的值，并且插入返回值中
    name = request.args.get('name')
    if name is None:
        # 从cookie中获name取值
        name = request.cookies.get('name', 'Human')
    response = '<h1>Hello, %s!</h1>' % name
    # 根据用户认证状态返回不同的内容
    if 'logged_in' in session:
        response += '[Authenticated]'
    else:
        response += '[Not Authenticated]'
    return response


# 使用int转换器，转换器使用规则<转换器:变量名>
@app.route('/goback/<int:year>')
def go_back(year):
    return 'Welcome to %d!' % (2019 - year)


# 返回404错误响应
@app.route('/20')
def not_found():
    abort(404)


# 通过Flask提供的make_redponse，使用MIME纯文本类型
@app.route('/foo')
def foo():
    response = make_response('Hello, Word!')
    response.mimetype = 'text/plain'
    return response


# 通过Flask提供的make_redponse，使用MIME中的json文本类型
@app.route('/foo_a')
def foo_a():
    data = {
        'name': 'WeiliGan',
        'gender': 'male'
    }
    a = make_response(json.dumps(data))
    a.mimetype = 'application/json'
    return a


# 通过Flask提供的make_redponse，使用MIME中的json文本类型，
# 在flask中借助jsonify()函數來完成上述效果，
# 只需传入数据和参数，它会对我们传入的参数进行序列化
@app.route('/foo_b')
def foo_b():
    # return jsonify(name='zhangsan', gender='male')
    return jsonify({'name': 'lisi', 'gender': 'male'})


# 通过附加状态码来自定义你响应类型
@app.route('/foo_c')
def foo_c():
    return jsonify(message='Error!'), 500


# 设置cookie
@app.route('/set/<name>')
def set_cookie(name):
    response = make_response(redirect(url_for('hello')))
    response.set_cookie('name', name)
    return response


# 登入用户
@app.route('/login')
def login():
    # 写入session
    session['logged_in'] = True
    return redirect(url_for('hello'))


# 模拟后台管理
@app.route('/admin')
def admin():
    if 'logged_in' not in session:
        abort(403)
    return 'Welcome to admin page'


# 登出用户
@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in')
    return redirect(url_for('hello'))


# 利用g程序上下文设置全局变量
# @app.before_request
# def get_name():
#     g.name = request.args.get('name')


@app.route('/foo_try')
def foo_try():
    return '<h1>Foo page</h1><a href="%s">Do something and redirect</a>' % url_for('do_something', next=request.full_path)


@app.route('/bar')
def bar():
    return '<h1>Foo page</h1><a href="%s">Do something and redirect</a>' % url_for('do_something', next=request.full_path)


# 链接视图函数
@app.route('/do_something_and_redirect')
def do_something():
    # 该视图函数实现的功能
    return redirect_back()


# 重定向回上一个页面
def redirect_back(default='hello', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        # 调用is_safe_url函数对URL进行安全验证
        if is_safe_url(target):
            return redirect(target)
    return redirect_back()


# 验证URL安全性
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


# 异步加载长文章示例，显示虚拟文章
@app.route('/post')
def show_post():
    # 生成两段随机文本
    post_body = generate_lorem_ipsum(n=2)
    return '''
<h1>A very long post</h1>
<div class="body">%s</div>
<button id="lode">Lode More</button>
<script src="https://code.jquery.com/jquery-3.3.1.min.js"></script>
<script type="text/javascript">
$(function() {
    $('#load').click(function() {
        $.ajax({
            url: '/more',
            type: 'get',
            success: function(data) {
                $('.body').append(data);
            }
        })
    })
})
</script>''' % post_body


@app.route('/more')
def load_post():
    return generate_lorem_ipsum(n=1)
