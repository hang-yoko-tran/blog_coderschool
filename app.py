from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =  'sqlite:///db.db' 


db = SQLAlchemy(app)


class Blog(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  title = db.Column(db.String(200), nullable=False)
  body = db.Column(db.String, nullable=False)
  author = db.Column(db.String(20), nullable=False)
  created = db.Column(db.DateTime, server_default=db.func.now()) 
  updated = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now()) 

db.create_all()



@app.route('/')

@app.route('/', methods=['GET','POST'])
def new_post(): 
  if request.method == "POST":
    new_blog = Blog(title=request.form['title'], 
                    body=request.form['body'],
                    author=request.form['author'])
    db.session.add(new_blog)
    db.session.commit()
    return redirect(url_for('new_post'))
  
  posts = Blog.query.all() 
  return render_template('views/index.html', posts = posts)


@app.route('/blogs/<id>', methods=['GET','POST']) 
def delete_entry(id):
  if request.method == "POST" : 
    post = Blog.query.filter_by(id=id).first() 
    if not post: 
      return "THERE IS NO SUCH POST"
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('new_post')) 
  return "NOT ALLOWED" 






if __name__ == '__main__':
  app.run(debug=True)