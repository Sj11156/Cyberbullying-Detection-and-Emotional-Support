from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import HttpResponseRedirect,redirect
from django.db import connection
from socialapp.forms import pform,sform
from socialapp.models import pmodel,smodel, PredictionDetail
from datetime import *
import datetime
today_date = datetime.date.today()
today = today_date.strftime("%Y-%m-%d")
import numpy as np
import pandas as pd
from  datetime import date 
from datetime import datetime
tms = datetime.now().strftime('%d-%m-%Y %H:%M:%S')
import nltk 
from django.db import connection
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize, sent_tokenize 
stop_words = set(stopwords.words('english')) 
from nltk.stem import PorterStemmer
def depression(request):
	cur=connection.cursor()
	return render(request,'depression.html')
def dpract(request):
    if request.method != "POST":
        return HttpResponse("Invalid request method", status=405)

    cur = connection.cursor()

    try:
        dpr = sum(int(request.POST.get(f'Q{i}', 0)) for i in range(1, 21))  # Now using POST
    except ValueError:
        return HttpResponse("Invalid input data", status=400)

    if dpr <= 10:
        depr = "Normal"
    elif dpr <= 16:
        depr = "Mild Mood Disturbance"
    elif dpr <= 20:
        depr = "Borderline Clinical Depression"
    elif dpr <= 30:
        depr = "Moderate Depression"
    elif dpr <= 40:
        depr = "Severe Depression"
    else:
        depr = "Extreme Depression"

    today = date.today()
    uid = request.session.get('uid', None)

    if not uid:
        return HttpResponse("User not logged in", status=403)

    cur.execute("SELECT depr FROM survey WHERE uid = %s", [uid])
    row = cur.fetchone()

    if row:
        if row[0] == 'Nil':
            cur.execute("UPDATE survey SET depr = %s, date = %s WHERE uid = %s", [depr, today, uid])
    else:
        cur.execute("INSERT INTO survey (uid, depr, date) VALUES (%s, %s, %s)", [uid, depr, today])

    connection.commit()
    cur.close()

    return render(request, 'userhome.html')
def vdeprs(request):
	cur=connection.cursor()
	uid=request.session['uid']
	s="select * from survey where uid='%s'"%(uid)
	cur.execute(s)
	rs=cur.fetchall()
	usr=[]
	for row in rs:
		y={'sid':row[0],'uid':row[1],'depr':row[2]}
		usr.append(y)
	return render(request,'vdeprs.html',{'usr':usr})
def avanalysis(request):
	cur=connection.cursor()
	
	s="select * from survey inner join signup on survey.uid=signup.Uid"
	cur.execute(s)
	rs=cur.fetchall()
	usr=[]
	for row in rs:
		y={'uid':row[1],'fname':row[5],'depr':row[2]}
		usr.append(y)
	return render(request,'avanalysis.html',{'usr':usr})
def mentalchatbot(request):
    return render(request, 'mentalchatbot.html')
def comments(request):
	cursor=connection.cursor()
	pid=request.GET['id']
	ss="select cmid,coment,uid from comments where pid='%s' order by cmid desc"%(pid)
	cursor.execute(ss)
	rss=cursor.fetchall()
	list1=[]
	for row5 in rss:
		y={'cmid':row5[0],'coment':row5[1],'uid':row5[2]}
		list1.append(y)
	sql1="select postadd.*,registration.name from postadd inner join registration on registration.email=postadd.userid where postadd.id='%s'   "%(request.GET['id'])
	cursor.execute(sql1)
	res=cursor.fetchall()
	usrr=[]
	for row1 in res:
		z={'id':row1[0],'post':row1[1],'userid':row1[2],'nme':row1[3],'date':row1[4],'post_image':row1[5],'name':row1[6]}
		usrr.append(z)
	return render(request,'comments.html',{'list1':list1,'pid':pid,'post':usrr})
def vcommentsuser(request):
	cursor=connection.cursor()
	pid=request.GET['id']
	ss="select cmid,coment,uid from comments where pid='%s' order by cmid desc"%(pid)
	cursor.execute(ss)
	rss=cursor.fetchall()
	list1=[]
	for row5 in rss:
		y={'cmid':row5[0],'coment':row5[1],'uid':row5[2]}
		list1.append(y)
	sql1="select postadd.*,registration.name from postadd inner join registration on registration.email=postadd.userid where postadd.id='%s'   "%(request.GET['id'])
	cursor.execute(sql1)
	res=cursor.fetchall()
	usrr=[]
	for row1 in res:
		z={'id':row1[0],'post':row1[1],'userid':row1[2],'nme':row1[3],'date':row1[4],'post_image':row1[5],'name':row1[6]}
		usrr.append(z)
	return render(request,'vcomments.html',{'list1':list1,'pid':pid,'post':usrr})

