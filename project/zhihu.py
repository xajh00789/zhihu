from flask import Flask,g,render_template,request,url_for,redirect,session,flash
import config
from models import User2,User,Article,Answer,Question,AnswerQuestion
from exts import db
from functools import wraps
from decorates import login_required
from sqlalchemy import or_
import os
import imghdr
from flask_bootstrap import Bootstrap
from flask_wtf import Form
from wtforms import BooleanField,PasswordField,FileField,SubmitField,ValidationError,TextField,validators
import base64

app=Flask(__name__)
app.config.from_object(config)
bootstrap=Bootstrap(app)
db.init_app(app)


# class RegistrationForm(Form):
#     username=TextField('Username',[validators.Length(min=4,max=25)])
#     email=TextField('Email Address',[validators.Length(min=6,max=35)])
#     password=PasswordField('New Password',[validators.Required(),validators.EqualTo('confirm',message='Passwords must match')])
#     confirm=PasswordField('Repeat Password')
#     accept_tos=BooleanField('I accept the TOS',[validators.Required()])
#
# @app.route('/register2',methods=['GET','POST'])
# def register2():
#     form=RegistrationForm(request.form)
#     if request.method=='POST' and form.validate():
#         user=User2(form.username.data,form.email.data,form.password.data)
#         db.session.add(user)
#         db.session.commit()
#         flash('Thanks for registering')
#         return redirect(url_for('login'))
#     return render_template('register2.html',form=form)


@app.route('/')
@login_required
def index():
    #user=User.query.filter(User.id==g.user.id).first()
    user=g.user
    question_num=len(user.realquestions)
    answer_num=len(user.realanswer)
    article_num=len(user.questions)
    context={
        'articles':Article.query.order_by('-create_time').all(),
        'user':user,
        'question_num':question_num,
        'answer_num':answer_num,
        'article_num':article_num
    }
    return render_template('index.html',**context)

@app.route('/index_answer/')
@login_required
def index_answer():
    user=User.query.filter(User.id==g.user.id).first()
    question_num=len(user.realquestions)
    answer_num=len(user.realanswer)
    article_num=len(user.questions)
    context={
        'questions': Question.query.order_by('-create_time').all(),
        'user': g.user,
        'question_num': question_num,
        'answer_num': answer_num,
        'article_num': article_num
    }
    return render_template('index_answer.html',**context)

@app.route('/login/',methods=['GET','POST'])
def login():
    if request.method=='GET':
        return render_template('login.html')
    else:
        username=request.form.get('username')
        password=request.form.get('password')
        user=User.query.filter(User.username==username).first()
        if user and user.check_password(password):
            session['user_id']=user.id
            session.permanent=True
            return redirect(url_for('index'))
        else:
            return u'账号或密码错误，请确认后再输！'

class UploadBackgroundForm(Form):
    image_file=FileField('背景')
    submit=SubmitField('上传')

    def validate_image_fiel(self,field):
        if field.data.filename[-4:].lower()!='.jpg' or field.data.filename[-4:].lower()!='.png':
            raise ValidationError('照片格式不正确(需为.jpg格式)')
        if imghdr.what(field.data)!='jpeg' or imghdr.what(field.data)!='png':
            raise ValidationError('不合法的照片格式(确定您上传的是照片)')

@app.route('/persionalInform/',methods=['GET','POST'])
def persional_inform():
    image='uploads/'+g.user.telephone+'背景'+'.jpg'
    form=UploadBackgroundForm()
    if form.validate_on_submit():
        image='uploads/'+g.user.telephone+'背景'+'.jpg'
        form.image_file.data.save(os.path.join(app.static_folder,image))
    touxiang='uploads/'+g.user.telephone+'头像'+'.jpg'
    question_num=len(g.user.realquestions)
    answer_num=len(g.user.realanswer)
    article_num=len(g.user.questions)
    context = {
        'questions': Question.query.filter(Question.author_id == g.user.id).all(),
        'question_num': question_num,
        'answer_num': answer_num,
        'article_num': article_num
    }
    return render_template('persionalInform.html',form=form,image=image,user=g.user,touxiang=touxiang,**context)

