from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Blog(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	body = db.Column(db.String(200), nullable=False)
	title = db.Column(db.String(200), nullable=False)
	author = db.Column(db.String(200), nullable=False)
	
	def __repr__(self):
		return '<Blog %r>' % self.id

@app.route("/", methods=["POST", "GET"])
def home():		
	if request.method == "POST":
		blog_title = request.form["blog_title"]
		blog_body = request.form["blog_body"]
		blog_author = request.form["blog_author"]
	
		new_blog = Blog(title=blog_title, body = blog_body,
		  author = blog_author)
		
		try:
			db.session.add(new_blog)
			db.session.commit()
			return redirect('/')
		except:
			return 'There was an issue adding your task'
	else:
		blogs = Blog.query.all()
		return render_template("home.html", blogs = blogs)


@app.route("/blog/<int:id>/", methods=["POST", "GET"])
def blog_page(id):
	blog = Blog.query.get_or_404(id)
	if request.method == 'POST':
		blog.title = request.form['blog_title']
		try:
			db.session.commit()
			return redirect('/')
		except:
			return 'There was an issue updating your task'
	else:
		return render_template("blog.html/", blog = blog)
	
@app.route('/delete/<int:id>')
def delete(id):
	blog_to_delete = Blog.query.get_or_404(id)
	try:
		db.session.delete(blog_to_delete)
		db.session.commit()
		return redirect("/")
	except:
		return 'There was a problem deleting that task' 

@app.route("/new-blog")
def add_blog():
	return render_template("new_blog.html")
	
if __name__ == "__main__":
	app.run(debug=True)