def cmdaction(request):
	cursor=connection.cursor()
	pid=request.GET['pid']
	c=request.GET['cmd']
	uid=request.session['loginid']
	review =c
	sql2="truncate table postag"
	cursor.execute(sql2)
	tokenized = sent_tokenize(review) 
	for i in tokenized: 
		wordsList1 = nltk.word_tokenize(i) 
		wordsList = [w for w in wordsList1 if not w in stop_words] 
		tagged1 = nltk.pos_tag(wordsList)
		tagged=( [(word, tag) for word, tag in tagged1 if ( tag=='NN' or tag=='NNS' or  tag=='NNP' or tag=='NNPS' or tag=='JJ' or tag=='JJR'or  tag=='JJS'   or tag=='VB'or tag=='VBD' or tag=='VBG' or tag=='VBN' or tag=='VBP'or tag=='VBZ')])		
		for f,g in tagged1:
			sql="insert into postag(data) values('%s')"%(f)
			cursor.execute(sql)
	you=[]
	sql3 = "select * from postag"
	cursor.execute(sql3)
	result1 = cursor.fetchall()
	for row1 in result1:
			d = row1[1]
			you.append(d)	
	sentence=' '.join(you) 	
	
	
	#------
	ps = PorterStemmer() 
	words = word_tokenize(sentence) 
	w1=[]
	w2=''
	sql2="truncate table stemming"
	cursor.execute(sql2)
	for w in words:
		sql="insert into stemming(data) values('%s')"%(ps.stem(w))
		cursor.execute(sql)
		w1.append(ps.stem(w))
		print(w, " : ", ps.stem(w)) 
	w2=' '.join(w1)
	#---
	'''sql2="truncate table pword"
	cursor.execute(sql2)
	sql3 = "select * from stemming"
	cursor.execute(sql3)
	result = cursor.fetchall()
	for row in result:
		sql3 = "select * from positive"
		cursor.execute(sql3)
		result1 = cursor.fetchall()
		for row1 in result1:
			if(row[1]==row1[1]):
				sql="insert into pword(pword) values('%s')"%(row[1])
				cursor.execute(sql)
	sqlp="select * from pword "
	cursor.execute(sqlp)
	c1=cursor.fetchall()
	p=[]
	for r in c1:
		f={'data':r[1]}
		p.append(f)'''
	#--
	sql2="truncate table nword"
	cursor.execute(sql2)
	sql3 = "select * from stemming"
	cursor.execute(sql3)
	result = cursor.fetchall()
	for row in result:
		sql3 = "select * from negative"
		cursor.execute(sql3)
		result1 = cursor.fetchall()
		for row1 in result1:
			if(row[1]==row1[1]):
				sql="insert into nword(nword) values('%s')"%(row[1])
				cursor.execute(sql)
	sqlp="select * from nword "
	cursor.execute(sqlp)
	c1=cursor.fetchall()
	p=[]
	for r in c1:
		f={'data':r[1]}
		p.append(f)
	#--
	'''sqlp="select count(*) from pword "
	cursor.execute(sqlp)
	p1=cursor.fetchall()
	pcount=0
	for r in p1:
		pcount=r[0]'''
	sqlp="select count(*) from nword "
	cursor.execute(sqlp)
	n1=cursor.fetchall()
	ncount=0
	for r in n1:
		ncount=r[0]
	avgcount=0.0
	'''if pcount!=0 and ncount!=0:
		count = float(pcount) + float(ncount)
		sentiscore = (float(pcount) -float(ncount)) / (float(pcount) + float(ncount));
		avgcount = sentiscore / float(count)
		#return HttpResponse(avgcount)
		if (avgcount > 0.25):
			sentilabel = 4
			snt1="Best Performing"
		elif (avgcount < 0.25 and  avgcount>0.00):
			sentilabel = 3
			snt1="(Good)"
		elif (avgcount ==-0.25):
			sentilabel = 1
			snt1="(Fair)"
		elif (avgcount <0.25):
			sentilabel = 0
			snt1="(Bad)"
		else:
			sentilabel=2
			snt1="(Average)"
		re="the comment  belongs to level  "+str(sentilabel)+ ' '+snt1
		return HttpResponse(avgcount)'''
	#return HttpResponse(ncount)
	if(ncount >=1):
		sql="insert into block_user(pid,coment,uid) values('%s','%s','%s')" %(pid,c,uid)
		cursor.execute(sql)
		html="<script>alert('its not posted !!!!!! ');window.location='/comments?id=%s';</script>"%(pid)
		#return HttpResponse(html)
	else:
		sql="insert into comments(pid,coment,uid) values('%s','%s','%s')" %(pid,c,uid)
		cursor.execute(sql)
		html="<script>alert('send !!!!!! ');window.location='/comments?id=%s';</script>"%(pid)
	return HttpResponse(html)
def reviewinsert(request):
	cursor=connection.cursor()
	hid=request.POST['hid']
	review=request.POST['revi']

	sql4="insert into review(hid,review) values('%s','%s')"%(hid,review)  
	cursor.execute(sql4)
	#---------------
	cursor.execute("select * from review where hid='%s'"%(hid))
	result=cursor.fetchall()
	list=[]
	review=''
	if cursor.rowcount>0:
		for row in result:
			review =review+' ' +row[2]
	sql2="truncate table postag"
	cursor.execute(sql2)
	tokenized = sent_tokenize(review) 
	for i in tokenized: 
		wordsList1 = nltk.word_tokenize(i) 
		wordsList = [w for w in wordsList1 if not w in stop_words] 
		tagged1 = nltk.pos_tag(wordsList)
		tagged=( [(word, tag) for word, tag in tagged1 if ( tag=='NN' or tag=='NNS' or  tag=='NNP' or tag=='NNPS' or tag=='JJ' or tag=='JJR'or  tag=='JJS'   or tag=='VB'or tag=='VBD' or tag=='VBG' or tag=='VBN' or tag=='VBP'or tag=='VBZ')])		
		for f,g in tagged1:
			sql="insert into postag(data) values('%s')"%(f)
			cursor.execute(sql)
	you=[]
	sql3 = "select * from postag"
	cursor.execute(sql3)
	result1 = cursor.fetchall()
	for row1 in result1:
			d = row1[1]
			you.append(d)	
	sentence=' '.join(you) 	
	
	
	#------
	ps = PorterStemmer() 
	words = word_tokenize(sentence) 
	w1=[]
	w2=''
	sql2="truncate table stemming"
	cursor.execute(sql2)
	for w in words:
		sql="insert into stemming(data) values('%s')"%(ps.stem(w))
		cursor.execute(sql)
		w1.append(ps.stem(w))
		print(w, " : ", ps.stem(w)) 
	w2=' '.join(w1)
	#---
	sql2="truncate table pword"
	cursor.execute(sql2)
	sql3 = "select * from stemming"
	cursor.execute(sql3)
	result = cursor.fetchall()
	for row in result:
		sql3 = "select * from positive"
		cursor.execute(sql3)
		result1 = cursor.fetchall()
		for row1 in result1:
			if(row[1]==row1[1]):
				sql="insert into pword(pword) values('%s')"%(row[1])
				cursor.execute(sql)
	sqlp="select * from pword "
	cursor.execute(sqlp)
	c1=cursor.fetchall()
	p=[]
	for r in c1:
		f={'data':r[1]}
		p.append(f)
	#--
	sql2="truncate table nword"
	cursor.execute(sql2)
	sql3 = "select * from stemming"
	cursor.execute(sql3)
	result = cursor.fetchall()
	for row in result:
		sql3 = "select * from negative"
		cursor.execute(sql3)
		result1 = cursor.fetchall()
		for row1 in result1:
			if(row[1]==row1[1]):
				sql="insert into nword(nword) values('%s')"%(row[1])
				cursor.execute(sql)
	sqlp="select * from nword "
	cursor.execute(sqlp)
	c1=cursor.fetchall()
	p=[]
	for r in c1:
		f={'data':r[1]}
		p.append(f)
	#--
	sqlp="select count(*) from pword "
	cursor.execute(sqlp)
	p1=cursor.fetchall()
	pcount=0
	for r in p1:
		pcount=r[0]
	sqlp="select count(*) from nword "
	cursor.execute(sqlp)
	n1=cursor.fetchall()
	ncount=0
	for r in n1:
		ncount=r[0]
	if pcount!=0 and ncount!=0:
		count = float(pcount) + float(ncount)
		sentiscore = (float(pcount) -float(ncount)) / (float(pcount) + float(ncount));
		avgcount = sentiscore / float(count)
		#return HttpResponse(avgcount)
		if (avgcount > 0.25):
			sentilabel = 4
			snt1="Best Performing"
		elif (avgcount < 0.25 and  avgcount>0.00):
			sentilabel = 3
			snt1="(Good)"
		elif (avgcount ==-0.25):
			sentilabel = 1
			snt1="(Fair)"
		elif (avgcount <0.25):
			sentilabel = 0
			snt1="(Bad)"
		else:
			sentilabel=2
			snt1="(Average)"
		re="the area review  belongs to level  "+str(sentilabel)+ ' '+snt1
		data=[]
		w2={'data':re}
		data.append(w2)
		sql11 = "select * from scoretbl where hid='%s'" %(hid)
		cursor.execute(sql11)
		if cursor.rowcount >0:
			sql7="update  scoretbl set  score='%s',avg='%s',review='%s' where hid='%s'"%(sentiscore,avgcount,snt1,hid)  
			cursor.execute(sql7)
		else:
			sql6="insert into scoretbl(hid,score,avg,review) values('%s','%s','%s','%s')"%(hid,sentiscore,avgcount,snt1)  
			cursor.execute(sql6)
	html="<script>alert('send!!!!!! ');window.location='/review/';</script>"
	return HttpResponse(html)	
		





		
	
	
