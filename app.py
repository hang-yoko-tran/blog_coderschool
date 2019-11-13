from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager
from werkzeug import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] =  'sqlite:///db.db' 
app.secret_key = 'My secret'

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)


class User(UserMixin, db.Model):
  id = db.Column(db.Integer, primary_key = True)
  email = db.Column(db.String(200), nullable=False, unique=True)
  username = db.Column(db.String(200), nullable=False)
  password = db.Column(db.String(200), nullable=False, unique=True)

  def set_password(self, password):
    self.password = generate_password_hash(password)

  def check_password(self, password):
    return check_password_hash(self.password, password)
    


class Blog(db.Model):
  id = db.Column(db.Integer, primary_key = True)
  title = db.Column(db.String(200), nullable=False)
  body = db.Column(db.String, nullable=False)
  author = db.Column(db.String(20), nullable=False)
  created = db.Column(db.DateTime, server_default=db.func.now()) 
  updated = db.Column(db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now()) 




db.create_all()


 
@app.route('/', methods=['POST','GET']) 
def root():
  if request.method == 'POST':
    # import code; code.interact(local=dict(globals(), **locals()))
    user = User.query.filter_by(email = request.form['email']).first()
    # return redirect(url_for('new_post'))

    if not user:
      user = User(email = request.form['email'], username= request.form['username'])
      user.set_password(request.form['password'])
      db.session.add(user)
      db.session.commit()
      flash('You have successfully signed up', 'success')
      return redirect(url_for('new_post'))
      

  return render_template('views/login.html')

@app.route('/newpost', methods=['GET','POST'])
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