from flask_restful import Resource, reqparse, fields, marshal_with
from application.database import db
from application.models import List, Card, User
from application.validation import BusinessValidationError
from datetime import date, timedelta, datetime


user_output_fields = {
	"UserID": fields.Integer,
	"Username": fields.String,
	"EmailID": fields.String,
	"Password": fields.String }
	
create_user_parser = reqparse.RequestParser()
#create_user_parser.add_argument('UserID')
create_user_parser.add_argument('Username')
create_user_parser.add_argument('EmailID')
create_user_parser.add_argument('Password')

update_user_parser = reqparse.RequestParser()
update_user_parser.add_argument('EmailID')
update_user_parser.add_argument('Password')

class UserAPI(Resource):
	@marshal_with(user_output_fields)
	def get(self, UserID):
		user = db.session.query(User).filter(User.UserID == UserID).first()
		if user is None:
			return '', 404
		else:
			return user, 200
	
	@marshal_with(user_output_fields)		
	def put(self, UserID):
		user = db.session.query(User).filter(User.UserID == UserID).first()
		if user is None:
			return '', 404
		
		args = update_user_parser.parse_args()
		EmailID = args.get("EmailID", None)
		Password = args.get("Password", None)
		print(EmailID, Password)
		if (not isinstance(EmailID, str) or ('@' not in EmailID)):
			raise BusinessValidationError(status_code = 400, error_code = "USER003", error_message = "EmailID should be a string and should be a valid Email ID.")
		if ((Password == None) or (not isinstance(Password, str))):
			raise BusinessValidationError(status_code = 400, error_code = "USER004", error_message = "Password is required and should be a string.")
		
		user.EmailID = EmailID
		user.Password = Password
		db.session.commit()
		return user, 200

	def delete(self, UserID):
		user = db.session.query(User).filter(User.UserID == UserID).first()
		if user is None:
			return '', 404
		else:
			db.session.delete(user)
			db.session.commit()
			return "", 200
	
	@marshal_with(user_output_fields)			
	def post(self):
		args = create_user_parser.parse_args()
		#UserID = args.get("UserID", None)
		Username = args.get("Username", None)
		EmailID = args.get("EmailID", None)
		Password = args.get("Password", None)
		
		user = db.session.query(User).filter(User.Username == Username).first()
		if user != None:
			return '', 409

		if ((Username == None) or (not isinstance(Username, str))):
			raise BusinessValidationError(status_code = 400, error_code = "USER002", error_message = "Username is required and should be a string.")
		if (not isinstance(EmailID, str) or ('@' not in EmailID)):
			raise BusinessValidationError(status_code = 400, error_code = "USER003", error_message = "EmailID should be a string and should be a valid Email ID.")
		if ((Password == None) or (not isinstance(Password, str))):
			raise BusinessValidationError(status_code = 400, error_code = "USER004", error_message = "Password is required and should be a string.")
		
		new_user = User(Username=Username, EmailID=EmailID, Password=Password)
		db.session.add(new_user)
		db.session.commit()
		return new_user, 201

list_output_fields = {
	"ListID": fields.Integer,
	"UserID": fields.Integer,
	"Name": fields.String,
	"Description": fields.String,
	"Created_time": fields.String }
	
create_list_parser = reqparse.RequestParser()
#create_list_parser.add_argument('ListID')
create_list_parser.add_argument('UserID')
create_list_parser.add_argument('Name')
create_list_parser.add_argument('Description')

update_list_parser = reqparse.RequestParser()
update_list_parser.add_argument('Name')
update_list_parser.add_argument('Description')

