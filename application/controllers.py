from flask import Flask, request, redirect, url_for
from flask import render_template
from flask import current_app as app
from application.models import User, List, Card
from .database import db
from datetime import date, timedelta, datetime
import matplotlib
from matplotlib import pyplot as plt
from matplotlib.figure import Figure
matplotlib.use('Agg')
plt.clf()

def daterange(date1, date2):
    for n in range(int ((date2 - date1).days)+1):
        yield date1 + timedelta(n)

@app.route("/")
def main():
    return render_template("main.html")

@app.route("/<username>")
def home(username):
    user = User.query.filter_by(Username=username).first()
    lists = List.query.filter_by(UserID=user.UserID).all()
    if lists==[]:
        return render_template("nolists.html",username = user.Username)
    else:
        c_cards = Card.query.filter_by(UserID=user.UserID, Complete="1")
        d_cards = Card.query.filter_by(UserID=user.UserID, Complete="0")
        return render_template("home.html",username = user.Username, lists = lists, dcards = d_cards, ccards = c_cards)

@app.route("/signup", methods = ['GET','POST'])
def signup():
    if request.method == 'GET':
        return render_template("signup.html")
    elif request.method == 'POST':
    	if '@' not in request.form['email']:
    		return render_template('invalidentries.html')
    	temp = User.query.filter_by(Username = request.form['username']).first()
    	if temp == None:
    		newuser = User(Username = request.form['username'], EmailID = request.form['email'], Password = request.form['password'])
    		db.session.add(newuser)
    		db.session.commit()
    		return redirect(url_for("home", username = request.form['username']))
    	else:
    		return render_template("userexists.html")

