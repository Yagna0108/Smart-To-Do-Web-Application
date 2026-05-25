from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)

# MySQL Connection
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Asdfghjkl%40123@localhost/taskdb'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Task Table
class Task(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    task_name = db.Column(db.String(200), nullable=False)
    status = db.Column(db.String(50), default='Pending')


# Create Table Automatically
with app.app_context():
    db.create_all()


# Get Tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():

    tasks = Task.query.all()

    output = []

    for task in tasks:

        output.append({
            'id': task.id,
            'task_name': task.task_name,
            'status': task.status
        })

    return jsonify(output)


# Add Task
@app.route('/add-task', methods=['POST'])
def add_task():

    data = request.json

    new_task = Task(
        task_name=data['task_name']
    )

    db.session.add(new_task)
    db.session.commit()

    return jsonify({
        'message': 'Task Added Successfully'
    })


# Complete Task
@app.route('/complete-task/<int:id>', methods=['PUT'])
def complete_task(id):

    task = Task.query.get(id)

    if task:
        task.status = 'Completed'
        db.session.commit()

    return jsonify({
        'message': 'Task Completed'
    })


# Incomplete Task
@app.route('/incomplete-task/<int:id>', methods=['PUT'])
def incomplete_task(id):

    task = Task.query.get(id)

    if task:
        task.status = 'Incomplete'
        db.session.commit()

    return jsonify({
        'message': 'Task Incomplete'
    })
# Delete Task
@app.route('/delete-task/<int:id>', methods=['DELETE'])
def delete_task(id):

    task = Task.query.get(id)

    if task:
        db.session.delete(task)
        db.session.commit()

    return jsonify({
        'message': 'Task Deleted'
    })


# Undo Task → Back to Pending
@app.route('/undo-task/<int:id>', methods=['PUT'])
def undo_task(id):

    task = Task.query.get(id)

    if task:
        task.status = 'Pending'
        db.session.commit()

    return jsonify({
        'message': 'Task Moved Back To Pending'
    })


if __name__ == '__main__':
    app.run(debug=True)