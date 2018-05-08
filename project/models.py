from exts import db
from datetime import datetime
from werkzeug.security import  generate_password_hash,check_password_hash

class User(db.Model):
    __tablename__='user'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    username=db.Column(db.String(50),nullable=False)
    telephone=db.Column(db.String(11),nullable=False)
    password=db.Column(db.String(100),nullable=False)
    sex=db.Column(db.String(50),nullable=True)
    self_introduce=db.Column(db.String(100),nullable=True)
    liveplace=db.Column(db.String(50),nullable=True)
    job=db.Column(db.String(20),nullable=True)
    xueli=db.Column(db.String(20),nullable=True)
    touxiang=db.Column(db.LargeBinary(length=2048),nullable=True)

    def __init__(self,*args,**kwargs):
        telephone=kwargs.get('telephone')
        username=kwargs.get('username')
        password=kwargs.get('password')

        self.telephone=telephone
        self.username=username
        self.password=generate_password_hash(password)

    def check_password(self,raw_password):
        result=check_password_hash(self.password,raw_password)
        return result

class User2(db.Model):
    __tablename__ = 'user2'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(50), nullable=False)

# class UserInform(db.Model):
#     __tablename__='userinform'
#     id=db.Column(db.Integer,primary_key=True,autoincrement=True)
#     sex=db.Column(db.String(50),nullable=False)
#     self_introduce=db.Column(db.String(100),nullable=False)
#     liveplace=db.Column(db.String(50),nullable=False)
#     job=db.Column(db.String(20),nullable=False)
#     xueli=db.Column(db.String(20),nullable=False)
#
#     username = db.relationship('User', backref=db.backref('user'))

#发布的问题
class Question(db.Model):
    __tablename__='question'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    question_title=db.Column(db.String(100),nullable=False)
    content=db.Column(db.Text,nullable=False)
    create_time=db.Column(db.DateTime,default=datetime.now)
    author_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    author=db.relationship('User',backref=db.backref('realquestions'))

#针对发布的问题进行的回答
class AnswerQuestion(db.Model):
    __tablename__='answer_question'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    content=db.Column(db.Text,nullable=False)
    create_time=db.Column(db.DateTime,default=datetime.now)

    author_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    answer_question_id=db.Column(db.Integer,db.ForeignKey('question.id'))

    author=db.relationship('User',backref=db.backref('realanswer'))
    question=db.relationship('Question',backref=db.backref('questionAnswer'))

#发布的文章
class Article(db.Model):
    __tablename__='article'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    title=db.Column(db.String(100),nullable=False)
    content=db.Column(db.Text,nullable=False)
    #now()获取的是服务器第一次运行的时间
    #now是每次创建一个模型的时候，都获取当前时间
    create_time=db.Column(db.DateTime,default=datetime.now)
    author_id=db.Column(db.Integer,db.ForeignKey('user.id'))
    author=db.relationship('User',backref=db.backref('questions'))




#文章下的评论
class Answer(db.Model):
    __tablename__='answer'
    id=db.Column(db.Integer,primary_key=True,autoincrement=True)
    content=db.Column(db.Text,nullable=False)
    create_time=db.Column(db.DateTime,default=datetime.now)
    article_id=db.Column(db.Integer,db.ForeignKey('article.id'))
    author_id=db.Column(db.Integer,db.ForeignKey('user.id'))

    article=db.relationship('Article',backref=db.backref('answers',order_by=create_time.desc()))
    author=db.relationship('User',backref=db.backref('answers'))