class ListAPI(Resource):
	@marshal_with(list_output_fields)
	def get(self, ListID):
		list_ = db.session.query(List).filter(List.ListID == ListID).first()
		if list_ is None:
			return '', 404
		else:
			return list_, 200
	@marshal_with(list_output_fields)	
	def put(self, ListID):
		list_ = db.session.query(List).filter(List.ListID == ListID).first()
		if list_ is None:
			return '', 404
		
		args = update_list_parser.parse_args()
		Name = args.get("Name", None)
		Description = args.get("Description", None)
		
		if ((Name == None) or (not isinstance(Name, str))):
			raise BusinessValidationError(status_code = 400, error_code = "LIST003", error_message = "Name is required and should be a string.")
		if not isinstance(Description, str):
			raise BusinessValidationError(status_code = 400, error_code = "LIST004", error_message = "Description should be a string.")
		
		list_.Name = Name
		list_.Description = Description
		db.session.commit()
		return list_, 200

	def delete(self, ListID):
		list_ = db.session.query(List).filter(List.ListID == ListID).first()
		if list_ is None:
			return '', 404
		else:
			db.session.delete(list_)
			db.session.commit()
			return "", 200
	
	@marshal_with(list_output_fields)			
	def post(self):
		args = create_list_parser.parse_args()
		#ListID = args.get("ListID", None)
		try:
			UserID = int(args.get("UserID", None))
		except:
			raise BusinessValidationError(status_code = 400, error_code = "LIST002", error_message = "UserID is required and should be a integer.")
		Name = args.get("Name", None)
		Description = args.get("Description", None)
		
		user = db.session.query(User).filter(User.UserID == UserID).first()
		if user == None:
			return '', 404
		
		'''if ((ListID == None) or (not isinstance(ListID, int))):
			raise BusinessValidationError(status_code = 400, error_code = "LIST001", error_message = "ListID is required and should be a integer.")'''
		
		if ((UserID == None) or (not isinstance(UserID, int))):
			raise BusinessValidationError(status_code = 400, error_code = "LIST002", error_message = "UserID is required and should be a integer.")
		if ((Name == None) or (not isinstance(Name, str))):
			raise BusinessValidationError(status_code = 400, error_code = "LIST003", error_message = "Name is required and should be a string.")
		if not isinstance(Description, str):
			raise BusinessValidationError(status_code = 400, error_code = "LIST004", error_message = "Description should be a string.")
		
		new_list = List(UserID=UserID, Name=Name, Description=Description,Created_time=str(date.today().strftime('%d/%m/%Y')))
		db.session.add(new_list)
		db.session.commit()
		return new_list, 201

card_output_fields = {
	"CardID": fields.Integer,
	"ListID": fields.Integer,
	"UserID": fields.Integer,
	"Title": fields.String,
	"Content": fields.String,
	"Deadline": fields.String,
	"Complete" : fields.String,
	"Created_time": fields.String,
	"Last_updated_time": fields.String,
	"Completed_time": fields.String }
	
create_card_parser = reqparse.RequestParser()
#create_card_parser.add_argument('CardID')
create_card_parser.add_argument('ListID')
create_card_parser.add_argument('Title')
create_card_parser.add_argument('Content')
create_card_parser.add_argument('Deadline')
create_card_parser.add_argument('Complete')

update_card_parser = reqparse.RequestParser()
update_card_parser.add_argument('ListID')
update_card_parser.add_argument('Title')
update_card_parser.add_argument('Content')
update_card_parser.add_argument('Deadline')
update_card_parser.add_argument('Complete')

