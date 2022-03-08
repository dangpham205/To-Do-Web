from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
# nơi database sẽ đươc lưu
# /// là relative path
# //// là abs path

db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    deadline = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r> <Deadline %r>' % self.id

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        task_deadline = request.form['deadline']
        new_task = Todo(content=task_content, deadline=task_deadline)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue with the db'
    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was a problem deleting that task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task = Todo.query.get_or_404(id)
    if request.method == 'POST':
        task.content = request.form['content']
        task.deadline = request.form['deadline']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'Update failed'
    else:
        return render_template('update.html', task=task)

if __name__ == "__main__":
    app.run(debug=True)

# @app.route('/delete/<int:id>')
# def delete(id):
#     delete_task= Todo.query.get_or_404(id)
#     try:
#         db.session.delete(delete_task)
#         db.session.commit()
#         return redirect('/')
#     except:
#         return 'Cannot delete'
