# coding=utf-8

from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin,current_user,current_app
class User(UserMixin,db.Model):
    __tablename__ = 'user'
    #email=db.Column(db.String(64),unique=True,index=True)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    telephone = db.Column(db.String(11), nullable=False)
    username = db.Column(db.String(64),unique=True,index=True, nullable=False)
    password= db.Column(db.String(128), nullable=False)
    # 新添加的用户资料
    name=db.Column(db.String(64))
    location=db.Column(db.String(64))
    about_me=db.Column(db.Text())
    member_since=db.Column(db.DateTime(),default=datetime.utcnow)
    last_seen=db.Column(db.DateTime(),default=datetime.utcnow)
    def __init__(self,*args,**kwargs):
        telephone=kwargs.get('telephone')
        username=kwargs.get('username')
        password=kwargs.get('password')
        self.telephone=telephone
        self.username=username
        self.password=generate_password_hash(password)
        self.name = kwargs.get('name')
        self.location = kwargs.get('location')
        self.about_me = kwargs.get('about_me')
        self.member_since = kwargs.get('member_since')
        self.last_seen = kwargs.get('last_seen')

    #刷新用户的最后访问时间
    def ping(self):
        self.last_seen=datetime.utcnow()
        db.session.add(self)
    def check_password(self,raw_password):
        result=check_password_hash(self.password,raw_password)
        return result
    @staticmethod   #生成随机手机号码
    def randtele():
        import random
        foke_num=''.join([str(random.choice(range(10))) for i in range(11)])
        print(foke_num)
        return foke_num
    @staticmethod
    def generate_fake(count=100):
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py

        seed()
        for i in range(100):
            u=User(username=forgery_py.internet.user_name(),
                   telephone=User.randtele(),
                   password=forgery_py.lorem_ipsum.word())
            try:
                db.session.add(u)
            except IntegrityError:
                db.session.commit()
    #role_id=db.Column(db.Integer,db.ForeignKey('roles.id'))
    #def __init__(self,**kwargs):
      #  super(User,self).__init__(**kwargs)
        #####
        # if self.role_id

    #密码散列
    """
    password_hash=db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')
    @password.setter
    def password(self,password):
        self.password_hash=generate_password_hash(password)
    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)
"""
class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    tags=db.Column(db.String(100))
    create_time = db.Column(db.DateTime, default=datetime.now)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    dict_tags = {
        0x00: 'python',
        0x01: 'c++',
        0x02: '电影',
        0x03: '小说',
        0x04: '豆瓣',
        0x05: '图片',
        0x06: '段子',
        0x07: '星星'
    }

    author = db.relationship('User', backref=db.backref('questions'))

    @staticmethod   #生成假数据
    def generate_fake(count=100):
        from random import seed,randint
        import forgery_py

        seed()
        user_count=User.query.count()
        for i in range(count):
            u=User.query.offset(randint(0,user_count-1)).first()
            question=Question(title=forgery_py.lorem_ipsum.title(),
                              content=forgery_py.lorem_ipsum.word(),
                              tags=forgery_py.lorem_ipsum.word())
            question.author = u
            db.session.add(question)
            db.session.commit()
class Answer(db.Model):
    __tablename__ = 'answer'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.Text, nullable=False)
    create_time = db.Column(db.DateTime, default=datetime.now)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    question = db.relationship(
        'Question', backref=db.backref('answers', order_by=id.desc()))
    author = db.relationship('User', backref=db.backref('answers'))
#角色
"""
class Role(db.Model):
    __tablename__='roles'
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(64),unique=True)
    default=db.Column(db.Boolean,default=False,index=True)
    permissions=db.Column(db.Integer)
    user=db.relationship('User',backref='role',lazy='dynamic')

    @staticmethod
    def insert_roles():
        roles={
            'User':(Permission.FOLLOW|
                    Permission.COMMENT|
                    Permission.WRITE_ARTICLES,True),
            'Moderator':(Permission.FOLLOW|Permission.COMMENT|Permission.WRITE_ARTICLES|Permission.MODERATE_COMMENTS,False),
            'Administrator':(0xff,False)
        }
        for r in roles:
            role=Role.query.filter_by(name=r).first()
            if role is None:
                role=Role(name=r)
            role.permissions=roles[r][0]
            role.default=roles[r][1]
            db.session.add(role)
            db.session.commit()
"""
#权限常量
class Permission:
    FOLLOW=0x01
    COMMENT=0x02
    WRITE_ARTICLES=0x04
    MODERATE_COMMENTS=0x08
    ADMINISTER=0x80


# 自己添加的
class Movies(db.Model):
    __tablename__ = 'movie'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    moviename = db.Column(db.String(50), nullable=False)
    directer = db.Column(db.String(50), nullable=False)
    star = db.Column(db.String(50), nullable=False)
    category = db.Column(db.String(50), nullable=False)