def index(request):
    return render(request,'index.html')

def Registration(request):
    return render(request,'Registration.html')
def login(request):
    return render(request,'index.html')

def page(request):
    return render(request,'page.html')

def caretakerHome(request):
    return render(request,'caretakerHome.html')

def regaction(request):
    cursor=connection.cursor()
    name=request.GET['Name']
    mob=request.GET['Mob']
    g=request.GET['gender']
    email=request.GET['Email']
    dob=request.GET['Dob']
    password=request.GET['Password']
    u='user'
    sql="insert into registration(name,gender,email,dob,mob,password) values('%s','%s','%s','%s','%s','%s')" %(name,g,email,dob,mob,password)
    cursor.execute(sql)
    s2="select max(id) as uid from registration"
    cursor.execute(s2)
    rs=cursor.fetchall()
    for row in rs:
        sql1="insert into login(uid,loginid,password,utype) values('%s','%s','%s','%s')" %(row[0],email,password,u)
        cursor.execute(sql1)
    msg="<script> alert('successfull');window.location='/index/';</script>"
    return HttpResponse(msg)
def care(request):
    return render(request,'care.html')
def caaction(request):
    cursor=connection.cursor()
    name=request.GET['Name']
    mob=request.GET['Mob']
    g=request.GET['gender']
    email=request.GET['Email']
    dob=request.GET['Dob']
    password=request.GET['Password']
    c='caretaker'
    sql="insert into caretkr(name,gender,email,dob,mob,password) values('%s','%s','%s','%s','%s','%s')" %(name,g,email,dob,mob,password)
    cursor.execute(sql)

    sql1="insert into login(loginid,password,utype) values('%s','%s','%s')" %(email,password,c)
    cursor.execute(sql1)
    msg="<script> alert('successfull');window.location='/care/';</script>"
    return HttpResponse(msg)
def profileimage(uid):
	cursor=connection.cursor()
	ss="select p_image from p_image where pid=(select max(pid) from p_image where uid='%s')"%(uid)
	cursor.execute(ss)
	rss=cursor.fetchall()
	list1=[]
	for row5 in rss:
		y={'p_image':row5[0]}
		list1.append(y)
	return list1
def postfriend(request):
	cursor=connection.cursor()
	sql1="select * from postadd where id in(select id from postadd where userid in (select fid from request where uid='%s' and status='approved')) order by date desc" %(request.session['loginid'])
	cursor.execute(sql1)
	res=cursor.fetchall()
	list2=[]
	for row2 in res:
		z={'id':row2[0],'post':row2[1],'userid':row2[2],'nme':row2[3],'date':row2[4],'post_image':row2[5]}
		list2.append(z)
	#return HttpResponse(list2)
	return list2
def userhome(request):
    cursor = connection.cursor()
    list2 = postfriend(request)
    ss = "select * from registration where email='%s'" % (request.session['loginid'])
    cursor.execute(ss)
    rss = cursor.fetchall()
    list1 = []
    for row5 in rss:
        y = {'name': row5[1], 'email': row5[3]}
        list1.append(y)
    pimage = profileimage(request.session['loginid'])
    return render(request, 'userhome.html', {'list1': list1, 'list2': list2, 'uid': request.session['loginid'], 'pimage': pimage})
def friends(request):
    cursor = connection.cursor()
    q = "select * from registration where email!='%s' and email not in (select fid from request where uid='%s')" % (request.session['loginid'], request.session['loginid'])
    cursor.execute(q)
    # return HttpResponse(q)
    qq = cursor.fetchall()
    usq = []
    for row2 in qq:
        qqq = {'id': row2[0], 'name': row2[1], 'email': row2[3]}
        usq.append(qqq)
    return usq
def postadd(request):
    cursor=connection.cursor()
    s="select name,email from registration where email='%s'"%(request.session['loginid'])
    cursor.execute(s)
    print(s)
    #return HttpResponse(s)
    rs=cursor.fetchall()
    usr=[]
    for row in rs:
        y={'name':row[0],'email':row[1]}
        usr.append(y)
    
    sql1="select * from postadd where userid='%s'  order by date desc "%(request.session['loginid'])
    cursor.execute(sql1)
    res=cursor.fetchall()
    usrr=[]
    for row1 in res:
        z={'id':row1[0],'post':row1[1],'userid':row1[2],'nme':row1[3],'date':row1[4],'post_image':row1[5]}
        usrr.append(z)
    usq=friends(request)
    abc="select * from request where status='requested' and  fid='%s'"%(request.session['loginid'])
    cursor.execute(abc)
    cab=cursor.fetchall()
    cabb=[]
    for row2 in cab:
        zq={'rqid':row2[0],'uid':row2[1],'fid':row2[2],'name':row2[3],'uid_name':row2[5]}
        cabb.append(zq)
    
    xyz="select registration.name,registration.email from request inner join registration on request.uid=registration.email where request.status='approved' and  request.fid='%s'"%(request.session['loginid'])
    cursor.execute(xyz)
    pug=cursor.fetchall()
    pubg=[]
    for row3 in pug:
        qaw={'name':row3[0],'email':row3[1]}
        pubg.append(qaw)
    
    '''gp="select * from group_tbl where userid!='%s' "%(request.session['loginid'])
    cursor.execute(gp)
    gpp=cursor.fetchall()
    grop=[]
    for row4 in gpp:
        gppp={'id':row4[0],'groupname':row4[1],'adminname':row4[2],'mission':row4[3],'description':row4[4],'userid':row4[5]}
        grop.append(gppp)'''

    pimage=profileimage(request.session['loginid'])
    return render(request,'postadd.html',{'usr':usr,'usrr':usrr,'usq':usq,'cabb':cabb,'pubg':pubg,'pimage':pimage})#'grop':grop})

emotions_emoji_dict = {
    "Happy": "😊",
    "Sad": "😢",
    "Angry": "😠",
    "Neutral": "😐"
}

# Enhanced prediction functions
def predict_emotions(text):
    text = text.lower()
    if any(word in text for word in ["sad", "empty", "missing", "down", "heavy", "overwhelmed", "alone", "grey", "dull", "trapped", "sorrow", "weight"]):
        return "Sad"
    elif any(word in text for word in ["happy", "joy", "smile", "delight", "glad", "cheerful", "content", "pleased"]):
        return "Happy"
    elif any(word in text for word in ["angry", "furious", "rage", "mad", "irate", "annoyed", "frustrated"]):
        return "Angry"
    else:
        return "Neutral"

