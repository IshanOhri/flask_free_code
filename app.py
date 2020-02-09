from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
'''
Telling our app where database is located
//// - 4 forward slashes is an absolute path
/// - 3 slashes for relative path and everything gonna be stored in test.db file
'''
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db' 
db = SQLAlchemy(app)  # initialize database with setting from the app and then create model/class

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    def __repr__(self):
        return '<Task %r>' % self.id # we need a string function that returns everytime we create an element

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'

    else:
        task = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', task=task)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    update_task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        update_task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Unable to add that content'
            
    else:
        return render_template('update.html', task=update_task)

if __name__ == "__main__":
    app.run(debug=True)