@app.route("/login", methods = ['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    elif request.method == 'POST':
        temp = User.query.filter_by(Username = request.form['username'], Password = request.form['password']).first()
        if temp==None:
            return render_template("invalidentries.html")
        else:
            return redirect(url_for("home",username=request.form['username']))

@app.route("/<username>/addlist", methods = ['GET','POST'])
def addlist(username):
    if request.method == 'GET':
        user = User.query.filter_by(Username=username).first()
        lists = List.query.filter_by(UserID=user.UserID).all()
        if len(lists)==5:
            return render_template("maxlists.html",username=username)
        return render_template("addlist.html",username=username)
    elif request.method == 'POST':
        user = User.query.filter_by(Username=username).first()
        list = List(UserID=user.UserID, Name=request.form['name'], Description=request.form['desc'], Created_time=str(date.today().strftime('%d/%m/%Y')))
        db.session.add(list)
        db.session.commit()
        return redirect(url_for("home",username = username))

@app.route("/<username>/editlist/<listid>", methods=['GET','POST'])
def editlist(username,listid):
    list = List.query.filter_by(ListID=listid).first()
    if request.method == 'GET':
        return render_template('editlist.html', username=username, list=list)
    elif request.method == 'POST':
        list.Name = request.form['name']
        list.Description = request.form['desc']
        db.session.commit()
        return redirect(url_for('home',username=username))

@app.route("/<username>/deletelist/<listid>")
def deletelist(username,listid):
    if request.method == 'GET':
        list = List.query.filter_by(ListID = listid).first()
        cards = Card.query.filter_by(ListID=listid).all()
        print(cards)
        if cards == []:
        	return render_template('deletelist3.html', username=username, listid=listid, listname=list.Name)
        else:
        	return render_template('deletelist1.html',username=username, listid=listid,listname=list.Name)

@app.route("/<username>/deletelistandcards/<listid>")
def deletelistandcards(username,listid):
    cards = Card.query.filter_by(ListID = listid).all()
    for card in cards:
        db.session.delete(card)
        print(card)
    list = List.query.filter_by(ListID = listid).first()
    db.session.delete(list)
    print("deleted successfully")
    db.session.commit()
    return redirect(url_for('home',username=username))

@app.route("/<username>/movecards/<listid>", methods=['GET','POST'])
def movecards(username, listid):
    cards = Card.query.filter_by(ListID = listid).all()
    list = List.query.filter_by(ListID = listid).first()
    if request.method == 'GET':
        user = User.query.filter_by(Username = username).first()
        lists = List.query.filter_by(UserID = user.UserID).all()
        lists.remove(list)
        return render_template("deletelist2.html",username=username, listid = listid, cards = cards, lists = lists)
    elif request.method =='POST':
        print("here")
        for card in cards:
            card.ListID = request.form[str(card.CardID)]
        db.session.delete(list)
        print("done")
        db.session.commit()
        return redirect(url_for('home',username=username))

@app.route("/<username>/<listid>/addcard", methods=['GET','POST'])
def addcard(username, listid):
    user = User.query.filter_by(Username=username).first()
    if request.method == 'GET':
        lists = List.query.filter_by(UserID=user.UserID).all()
        list = List.query.filter_by(ListID=listid).first()
        lists.remove(list)
        lists.insert(0,list)
        curr_date = str(date.today())
        return render_template('addcard.html', username=username, lists=lists, curr_date=curr_date)
    elif request.method == 'POST':
        time = str(date.today().strftime('%d/%m/%Y'))
        if request.form['complete'] == "1":
            ctime = time
        elif request.form['complete'] == "0":
            ctime = None
        x = (datetime.strptime(request.form['deadline'], '%Y-%m-%d').date()).strftime('%d/%m/%Y')
        newcard = Card(ListID = request.form['listid'], UserID = user.UserID, Title = request.form['title'], Content = request.form['content'], Deadline = x, Complete = request.form['complete'], Created_time = time, Last_updated_time = time, Completed_time = ctime)
        db.session.add(newcard)
        db.session.commit()
        return redirect(url_for('home',username=username))

@app.route("/<username>/editcard/<cardid>", methods=['GET','POST'])
def editcard(username,cardid):
    user = User.query.filter_by(Username=username).first()
    card = Card.query.filter_by(CardID = cardid).first()
    if request.method == 'GET':
        lists = List.query.filter_by(UserID=user.UserID).all()
        list = List.query.filter_by(ListID=card.ListID).first()
        lists.remove(list)
        lists.insert(0,list)
        curr_date = str(date.today())
        val = 0
        if card.Complete == 1:
            val = 1
        
        x = (datetime.strptime(card.Deadline, '%d/%m/%Y').date()).strftime('%Y-%m-%d')
        return render_template('editcard.html',username=username, card=card, lists=lists, val=val, curr_date = curr_date, ddate = x)
    elif request.method == 'POST':
        time = str(date.today().strftime('%d/%m/%Y'))
        ctime = None
        if request.form['complete'] == "1":
            ctime = time
        card.ListID = int(request.form['listid'])
        card.Title = request.form['title']
        card.Content = request.form['content']
        card.Deadline = (datetime.strptime(request.form['deadline'], '%Y-%m-%d').date()).strftime('%d/%m/%Y')
        card.Complete = str(request.form['complete'])
        card.Last_updated_time = time
        card.Completed_time = ctime
        db.session.commit()
        return redirect(url_for('home',username=username))

@app.route("/<username>/deletecard/<cardid>", methods=['GET','POST'])
def deletecard(username,cardid):
    card = Card.query.filter_by(CardID=cardid).first()
    if request.method == 'GET':
        return render_template('deletecard.html',username=username, card=card)
    elif request.method == 'POST':
        db.session.delete(card)
        db.session.commit()
        return redirect(url_for('home',username=username))

@app.route("/<username>/summary")
def summary(username):
    user = User.query.filter_by(Username = username).first()
    lists = List.query.filter_by(UserID = user.UserID).all()
    count = {}
    for list in lists:
        l = {}
        total_cards = Card.query.filter_by(ListID = list.ListID).all()
        l['total'] = len(total_cards)
        completed_cards = Card.query.filter_by(ListID = list.ListID, Complete = '1').all()
        l['c'] = len(completed_cards)
        not_completed_cards = Card.query.filter_by(ListID = list.ListID, Complete = '0', ).all()
        curr_date = str(date.today())
        l['pd'] = 0
        l['d'] = 0
        for card in not_completed_cards:
        	x = str(datetime.strptime(card.Deadline, '%d/%m/%Y').date())
       		if curr_date > x:
       			l['pd']+=1
       		else:
       			l['d']+=1
       	count[list.ListID] = l

        dates = []
        completed_card_count = []
        start_date = datetime.strptime(list.Created_time, '%d/%m/%Y').date()
        end_date = datetime.strptime(str(date.today().strftime('%d/%m/%Y')), '%d/%m/%Y').date()
        for x in daterange(start_date, end_date):
            x = x.strftime('%d/%m/%Y')
            dates.append(x[:5])
            cc = Card.query.filter_by(ListID=list.ListID, Completed_time = x).all()
            completed_card_count.append(len(cc))

        fig = plt.figure()
        fig.add_subplot(111)
        plt.bar(dates, completed_card_count)
        plt.savefig("static/"+str(list.ListID)+"_graph.png")
    
    return render_template("summary.html",username=username, lists=lists, count=count)



@app.route("/<username>/overallsummary")
def overallsummary(username):
    user = User.query.filter_by(Username = username).first()
    lists = List.query.filter_by(UserID = user.UserID).all()
    start_date=(datetime.strptime(lists[0].Created_time, '%d/%m/%Y').date())
    
    for list in lists:
    	x = (datetime.strptime(list.Created_time, '%d/%m/%Y').date())
    	if x < start_date:
    		start_date = x
    start_date = start_date.strftime('%d/%m/%Y')

    dates = []
    completed_card_count = []
    start_date = datetime.strptime(start_date, '%d/%m/%Y').date()
    end_date = datetime.strptime(str(date.today().strftime('%d/%m/%Y')), '%d/%m/%Y').date()
    for x in daterange(start_date, end_date):
        x = x.strftime('%d/%m/%Y')
        dates.append(x[:5])
        cc = Card.query.filter_by(UserID=user.UserID, Completed_time = x).all()
        completed_card_count.append(len(cc))

    fig = plt.figure()
    fig.add_subplot(111)
    plt.bar(dates, completed_card_count)
    plt.savefig("static/overall.png")
    
    return render_template("overallsummary.html",username=username)

@app.route("/account/<username>")
def account(username):
	user = User.query.filter_by(Username = username).first()
	return render_template("account.html",username=username, user=user)

@app.route("/editaccount/<username>", methods=['GET','POST'])
def editaccount(username):
	user = User.query.filter_by(Username = username).first()
	if request.method == 'GET':
		return render_template("editaccount.html",username=username, user=user)
	elif request.method == 'POST':
		if '@' not in request.form['email']:
			return render_template('invaliddetails.html', username=username)
		user.EmailID = request.form['email']
		user.Password = request.form['password']
		db.session.commit()
		return redirect(url_for('account',username=username))

@app.route("/deleteaccount/<username>", methods=['GET','POST'])
def deleteaccount(username):
	if request.method == 'GET':
		return render_template("deleteaccount.html",username=username)
	elif request.method == 'POST':
		user = User.query.filter_by(Username = username).first()
		db.session.delete(user)
		db.session.commit()
		return redirect(url_for('main'))

@app.route("/logout")
def logout():
    return redirect(url_for('main'))


