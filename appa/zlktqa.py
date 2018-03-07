# coding=utf-8

from flask import Flask, render_template, request, url_for
import config
from models import User, Question, Answer, Movies
from exts import db
from config import DEBUG
from werkzeug import redirect
from flask.globals import session
from decorators import login_required
from sqlalchemy import or_
from movietest import movies
from flask_login import current_user,current_app,LoginManager,logout_user
app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
login_manager=LoginManager()
login_manager.session_protection='strong'
login_manager.login_view='login'
login_manager.init_app(app)
# 登录限制
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
@app.route('/',methods=['GET','POST'])
def index():
    page=request.args.get('page',1,type=int)
    pagination=Question.query.order_by('-create_time').paginate(page,error_out=False)
    context = {
        'questions':pagination.items

    }
    return render_template('index.html',user=None,pagination=pagination,**context)

@app.route('/index_login/',methods=['GET','POST'])
def index_login():
    page = request.args.get('page', 1, type=int)
    pagination = Question.query.order_by('-create_time').paginate(page, error_out=False)
    context = {
        'questions': pagination.items

    }
    user_id=session.get('user_id')
    user = User.query.filter(User.id == user_id).first()
    if user is None:
        return render_template('404.html')
    return render_template('index_login.html',user=user,pagination=pagination,**context)

@app.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html',user=None)
    else:
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        user = User.query.filter(
            User.telephone == telephone).first()

        if user and user.check_password(password):
            session['user_id'] = user.id
            session.permanent = True
            return redirect(url_for('index_login'))
        else:
            return u'密码错误'

@app.route('/logout/')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/regist/', methods=['GET', 'POST'])#注册账号
def regist():
    if request.method == 'GET':
        return render_template('regist.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter(User.telephone == telephone).first()
        if user:
            return u'该手机号码已被注册，请更换手机号码'
        else:
            if password1 != password2:
                return u'两次密码不相等，请重新输入'
            else:
                user = User(telephone=telephone,
                            username=username, password=password1)#建立ORM模型映射一条记录
                db.session.add(user)
                db.session.commit()#提交事务
                return redirect(url_for('login'))


def tags_tag(tags):
    tag = tags.split(',')
    num = len(tag)
    print(tag, num)
@app.route('/myshell/')
def myshell():
    Question.generate_fake(100)
    User.generate_fake(100)
    return redirect(url_for('index'))
@app.route('/user/<username>')
def user(username):
    u=User.query.filter(User.username==username).first()
    if u is None:
        return render_template('404.html')
    return render_template('user.html',user=u)
@app.route('/modify_user/<username>',methods=['POST'])
@login_required
def modify_user(username):
    name=request.form.get('name')
    location=request.form.get('location')
    about_me=request.form.get('about_me')



@app.route('/question/', methods=['GET', 'POST'])
@login_required
def question():
    if request.method == 'GET':
        return render_template('question.html',user=None)
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        tags=request.form.get('tags')
        question = Question(title=title, content=content,tags=tags)
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        question.author = user
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index'))
@app.route('/search/')
def search():
    q=request.args.get('q')
    questions=Question.query.filter(or_(Question.title.contains(q),Question.content.contains(q)))
    page = request.args.get('page', 1, type=int)
    pagination = Question.query.order_by('-create_time').paginate(page, error_out=False)
    return render_template('index.html',user=None,pagination=pagination,questions=questions)
@app.route('/detail/<question_id>/')
def detail(question_id):
    question_model = Question.query.filter(Question.id == question_id).first()

    return render_template('detail.html',user=None,question=question_model)

@app.route('/tag_search/<tag_name>/', methods=['GET', 'POST'])
def tag_search(tag_name):
    tag_questions = Question.query.filter(Question.tags.contains(tag_name)).all()
    return render_template('index.html',user=None,questions=tag_questions)

@app.route('/add_answer/', methods=['POST'])
@login_required
def add_answer():
    content = request.form.get('answer_content')
    question_id = request.form.get('question_id')

    answer = Answer(content=content)
    user_id = session['user_id']
    user = User.query  .filter(User.id == user_id).first()
    answer.author = user
    question = Question.query.filter(Question.id == question_id).first()
    answer.question = question
    db.session.add(answer)
    db.session.commit()

    return redirect(url_for('detail',user=user, question_id=question_id))


if __name__ == '__main__':
    app.run(debug=DEBUG)