def get_prediction_proba(text):
    text = text.lower()
    if any(word in text for word in ["sad", "empty", "missing", "down", "heavy", "overwhelmed", "alone", "grey", "dull", "trapped", "sorrow", "weight"]):
        return [0.8, 0.1, 0.1]
    elif any(word in text for word in ["happy", "joy", "smile", "delight", "glad", "cheerful", "content", "pleased"]):
        return [0.1, 0.8, 0.1]
    elif any(word in text for word in ["angry", "furious", "rage", "mad", "irate", "annoyed", "frustrated"]):
        return [0.1, 0.1, 0.8]
    else:
        return [0.3, 0.3, 0.4]

# Function to add prediction details to the database
def add_prediction_details(pos, userid, nme, date, prediction):
    cursor = connection.cursor()
    
    # Correcting the SQL syntax and ensuring all fields are correctly addressed
    sql = """
    INSERT INTO postadd (pos, userid, nme, date, post_image, prediction,status)
    VALUES (%s, %s, %s, %s, %s, %s,%s)
    """
    
    # Assuming post_image is optional, hence using None
    cursor.execute(sql, [pos, userid, nme, date, None, prediction,'pending'])
    cursor.close()

def postaction(request):
    if request.method == "POST":
        MyProfileForm = pform(request.POST, request.FILES)
        p = request.POST.get('pos', '')
        q = request.POST.get('t1', '')
        z = request.POST.get('t2', '')
        l = datetime.now()

        if MyProfileForm.is_valid():
            profile = pmodel()
            profile.pos = MyProfileForm.cleaned_data["pos"]
            profile.userid = request.session["loginid"]
            profile.nme = z
            profile.date = l
            profile.post_image = MyProfileForm.cleaned_data["post_image"]
            profile.save()
        else:
            cursor = connection.cursor()
            im = 'null'
            sql = """
            INSERT INTO postadd (pos, userid, nme, date, post_image, prediction,status)
            VALUES (%s, %s, %s, %s, %s,'pending')
            """
            cursor.execute(sql, [p, q, z, l, im])
            cursor.close()

        if 'pos' in request.POST:
            pos = request.POST.get("pos", "")
            prediction = predict_emotions(pos)
            userid = request.session["loginid"]

            # Correct function call with 5 arguments
            add_prediction_details(p, userid, z, l, prediction)

            context = {
                "pos": pos,
                "prediction": prediction,
                "emoji_icon": emotions_emoji_dict[prediction],
                'userid': userid,
                'form': MyProfileForm
            }
            return render(request, "postadd.html", context)

        return HttpResponse("<script>alert('Successfully added!');window.location='/postadd/';</script>")
    else:
        MyProfileForm = pform()
        return render(request, "postadd.html", {'form': MyProfileForm})

def postimage(request):
    cursor=connection.cursor()
    s="select * from registration where email='%s'"%(request.session['loginid'])
    cursor.execute(s)
    #return HttpResponse(s)
    rs=cursor.fetchall()
    usr=[]
    for row in rs:
        y={'name':row[1],'email':row[3]}
        usr.append(y)
    
    sql1="select * from tbl_image where uid='%s' "%(request.session['loginid'])
    cursor.execute(sql1)
    res=cursor.fetchall()
    usrr=[]
    for row1 in res:
        z={'id':row1[0],'uid':row1[1],'uname':row1[2],'p_image':row1[3]}
        usrr.append(z)
    
    usq=friends(request)
    
    abc="select * from request where status='requested' and  fid='%s'"%(request.session['loginid'])
    cursor.execute(abc)
    cab=cursor.fetchall()
    cabb=[]
    for row2 in cab:
        zq={'rqid':row2[0],'uid':row2[1],'fid':row2[2],'name':row2[3],'uid_name':row2[5]}
        cabb.append(zq)
    
    xyz="select registration.name,registration.email from request inner join registration on request.uid=registration.email where request.status='approved' and  request.fid='%s'"%(request.session['loginid'])
    cursor.execute(xyz)
    pug=cursor.fetchall()
    pubg=[]
    for row3 in pug:
        qaw={'name':row3[0],'email':row3[1]}
        pubg.append(qaw)
    #return HttpResponse(pubg)
    '''gp="select * from group_tbl where userid!='%s' "%(request.session['loginid'])
    cursor.execute(gp)
    gpp=cursor.fetchall()
    grop=[]
    for row4 in gpp:
        gppp={'id':row4[0],'groupname':row4[1],'adminname':row4[2],'mission':row4[3],'description':row4[4],'userid':row4[5]}
        grop.append(gppp)'''

    pimage=profileimage(request.session['loginid'])
    return render(request,'postimage.html',{'usr':usr,'usrr':usrr,'usq':usq,'cabb':cabb,'pubg':pubg,'pimage':pimage})

def imgaction(request):
    if request.method == "POST":
        MyProfileForm = pform(request.POST, request.FILES)
        if MyProfileForm.is_valid():
            profile =pmodel()
            profile.uid = MyProfileForm.cleaned_data["uid"]
            profile.uname =request.POST["t2"]
            profile.p_image = MyProfileForm.cleaned_data["p_image"]
            profile.save()
            html = "<script>alert('successfully added! ');window.location='/postimage/';</script>"
            saved = True
    else:
        MyProfileForm = pform()
    return HttpResponse(html)
def profileimgaction(request):
    if request.method == "POST":
        MyProfileForm = sform(request.POST, request.FILES)
        if MyProfileForm.is_valid():
            profile =smodel()
            profile.uid = MyProfileForm.cleaned_data["uid"]
            profile.p_image = MyProfileForm.cleaned_data["p_image"]
            profile.save()
            html = "<script>alert('successfully added! ');window.location='/userhome/';</script>"
            saved = True
    else:
        MyProfileForm = pform()
    return HttpResponse(html)
def group(request):
    cursor=connection.cursor()
    ss="select * from registration where email='%s'"%(request.session['loginid'])
    cursor.execute(ss)
    res=cursor.fetchall()
    list1=[]
    for row5 in res:
        y={'name':row5[1],'email':row5[3]}
        list1.append(y)
    return render(request,'group.html',{'list1':list1})

def gaction(request):
    cursor=connection.cursor()
    groupname=request.GET['groupname']
    adminname=request.GET['adminname']
    mission=request.GET['mission']
    description=request.GET['description']
    u=request.GET['admail']
    sql="insert into group_tbl(groupname,adminname,mission,description,userid) values('%s','%s','%s','%s','%s')" %(groupname,adminname,mission,description,u)
    cursor.execute(sql)
    msg="<script> alert('successfull');window.location='/postadd/';</script>"
    return HttpResponse(msg)