@app.route('/persional_question/<username>',methods=['GET','POST'])
def persional_question(username):
    user2=User.query.filter(User.username==username).first()
    telephone=user2.telephone
    image='uploads/'+telephone+'背景'+'.jpg'
    touxiang='uploads/'+telephone+'头像'+'.jpg'
    question_num=len(user2.realquestions)
    answer_num=len(user2.realanswer)
    article_num=len(user2.questions)
    context={
        'questions':Question.query.filter(Question.author_id==user2.id).all(),
        'question_num': question_num,
        'answer_num': answer_num,
        'article_num': article_num
    }

    return render_template('persional_question.html',image=image,user=g.user,user2=user2,touxiang=touxiang,**context)

@app.route('/personal_article/<username>',methods=['GET','POST'])
def personal_article(username):
    user2=User.query.filter(User.username==username).first()
    touxiang='uploads/'+user2.telephone+'头像'+'.jpg'
    image='uploads/'+user2.telephone+'背景'+'.jpg'
    question_num=len(user2.realquestions)
    answer_num=len(user2.realanswer)
    article_num=len(user2.questions)
    context={
        'articles':Article.query.filter(Article.author_id==user2.id).all(),
        'question_num': question_num,
        'answer_num': answer_num,
        'article_num': article_num
    }
    return render_template('personal_article.html',image=image,user2=user2,user=g.user,touxiang=touxiang,**context)


@app.route('/personal_answer/<username>',methods=['GET','POST'])
def personal_answer(username):
    user2=User.query.filter(User.username==username).first()
    image = 'uploads/' + user2.telephone + '背景' + '.jpg'
    touxiang='uploads/'+user2.telephone+'头像'+'.jpg'
    question_num=len(user2.realquestions)
    answer_num=len(user2.realanswer)
    article_num=len(user2.questions)
    context={
        'answers':AnswerQuestion.query.filter(AnswerQuestion.author_id==user2.id).all(),
        'question_num': question_num,
        'answer_num': answer_num,
        'article_num': article_num

    }
    return render_template('personal_answer.html',image=image,user2=user2,user=g.user,touxiang=touxiang,**context)




class UploadForm(Form):
    image_file=FileField('头像')
    submit=SubmitField('上传')

    def validate_image_fiel(self,field):
        if field.data.filename[-4:].lower()!='.jpg' or field.data.filename[-4:].lower()!='.png':
            raise ValidationError('照片格式不正确(需为.jpg格式)')
        if imghdr.what(field.data)!='jpeg' or imghdr.what(field.data)!='png':
            raise ValidationError('不合法的照片格式(确定您上传的是照片)')

@app.route('/persionalInform_edit/',methods=['GET','POST'])
def persionalInform_edit():
    if request.method == 'GET':
        image ='uploads/'+g.user.telephone+'头像'+'.jpg'
        form = UploadForm()
        if form.validate_on_submit():
            image='uploads/'+g.user.telephone+'头像'+'.jpg'
            form.image_file.data.save(os.path.join(app.static_folder,image))
        return render_template('persionalInform_edit.html',form=form,image=image)
    else:
        image = 'uploads/'+g.user.telephone+'头像'+'.jpg'
        form = UploadForm()
        if form.validate_on_submit():
            image='uploads/'+g.user.telephone+'头像'+'.jpg'
            form.image_file.data.save(os.path.join(app.static_folder,image))

        username = request.form.get('username')
        sex = request.form.get('sex')
        self_introduce = request.form.get('self-introduce')
        liveplace = request.form.get('liveplace')
        job=request.form.get('job')
        xueli=request.form.get('xueli')
        user_id = g.user.id
        print(user_id)
        if username:
            User.query.filter(User.id == user_id).update({User.username: username})
        if sex:
            User.query.filter(User.id == user_id).update({User.sex:sex})
        if self_introduce:
            #User.query.filter(User.id == user_id).update({User.self_introduce:'德国本科/播音主持群欢迎加入'})
            User.query.filter(User.id == user_id).update({User.self_introduce:self_introduce})
        if liveplace:
            User.query.filter(User.id == user_id).update({User.liveplace:liveplace})
        if job:
            User.query.filter(User.id == user_id).update({User.job:job})
        if  xueli:
            User.query.filter(User.id == user_id).update({User.xueli:xueli})
        db.session.commit()
        return render_template('persionalInform_edit.html',form=form,user=g.user,image=image)

