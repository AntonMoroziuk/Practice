from app import app, session
from flask import request
from news_mining_db.models import News
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
from flask_cors import CORS

CORS(app)

@app.route('/')
@app.route('/index')
def index():
	# Main UI for plagiarism detection
	return "Hello, World!"

@app.route('/database')
def database():
	# UI for database management
	return "Database"

@app.route('/check', methods=['POST'])
def check():
	if 'text' not in request.json:
		return {'Error': 'No text provided to check'}	

	text_to_check = request.json['text']

	original_texts = [item.text for item in session.query(News).all()]

	max_containment = 0
	title_id = 0
	for text in original_texts:
		vectorizer = CountVectorizer(analyzer='word', ngram_range=(1,4))
		ngram_arr = vectorizer.fit_transform([text, text_to_check]).toarray()
		intersection_list = np.amin(ngram_arr, axis=0)
		containment = np.sum(intersection_list) / np.sum(ngram_arr[0])
		if containment > max_containment:
			max_containment = containment
			title_id = text.id

	return {'Result': max_containment, 'Title_id': title_id}


@app.route('/database/texts', methods=['GET'])
def texts():
	return {'Result': [{'id': item.id, 'title': item.title, 'text': item.text} for item in session.query(News).all()]}

@app.route('/database/text/<text_id>', methods=['GET'])
def get_text(text_id):
	text = session.query(News).filter_by(id = text_id).first()
	if text is None:
		return {'Error': 'No such text'}
	print(text.text)
	return {'Result': {'id': text.id, 'title': text.title, 'text': text.text}}

@app.route('/database/text', methods=['POST'])
def add_text():
	if 'text' not in request.json:
		return {'Error': 'No text provided to add'}
	
	news = News(text=request.json['text'], title=request.json['title'])
	session.add(news)
	session.commit()
	return {'Result': 'Success'}

@app.route('/database/text/<text_id>', methods=['DELETE'])
def remove_text(text_id):

	session.query(News).filter_by(id = text_id).delete()
	session.commit()
	return {'Result': 'Success'}