def laction(request):
    cursor=connection.cursor()
    p=request.POST['lg']
    q=request.POST['p']
    sql2="select * from login where loginid='%s' and password='%s' " %(p,q)
    cursor.execute(sql2)
    result=cursor.fetchall()
    if (cursor.rowcount)>0:
        sql3="select * from login where loginid='%s' and password='%s' " %(p,q)
        cursor.execute(sql3)
        result1=cursor.fetchall()
        for row1 in result1:
            request.session['id']=row1[0]
            request.session['uid']=row1[1]
            request.session['loginid']=row1[2]
            request.session['utype']=row1[4]
        if(request.session['utype']=='admin'):
            return render(request,'adminhome.html')
        elif(request.session['utype']=='caretaker'):
            return render(request,'caretakerHome.html')
        elif(request.session['utype']=='user'):
            ss="select * from registration where email='%s'"%(request.session['loginid'])
            cursor.execute(ss)
            rss=cursor.fetchall()
            list1=[]
            for row5 in rss:
                y={'name':row5[1],'email':row5[3]}
                list1.append(y)
            uid=request.session['loginid']
            list2=postfriend(request)
            pimage=profileimage(request.session['loginid'])
            return render(request,'userhome.html',{'list1':list1,'list2':list2,'uid':request.session['loginid'],'pimage':pimage})
        else:
            html="<script>alert('invalid password and username');window.location='/login/';</script>"
            return HttpResponse(html)
    else:
        html="<script>alert('invalid password and username');window.location='/login/';</script>"
        return HttpResponse(html)

def adminhome(request):
    return render(request,'adminhome.html')

def viewreg(request):
    cursor=connection.cursor()
    s="select * from registration"
    cursor.execute(s)
    rs=cursor.fetchall()
    usr=[]
    for row in rs:
        y={'id': row[0],'name':row[1],'address':row[2],'email':row[3],'age':row[4],'dob':row[5],'mob':row[6]}
        usr.append(y)
    return render(request,'viewreg.html',{'usr':usr})
    
def viewpost(request):
    cursor=connection.cursor()
    s="select * from postadd"
    cursor.execute(s)
    rs=cursor.fetchall()
    stu=[]
    for row in rs:
        y={'post':row[0],'id':row[1],}
        stu.append(y)
    return render(request,'viewpost.html',{'stu':stu})

def maction(request):
    cursor=connection.cursor()
    t=request.GET['t1']
    m=request.GET['message']
    l=request.GET['t2']
    sql="insert into message_tbl(toadd,message,fromm) values('%s','%s','%s')" %(t,m,l)
    cursor.execute(sql)
    msg="<script> alert('successfull');window.location='/message/';</script>"
    return HttpResponse(msg)

def viewmessage(request):
    cursor=connection.cursor()
    s="select * from message_tbl"
    cursor.execute(s)
    rs=cursor.fetchall()
    stu=[]
    for row in rs:
        y={'id':row[0],'toadd':row[1],'message':row[2],}
        stu.append(y)
    return render(request,'viewmessage.html',{'stu':stu})

def req(request):
    cursor=connection.cursor()
    fid=request.GET['id']
    fd=request.GET['na']
    z=request.GET['zz']
    uid=request.session['loginid']
    stat="requested"
    sqll="select * from request where uid='%s' and fid='%s'" %(uid,fid)
    cursor.execute(sqll)
    if(cursor.rowcount>0):
        msg="<script> alert('already requested');window.location='/postadd/';</script>"
    else:
        sql="insert into request(fid,uid,name,status,uid_name) values('%s','%s','%s','%s','%s')" %(fid,uid,fd,stat,z)
        cursor.execute(sql)
        msg="<script> alert('Request Send Success');window.location='/postadd/';</script>"
    return HttpResponse(msg)

def accept(request):
    cursor=connection.cursor()
    fid=request.GET['id']
    id=request.GET['na']
    em=request.GET['em']
    nm=request.GET['nm']
    fm=request.GET['fm']
    stat="approved"
    sqll="update request set status='%s' where fid='%s' and rqid='%s'" %(stat,id,fid)
    cursor.execute(sqll)
    sql="insert into request(fid,uid,name,status,uid_name) values('%s','%s','%s','%s','%s')" %(em,request.session['loginid'],fm,'approved',nm)
    #return HttpResponse(sql)
    cursor.execute(sql)
    msg="<script> alert('friend Request Accepted');window.location='/postadd/';</script>"
    return HttpResponse(msg)

def groupreq(request):
    cursor=connection.cursor()
    gid=request.GET['id']
    gn=request.GET['na']
    uid=request.session['loginid']
    stat="requested"
    sqll="select * from grp_request where ujid='%s' and gid='%s' and gname='%s'" %(uid,gid,gn)
    cursor.execute(sqll)
    if(cursor.rowcount>0):
        msg="<script> alert('Already requested for join');window.location='/postadd/';</script>"
    else:
        sql="insert into grp_request(gid,ujid,gname,status) values('%s','%s','%s','%s')" %(gid,uid,gn,stat)
        cursor.execute(sql)
        msg="<script> alert('Request Send Success');window.location='/postadd/';</script>"
    return HttpResponse(msg)

def profile(request):
    cursor = connection.cursor()
    ss = "select * from registration where email='%s'" % (request.session['loginid'])
    cursor.execute(ss)
    res = cursor.fetchall()
    list1 = []
    for row5 in res:
        y = {'name': row5[1], 'email': row5[3]}
        list1.append(y)
    ss1 = "select * from profile where uid='%s'" % (request.session['loginid'])
    cursor.execute(ss1)
    res1 = cursor.fetchall()
    list2 = []
    for row in res1:
        y1 = {'id': row[0], 'relationship': row[1], 'education': row[2], 'work': row[3], 'name': row[4], 'uid': row[5], 'hobbies': row[6]}
        list2.append(y1)
    return render(request, 'profile.html', {'list1': list1, 'list2': list2})
def paction(request):
    cursor=connection.cursor()
    relationship=request.GET['st']
    education=request.GET['Education']
    work=request.GET['Work']
    nme=request.GET['name']
    mail=request.GET['mail']
    ho=request.GET['Hobbies']
    sql="insert into profile(relationship,education,work,name,uid,hobbies) values('%s','%s','%s','%s','%s','%s')" %(relationship,education,work,nme,mail,ho)
    cursor.execute(sql)
    msg="<script> alert('successfull');window.location='/postadd/';</script>"
    return HttpResponse(msg)
def pupaction(request):
    cursor=connection.cursor()
    relationship=request.GET['st']
    education=request.GET['Education']
    work=request.GET['Work']
    nme=request.GET['name']
    mail=request.GET['mail']
    ho=request.GET['Hobbies']
    sql="update profile set relationship='%s',education='%s',work='%s',name='%s',hobbies='%s' where uid='%s'" %(relationship,education,work,nme,ho,mail)
    cursor.execute(sql)
    msg="<script> alert('successfull');window.location='/postadd/';</script>"
    return HttpResponse(msg)