@app.route('/detail/<int:question_id>')
@login_required
def detail(question_id):
    user2=Article.query.filter(Article.id == question_id).first().author
    question_num=len(user2.realquestions)
    answer_num=len(user2.realanswer)
    article_num=len(user2.questions)
    context={
        'article':Article.query.filter(Article.id == question_id).first(),
        'question_num': question_num,
        'answer_num': answer_num,
        'article_num': article_num
    }
    return render_template('detail.html',user2=user2,user=g.user,**context)

@app.route('/answer_detail/<int:question_id>')
@login_required
def answer_detail(question_id):
    user2=Question.query.filter(Question.id == question_id).first().author
    question_num=len(user2.realquestions)
    answer_num=len(user2.realanswer)
    article_num=len(user2.questions)
    context={
        'question':Question.query.filter(Question.id==question_id).first(),
        'answers':AnswerQuestion.query.filter(AnswerQuestion.answer_question_id==question_id).all(),
        'user2': user2,
        'user':g.user,
        'question_num': question_num,
        'answer_num': answer_num,
        'article_num': article_num
    }
    return render_template('answer_detail.html',**context)

@app.route('/answer_detail_edit/<int:question_id>',methods=['GET','POST'])
def answer_detail_edit(question_id):
    if request.method=='GET':
        question=Question.query.filter(Question.id==question_id).first()
        title=question.question_title
        return render_template('answer_detail_edit.html',title=title)
    else:
        author_id=g.user.id
        question = Question.query.filter(Question.id == question_id).first()
        questionId=question.id
        content=request.form.get('content')
        if content=='':
            return (u'回答内容不能为空！')
        answer=AnswerQuestion(content=content,author_id=author_id,answer_question_id=questionId)
        db.session.add(answer)
        db.session.commit()
        return redirect(url_for('answer_detail',question_id=question_id))

#添加文章回答
# @app.route('/add_answer_artilce',methods=['POST'])
# @login_required
# def  add_answer_article():


@app.route('/add_answer/',methods=['POST'])
@login_required
def add_answer():
    content=request.form.get('answer_content')
    article_id=request.form.get('article_id')

    answer=Answer(content=content)
    # user_id=session['user_id']
    # user=User.query.filter(User.id==user_id).first()
    answer.author=g.user
    article=Article.query.filter(Article.id==article_id).first()
    answer.article=article
    db.session.add(answer)
    db.session.commit()
    return redirect(url_for('detail',question_id=int(article_id)))

@app.route('/delete_article_answer/',methods=['POST'])
@login_required
def delete_article_answer():
    article_id=request.form.get('article_id')
    answer_id=request.form.get('answer_id')
    answer=Answer.query.filter(Answer.id==answer_id).first()
    db.session.delete(answer)
    db.session.commit()
    return redirect(url_for('detail',question_id=int(article_id)))

@app.route('/delete_question_answer/',methods=['POST'])
@login_required
def delete_question_answer():
    answer_id=request.form.get('answer_id')
    question_id=request.form.get('question_id')
    answer=AnswerQuestion.query.filter(AnswerQuestion.id==answer_id).first()
    db.session.delete(answer)
    db.session.commit()
    return redirect(url_for('answer_detail',question_id=int(question_id)))


@app.route('/delete_article/',methods=['POST'])
@login_required
def delete_article():
    article_id=request.form.get('article_id')
    username=g.user.username
    answers=Answer.query.filter(Answer.article_id==article_id).all()
    article=Article.query.filter(Article.id==article_id).first()
    for answer in answers:
        db.session.delete(answer)
    db.session.delete(article)
    db.session.commit()
    return redirect(url_for('personal_article',username=username))