class CardAPI(Resource):
	@marshal_with(card_output_fields)
	def get(self, CardID):
		card = db.session.query(Card).filter(Card.CardID == CardID).first()
		if card is None:
			return '', 404
		else:
			return card, 200
	
	@marshal_with(card_output_fields)
	def put(self, CardID):
		card = db.session.query(Card).filter(Card.CardID == CardID).first()
		if card is None:
			return '', 404
		
		args = update_card_parser.parse_args()
		try:
			ListID = int(args.get("ListID", None))
		except:
			raise BusinessValidationError(status_code = 400, error_code = "CARD002", error_message = "ListID is required and should be an integer.")
		Title = args.get("Title", None)
		Content = args.get("Content", None)
		Deadline = args.get("Deadline", None)
		try: 
			Complete = int(args.get("Complete", None))
		except:
			raise BusinessValidationError(status_code = 400, error_code = "CARD006", error_message = "Complete is required and should be a string having value 0 or 1.")
		
		list_ = db.session.query(List).filter(List.ListID==ListID).first()
		if list_ is None:
			return '',404
		
		if ((ListID == None) or (not isinstance(ListID, int))):
			raise BusinessValidationError(status_code = 400, error_code = "CARD002", error_message = "ListID is required and should be an integer.")
		if ((Title == None) or (not isinstance(Title, str))):
			raise BusinessValidationError(status_code = 400, error_code = "CARD003", error_message = "Title is required and should be a string.")
		if not isinstance(Content, str):
			raise BusinessValidationError(status_code = 400, error_code = "CARD004", error_message = "Content should be a string.")
		if ((Deadline == None) or (not isinstance(Deadline, str))):
			raise BusinessValidationError(status_code = 400, error_code = "CARD005", error_message = "Deadline is required and should be a string.")
		if ((Complete!=0) and (Complete!=1)):
			raise BusinessValidationError(status_code = 400, error_code = "CARD006", error_message = "Complete is required and should be a string having value 0 or 1.")
		
		time = str(date.today().strftime('%d/%m/%Y'))
		ctime = None
		if Complete == 1:
			ctime = time
		card.ListID = ListID
		card.Title = Title
		card.Content = Content
		card.Deadline = Deadline
		card.Complete = Complete
		card.Last_updated_time = time
		card.Completed_time = ctime
		db.session.commit()
		return card, 200
		
	def delete(self, CardID):
		card = db.session.query(Card).filter(Card.CardID == CardID).first()
		if card is None:
			return '', 404
		else:
			db.session.delete(card)
			db.session.commit()
			return "", 200
	
	@marshal_with(card_output_fields)	
	def post(self):
		args = create_card_parser.parse_args()
		#CardID = args.get("CardID", None)
		try:
			ListID = int(args.get("ListID", None))
		except:
			raise BusinessValidationError(status_code = 400, error_code = "CARD002", error_message = "ListID is required and should be a integer.")
		Title = args.get("Title", None)
		Content = args.get("Content", None)
		Deadline = args.get("Deadline", None)
		try:
			Complete = int(args.get("Complete", None))
		except:
			raise BusinessValidationError(status_code = 400, error_code = "CARD006", error_message = "Complete is required and should be an integer having value 0 or 1.")
		
		list_ = db.session.query(List).filter(List.ListID == ListID).first()
		if list_ == None:
			return '', 404
		print(Complete, type(Complete))
		time = str(date.today().strftime('%d/%m/%Y'))
		if Complete == 1:
			ctime = time
		elif Complete == 0:
			ctime = None
		
		'''if ((CardID == None) or (not isinstance(CardID, int))):
			raise BusinessValidationError(status_code = 400, error_code = "CARD001", error_message = "CardID is required and should be a integer.")'''
		if ((ListID == None) or (not isinstance(ListID, int))):
			raise BusinessValidationError(status_code = 400, error_code = "CARD002", error_message = "ListID is required and should be a integer.")
		if ((Title == None) or (not isinstance(Title, str))):
			raise BusinessValidationError(status_code = 400, error_code = "CARD003", error_message = "Title is required and should be a string.")
		if not isinstance(Content, str):
			raise BusinessValidationError(status_code = 400, error_code = "CARD004", error_message = "Content should be a string.")
		if ((Deadline == None) or (not isinstance(Deadline, str))):
			raise BusinessValidationError(status_code = 400, error_code = "CARD005", error_message = "Deadline is required and should be a string.")
		if ((Complete!=0) and (Complete!=1)):
			raise BusinessValidationError(status_code = 400, error_code = "CARD006", error_message = "Complete is required and should be an integer having value 0 or 1.")
		
		new_card = Card(ListID=ListID, UserID = list_.UserID, Title = Title, Content = Content, Deadline = Deadline, Complete = Complete, Created_time = time, Last_updated_time = time, Completed_time = ctime)
		db.session.add(new_card)
		db.session.commit()
		db.session.add(new_card)
		db.session.commit()
		return new_card, 201