def viewprofile(request):
    cursor=connection.cursor()
    s="select * from profile"
    cursor.execute(s)
    rs=cursor.fetchall()
    usr=[]
    for row in rs:
        y={'id': row[0],'relationship':row[1],'education':row[2],'work':row[3],'hobbies':row[4],'tagline':row[5],}
        usr.append(y)
    return render(request,'viewprofile.html',{'usr':usr})

def pagen(request):
    cursor=connection.cursor()
    n=request.GET['n']
    d=request.GET['d']
    a=request.GET['a']
    sql="insert into paget(name,description,adminname) values('%s','%s','%s')" %(n,d,a)
    cursor.execute(sql)
    msg="<script> alert('successfull');window.location='/login/';</script>"
    return HttpResponse(msg)

def viewpage(request):
    cursor=connection.cursor()
    s="select * from paget"
    cursor.execute(s)
    rs=cursor.fetchall()
    usr=[]
    for row in rs:
        y={'id': row[0],'name':row[1],'description':row[2],'adminname':row[3],}
        usr.append(y)
    return render(request,'viewpage.html',{'usr':usr})

#user req confirm
def  urequest(request):
	cursor = connection.cursor()
	sql2="select * from registration inner join request on request.fid=registration.id where request.status='pending' "
	cursor.execute(sql2)
	result=cursor.fetchall()
	list=[]
	for row in result:   	 	 	
		w = {'aid' : row[0],'name': row[1],'address': row[2],'gender': row[3],'phone': row[4],'email': row[5],'exp': row[6]   }
		list.append(w)
	return render(request,'urequest.html', {'list': list})
    
def message(request):
    cursor=connection.cursor()
    s="select * from registration where email='%s'"%(request.session['loginid'])
    cursor.execute(s)
    #return HttpResponse(s)
    rs=cursor.fetchall()
    usr=[]
    for row in rs:
        y={'name':row[1],'email':row[3]}
        usr.append(y)
    
    sql1="select * from postadd where userid='%s'  order by date desc "%(request.session['loginid'])
    cursor.execute(sql1)
    res=cursor.fetchall()
    usrr=[]
    for row1 in res:
        z={'id':row1[0],'post':row1[1],'userid':row1[2],'nme':row1[3],'date':row1[4]}
        usrr.append(z)
    
    usq=friends(request)
    
    abc="select * from request where status='requested' and  fid='%s'"%(request.session['loginid'])
    cursor.execute(abc)
    cab=cursor.fetchall()
    cabb=[]
    for row2 in cab:
        zq={'rqid':row2[0],'uid':row2[1],'fid':row2[2],'name':row2[3],'uid_name':row2[5]}
        cabb.append(zq)
    
    xyz="select registration.name,registration.email from request inner join registration on request.fid=registration.email where   request.uid='%s' and request.fid in (select distinct(fid)  from request where uid='%s' and status='approved') "%(request.session['loginid'],request.session['loginid'])
    cursor.execute(xyz)
    #return HttpResponse(xyz)
    pug=cursor.fetchall()
    pubg=[]
    for row3 in pug:
        qaw={'name':row3[0],'email':row3[1]}
        pubg.append(qaw)
   
    pimage=profileimage(request.session['loginid'])
    return render(request,'message.html',{'usr':usr,'usrr':usrr,'usq':usq,'cabb':cabb,'pubg':pubg,'pimage':pimage})

def mssg(request):
    cursor=connection.cursor()
    id=request.GET['id']
    es="select * from registration where email='%s'"%(id)
    cursor.execute(es)
    #return HttpResponse(s)
    ress=cursor.fetchall()
    musr=[]
    for row8 in ress:
        y={'name':row8[1],'email':row8[3]}
        musr.append(y)
        
    s="select * from registration where email='%s'"%(request.session['loginid'])
    cursor.execute(s)
    #return HttpResponse(s)
    rs=cursor.fetchall()
    usr=[]
    for row in rs:
        y={'name':row[1],'email':row[3]}
        usr.append(y)
    
    sql1="select * from postadd where userid='%s'  order by date desc "%(request.session['loginid'])
    cursor.execute(sql1)
    res=cursor.fetchall()
    usrr=[]
    for row1 in res:
        z={'id':row1[0],'post':row1[1],'userid':row1[2],'nme':row1[3],'date':row1[4]}
        usrr.append(z)
    
    q="select * from registration where email!='%s'"%(request.session['loginid'])
    cursor.execute(q)
    qq=cursor.fetchall()
    usq=[]
    for row2 in qq:
        qqq={'id':row2[0],'name':row2[1],'email':row2[3]}
        usq.append(qqq)
    
    abc="select * from request where status='requested' and  fid='%s'"%(request.session['loginid'])
    cursor.execute(abc)
    cab=cursor.fetchall()
    cabb=[]
    for row2 in cab:
        zq={'rqid':row2[0],'uid':row2[1],'fid':row2[2],'name':row2[3],'uid_name':row2[5]}
        cabb.append(zq)
    
    xyz="select registration.name from request inner join registration on request.uid=registration.email where request.status='approved' and  request.fid='%s'"%(request.session['loginid'])
    cursor.execute(xyz)
    pug=cursor.fetchall()
    pubg=[]
    for row3 in pug:
        qaw={'name':row3[0]}
        pubg.append(qaw)
    
    gp="select * from group_tbl where userid!='%s' "%(request.session['loginid'])
    cursor.execute(gp)
    gpp=cursor.fetchall()
    grop=[]
    for row4 in gpp:
        gppp={'id':row4[0],'groupname':row4[1],'adminname':row4[2],'mission':row4[3],'description':row4[4],'userid':row4[5]}
        grop.append(gppp)
    
    id=request.GET['id']
    a=request.session['loginid']
    po="select * from message_tbl where toadd='%s' and fromm='%s' order by id desc"%(id,a)
    cursor.execute(po)
    pit=cursor.fetchall()
    pott=[]
    for row44 in pit:
        ad={'id':row44[0],'toadd':row44[1],'message':row44[2],'fromm':row44[3]}
        pott.append(ad)


    return render(request,'mssg.html',{'usr':usr,'usrr':usrr,'usq':usq,'cabb':cabb,'pubg':pubg,'grop':grop,'musr':musr,'pott':pott} )

def umsg(request):
    cursor = connection.cursor()
    es = "select * from message_tbl where (toadd='%s' and fromm='%s' ) or (toadd='%s' and fromm='%s')  order by  id desc " % (request.GET['id'], request.session['loginid'], request.session['loginid'], request.GET['id'])
    cursor.execute(es)
    # return HttpResponse(es)
    re1 = cursor.fetchall()
    list = []
    for r1 in re1:
        w = {'id': r1[0],
             'toadd': r1[1],
             'message': r1[2],
             'fromm': r1[3],
             'reply': r1[4],
             'date': r1[5],
            }
        list.append(w)

    s = "select * from registration where email='%s'" % (request.GET['id'])
    cursor.execute(s)
    # return HttpResponse(s)
    rs = cursor.fetchall()
    usr = []
    for row in rs:
        y = {'name': row[1], 'email': row[3]}
        usr.append(y)

    pimage = profileimage(request.GET['id'])
    return render(request, 'mssg.html', {'list': list, 'usr': usr, 's': request.session['loginid'], 'id': request.GET['id'], 'pimage': pimage})