@app.route('/delete_question/',methods=['POST'])
@login_required
def delete_question():
    question_id=request.form.get('question_id')
    username=g.user.username
    answers=AnswerQuestion.query.filter(AnswerQuestion.answer_question_id==question_id).all()
    question=Question.query.filter(Question.id==question_id).first()
    for answer in answers:
        db.session.delete(answer)
    db.session.delete(question)
    db.session.commit()
    return redirect(url_for('persional_question',username=username))

# @app.route('/delete_question/',methods=['POST'])
# @login_required
# def delete_question():
#


@app.route('/article',methods=['GET','POST'])
@login_required
def article():
    if request.method=='GET':
        return render_template('article.html')
    else:
        title=request.form.get('title')
        content=request.form.get('content')
        article=Article(title=title,content=content)
        # user_id=session.get('user_id')
        # user=User.query.filter(User.id==user_id).first()
        article.author=g.user
        db.session.add(article)
        db.session.commit()
        return redirect(url_for('index'))

@app.route('/article_edit/',methods=['GET','POST'])
@login_required
def article_edit():
    article_id=request.form.get('article_id')
    print(article_id)
    article=Article.query.filter(Article.id==article_id).first()
    print(article)
    return render_template('article_edit.html')



@app.route('/question/',methods=['GET','POST'])
@login_required
def question():
    if request.method=='GET':
        return render_template('question.html')
    else:
        title=request.form.get('title')
        content=request.form.get('content')
        question=Question(question_title=title,content=content)
        question.author=g.user
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index_answer'))

@app.route('/search/')
def search():
    q=request.args.get('q')
    #或搜索
    condition=or_(Article.title.contains(q),Article.content.contains(q))
    condition2=or_(Question.question_title.contains(q),Question.content.contains(q))
    #且搜索
    #condition=(Article.title.contains(q),Article.content.contains(q))
    articles=Article.query.filter(condition).order_by('-create_time')
    questions=Question.query.filter(condition2).order_by('-create_time')
    return render_template('index.html',articles=articles,questions=questions)

@app.route('/logout/')
def logout():
    session.pop('user_id')
    return redirect(url_for('login'))

@app.before_request
def my_before_request():
    user_id=session.get('user_id')
    if user_id:
        user=User.query.filter(User.id==user_id).first()
        if user:
            g.user=user
            touxiang='uploads//'+g.user.telephone+'头像'+'.jpg'
            background='uploads//'+g.user.telephone+'背景'+'.jpg'
            touxiang_lujing=os.path.join(app.static_folder, touxiang)
            background_lujing=os.path.join(app.static_folder, background)
            if os.path.exists(touxiang_lujing):
                g.touxiang=touxiang
            if os.path.exists(background_lujing):
                g.background=background



@app.context_processor
#上下文处理器应该返回一个字典，字典中的'key'会被模板中当成变量渲染
#上下文处理器中返回的字典在所有页面中都可以用的。
def  my_context_processor():
    if hasattr(g,'user'):
        return {'user':g.user}
    #before_request->视图函数->context-processor
    # user_id=session.get('user_id')
    # if user_id:
    #     user=User.query.filter(User.id==user_id).first()
    #     if user:
    #         return {'user':user}
    return {}

@app.route('/register/',methods=['GET','POST'])
def regist():
    if request.method=='GET':
        return render_template('register.html')
    else:
        telephone=request.form.get('telephone')
        username=request.form.get('username')
        password1=request.form.get('password1')
        password2=request.form.get('password2')
        user=User.query.filter(User.telephone==telephone).first()
        username_verify = User.query.filter(User.username == username).first()
        if user or username_verify:
            return u'该手机号码或账号已经注册，请更换手机号码或账号！'
        else:
            if password1!=password2:
                return u'密码或账号错误！'
            else:
                user=User(telephone=telephone,username=username,password=password1)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))




if __name__=='__main__':
    app.run()