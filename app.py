from flask import Flask, render_template, redirect, request, url_for
from flask_sqlalchemy import SQLAlchemy

#####Database Configuration#####
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123qweasdzxc!@#@localhost/sandbox'
db = SQLAlchemy(app)
app.debug = True

#####Models######

class Post(db.Model):
	id = db.Column('id', db.Integer, primary_key=True)
	title = db.Column('title', db.String(90), unique=True)
	body = db.Column('body', db.Text(), unique=True)
	
	def __init__(self, title, body):
		self.title = title
		self.body = body

#####Views#######

#loop through posts
@app.route('/', methods=['POST', 'GET'])
def index():
	post = Post.query.order_by(Post.id.desc()).all()
	return render_template('index.html', post=post)

#select individual posts	
@app.route('/post/<int:post_id>', methods=['POST', 'GET'])
def select(post_id):
	post = Post.query.filter_by(id=post_id).first()
	return render_template('select.html', post=post)

#create posts
@app.route('/create', methods=['POST', 'GET'])
def create():
	if request.method == 'POST':
		post = Post(request.form['title'], request.form['body'])
		db.session.add(post)
		db.session.commit()
		return redirect(url_for('index'))
	return render_template('create.html')

#delete posts
@app.route('/post/<int:post_id>/delete-this-post_pw{GreenHillZone91}', methods=['POST', 'GET'])
def delete(post_id):
	post = Post.query.filter_by(id=post_id).first()
	db.session.delete(post)
	db.session.commit()
	return redirect(url_for('index'))
	
#edit posts
@app.route('/post/<int:post_id>/edit', methods=['POST', 'GET'])
def update(post_id):
	post = Post.query.filter_by(id=post_id).first()
	if request.method == 'POST':
		post.title = request.form['title']
		post.body = request.form['body']
		db.session.commit()
		return redirect(url_for('index'))
	return render_template('update.html', post=post)	
	
	
	

#####Start Server#####	
if __name__ == "__main__":
	app.run()
	
	