def umsgaction(request):
	cursor=connection.cursor()
	msg=request.GET['t2']
	lid=request.GET['id']
	sql="insert into message_tbl(toadd,fromm,message,reply,date)  values('%s','%s','%s','%s','%s')"%(lid,request.session['loginid'],msg,'Nil',tms)
	cursor.execute(sql)
	h="<script> alert('send');window.location='/umsg?id=%s';</script>"%(lid)
	return HttpResponse(h)
def urplyaction(request):
	cursor=connection.cursor()
	id=request.GET['t1']
	rp=request.GET['t2']
	lid=request.GET['id']
	sql="update message_tbl set reply='%s'  where id='%s'"%(rp,id)
	#return HttpResponse(sql)
	cursor.execute(sql)
	h="<script> alert('send');window.location='/umsg?id=%s';</script>" %(lid)
	return HttpResponse(h)

def delpost(request):
    cursor=connection.cursor()
    id=request.GET['id']
    sql="delete from postadd where id='%s' "%(id)
    cursor.execute(sql)
    msg="<script>window.location='/postadd/';</script>"
    return HttpResponse(msg)

def delimg(request):
    cursor=connection.cursor()
    id=request.GET['id']
    sql="delete from tbl_image where id='%s' "%(id)
    cursor.execute(sql)
    msg="<script>window.location='/postimage/';</script>"
    return HttpResponse(msg)

def viewUsers(request):
    cursor=connection.cursor()
    q="select * from registration"
    cursor.execute(q)
    qq=cursor.fetchall()
    usq=[]
    for row2 in qq:
        qqq={'id':row2[0],'name':row2[1],'gender':row2[2],'email':row2[3],'dob':row2[4],'mob':row2[5]}
        usq.append(qqq)
    return render(request,'viewUsers.html',{'usq':usq})
from django.shortcuts import render
from django.db import connection

def viewUsersPost(request):
    cursor=connection.cursor()
    q="select * from postadd"
    cursor.execute(q)
    qq=cursor.fetchall()
    usq=[]
    for row2 in qq:
        qqq={'id':row2[0],'post':row2[1],'userid':row2[2],'nme':row2[3],'date':row2[4],'prediction':row2[6]}
        usq.append(qqq)
    q1="select * from caretkr"
    cursor.execute(q1)
    qq1=cursor.fetchall()
    cr=[]
    for row2 in qq1:
        qqq1={'id':row2[0],'name':row2[1],'gender':row2[2],'email':row2[3],'dob':row2[4],'mob':row2[5]}
        cr.append(qqq1)
    return render(request,'viewUsersPost.html',{'cr':cr,'usq':usq})


def delUpost(request):
    cursor=connection.cursor()
    id=request.GET['id']
    uid=request.GET['na']
    sql="delete from postadd where id='%s' and userid='%s' "%(id,uid)
    cursor.execute(sql)
    msg="<script>window.location='/viewUsersPost/';</script>"
    return HttpResponse(msg)

def delUserr(request):
    cursor=connection.cursor()
    id=request.GET['id']
    sql="delete from registration where email='%s' "%(id)
    cursor.execute(sql)
    sql1="delete from postadd  where userid='%s' "%(id)
    cursor.execute(sql1)
    sql2="delete from request  where uid='%s' "%(id)
    cursor.execute(sql2)
    sql3="delete from login  where loginid='%s' and utype='user' "%(id)
    cursor.execute(sql3)
    msg="<script>window.location='/viewUsers/';</script>"
    return HttpResponse(msg)
def unfriend(request):
	cursor=connection.cursor()
	uid=request.session['loginid']
	fid=request.GET['fid']
	'''sql1="update request set status='requested' where uid='%s' and fid='%s'" %(uid,fid)
	cursor.execute(sql1)
	sql2="update request set status='requested' where uid='%s' and fid='%s'" %(fid,uid)
	cursor.execute(sql2)'''
	sql1="delete from  request  where uid='%s' and fid='%s'" %(uid,fid)
	cursor.execute(sql1)
	sql2="delete from  request where uid='%s' and fid='%s'" %(fid,uid)
	cursor.execute(sql2)
	h="<script> alert('unfriend');window.location='/postadd/';</script>"
	return HttpResponse(h)
def vblock(request):
    cursor=connection.cursor()
    q="select * from block_user"
    cursor.execute(q)
    qq=cursor.fetchall()
    usq=[]
    for row2 in qq:
        qqq={'id':row2[0],'pid':row2[1],'coment':row2[2],'uid':row2[3]}
        usq.append(qqq)
    return render(request,'vblock.html',{'usq':usq})
def delblock(request):
    cursor=connection.cursor()
    id=request.GET['id']
    sql="delete from registration where email='%s' "%(id)
    cursor.execute(sql)
    sql1="delete from postadd  where userid='%s' "%(id)
    cursor.execute(sql1)
    sql2="delete from request  where uid='%s' "%(id)
    cursor.execute(sql2)
    sql3="delete from login  where loginid='%s' and utype='user' "%(id)
    cursor.execute(sql3)
    sql4="delete from block_user  where uid='%s' "%(id)
    cursor.execute(sql4)
    msg="<script>window.location='/vblock/';</script>"
    return HttpResponse(msg)
from datetime import datetime
import numpy as np
import pandas as pd
from django.shortcuts import render

emotions_emoji_dict = {
    "Happy": "😊",
    "Sad": "😢",
    "Angry": "😠",
    "Neutral": "😐"
}

# Enhanced prediction functions
def predict_emotions(text):
    text = text.lower()
    if any(word in text for word in ["sad", "empty", "missing", "down", "heavy", "overwhelmed", "alone", "grey", "dull", "trapped", "sorrow", "weight"]):
        return "Sad"
    elif any(word in text for word in ["happy", "joy", "smile", "delight", "glad", "cheerful", "content", "pleased"]):
        return "Happy"
    elif any(word in text for word in ["angry", "furious", "rage", "mad", "irate", "annoyed", "frustrated"]):
        return "Angry"
    else:
        return "Neutral"

def get_prediction_proba(text):
    text = text.lower()
    if any(word in text for word in ["sad", "empty", "missing", "down", "heavy", "overwhelmed", "alone", "grey", "dull", "trapped", "sorrow", "weight"]):
        return [0.8, 0.1, 0.1]
    elif any(word in text for word in ["happy", "joy", "smile", "delight", "glad", "cheerful", "content", "pleased"]):
        return [0.1, 0.8, 0.1]
    elif any(word in text for word in ["angry", "furious", "rage", "mad", "irate", "annoyed", "frustrated"]):
        return [0.1, 0.1, 0.8]
    else:
        return [0.3, 0.3, 0.4]

# Function to add prediction details to the database
# def add_prediction_details(prediction):
#     cursor = connection.cursor()
#     sql = "INSERT INTO postadd (prediction) VALUES (%s)"
#     cursor.execute(sql, [prediction])  # Convert list to string
#     cursor.close()

# def home(request):
#     if request.method == "POST":
#         raw_text = request.POST.get("raw_text", "")
#         prediction = predict_emotions(raw_text)
#         probability = get_prediction_proba(raw_text)
        
#         add_prediction_details(raw_text, prediction, np.max(probability), datetime.now())

#         context = {
#             "raw_text": raw_text,
#             "prediction": prediction,
#             "probability": probability,
#             "emoji_icon": emotions_emoji_dict[prediction]
#         }
#         return render(request, "home.html", context)
#     else:
#         return render(request, "home.html")

# def view_all_prediction_details():
#     cursor = connection.cursor()
#     cursor.execute("SELECT raw_text, prediction, probability, time_of_visit FROM prediction_details")
#     rows = cursor.fetchall()
#     cursor.close()
#     return rows

# def monitor(request):
#     context = {}
#     context['prediction_details'] = pd.DataFrame(view_all_prediction_details(), columns=['Rawtext', 'Prediction', 'Probability', 'Time_of_Visit'])
#     return render(request, "monitor.html", context)
def careview(request):
    cursor=connection.cursor()
    q="select * from caretkr"
    cursor.execute(q)
    qq=cursor.fetchall()
    usq=[]
    for row2 in qq:
        qqq={'id':row2[0],'name':row2[1],'gender':row2[2],'email':row2[3],'dob':row2[4],'mob':row2[5]}
        usq.append(qqq)
    return render(request,'careview.html',{'usq':usq})

def cVWork(request):
    cursor = connection.cursor()
    uid=request.session['loginid']
    print(uid)  
    sql="select a.aid,a.userid,a.cid,r.name from assign  as a inner join registration as r on a.userid=r.email where a.cid='%s'"%(uid)
    cursor.execute(sql)
    print(sql)
    rows=cursor.fetchall()
    cursor.close()
    return render(request,'cVWork.html',{'rows':rows})

def careview(request):
    cursor=connection.cursor()
    q="select * from caretkr"
    cursor.execute(q)
    qq=cursor.fetchall()
    usq=[]
    for row2 in qq:
        qqq={'id':row2[0],'name':row2[1],'mob':row2[2],'email':row2[3],'dob':row2[4],'gender':row2[5]}
        usq.append(qqq)
    return render(request,'careview.html',{'usq':usq})
def assign(request):
  
  cursor = connection.cursor()
  userid=request.GET['userid']
  id=request.GET['id']
  sql="insert into assign(userid,cid)values('%s','%s')"%(userid,id)
  cursor.execute(sql)
  
  h="<script> alert('assigned'); window.location='/viewUsersPost/'; </script>"
  return HttpResponse(h)
def assnCare(request):
    cursor = connection.cursor()
    uid=request.session['loginid']
    sql="select a.aid,a.userid,a.cid,c.name from assign  as a inner join caretkr as c on a.cid=c.email where a.userid='%s'"%(uid)
    cursor.execute(sql)
    rows=cursor.fetchall()
    cursor.close()
    return render(request,'assnCare.html',{'rows':rows})
def chat(request):
    cursor=connection.cursor()
    lid=request.GET['lid']
    uid=request.session['loginid']
    cd=today
    s="select * from chatm  inner join chats on chatm.chatid=chats.chatid where chatm.lid='%s' and chatm.uid='%s'"%(lid,uid)
    print(s)
    cursor.execute(s)
    rs=cursor.fetchall()
    alist=[]
    for r in rs:
        x={'chatid':r[0],'chatdate':r[3],'msg':r[5],'typ':r[6]}
        alist.append(x)
    return render(request,'chat.html',{'lid':lid,'uid':uid,'alist':alist})
def chataction(request):
    cursor=connection.cursor()
    uid=request.session['loginid']
    lid=request.GET['lid']
    msg=request.GET['msg']
    ss="select * from chatm where uid= '%s' and lid='%s' and chatdate='%s'"%(uid,lid,today)
    cursor.execute(ss)
    if(cursor.rowcount>0):
        ss="select max(chatid) as chatid from chatm"
        cursor.execute(ss)
        rss=cursor.fetchall()
        for row in rss:
            chid=row[0]
            sql="insert into chats(chatid,msg,typ)values('%s','%s','user')"%(chid,msg)
            cursor.execute(sql)
    else:
        sql1="insert into chatm(uid,lid,chatdate) values('%s','%s','%s')"%(uid,lid,today)
        cursor.execute(sql1)
        sql2="select max(chatid) as chatid from chatm"
        cursor.execute(sql2)
        output=cursor.fetchall()
        for row in output:
            sql1="insert into chats(chatid,msg,typ)values('%s','%s','user')"%(row[0],msg)
            cursor.execute(sql1)
    msg="<script>;window.location='/chat?lid="+lid+"';</script>"
    return HttpResponse(msg)
def lchat(request):
    cursor=connection.cursor()
    uid=request.GET['lid']
    lid=request.session['loginid']
    cd=today
    s="select * from chatm  inner join chats on chatm.chatid=chats.chatid where chatm.lid='%s' and chatm.uid='%s' order by chatdate asc"%(lid,uid)
    cursor.execute(s)
    print(s)
    rs=cursor.fetchall()
    alist=[]
    for r in rs:
        x={'chatid':r[0],'chatdate':r[3],'msg':r[5],'typ':r[6]}
        alist.append(x)
    return render(request,'lchat.html',{'uid':uid,'lid':lid,'alist':alist})
def lchataction(request):
    cursor=connection.cursor()
    uid=request.GET['uid']
    lid=request.session['loginid']
    msg=request.GET['msg']
    ss="select * from chatm where uid='%s' and lid='%s' and chatdate='%s'"%(uid,lid,today)
    print(ss)
    cursor.execute(ss)
    if(cursor.rowcount>0):
        ss="select max(chatid) as chatid from chatm"
        cursor.execute(ss)
        rss=cursor.fetchall()
        for row in rss:
            chid=row[0]
            sql="insert into chats(chatid,msg,typ)values('%s','%s','caretaker')"%(chid,msg)
            cursor.execute(sql)
    else:
        sql1="insert into chatm(lid,uid,chatdate) values('%s','%s','%s')"%(lid,uid,today)
        cursor.execute(sql1)
        sql2="SELECT max(chatid) as chatid from chatm"
        cursor.execute(sql2)
        output=cursor.fetchall()
        for row in output:
            sql1="insert into chats(chatid,msg,typ)values('%s','%s','caretaker')"%(row[0],msg)
            cursor.execute(sql1)
    msg="<script>;window.location='/lchat?lid="+uid+"';</script>"
    return HttpResponse(msg)
