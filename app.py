from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Student %r>' % self.name

def create_db():
    with app.app_context():
        db.create_all()

if __name__ == '__main__':
    create_db()


@app.route('/student', methods=['GET', 'POST'])
def student():
    if request.method == 'POST':
        
        name = request.json['name']
        age = request.json['age']
        student = Student(name=name, age=age)
        db.session.add(student)
        db.session.commit()
        return jsonify({'id': student.id, 'name': student.name, 'age': student.age})
    elif request.method == 'GET':
        students = Student.query.all()
        all_students = []
        for student in students:
            student_data = {}
            student_data['id'] = student.id
            student_data['name'] = student.name
            student_data['age'] = student.age
            all_students.append(student_data)
        return jsonify({'students': all_students})

@app.route('/student/<int:id>', methods=['GET'])
def get_student(id):
    student = Student.query.get(id)
    if student:
        return jsonify({'id': student.id, 'name': student.name, 'age': student.age})
    else:
        return jsonify({'error': 'Student not found'})

@app.route('/student/<int:id>', methods=['PUT'])
def update_student(id):
    student = Student.query.get(id)
    if student:
        student.name = request.json.get('name', student.name)
        student.age = request.json.get('age', student.age)
        db.session.commit()
        return jsonify({'id': student.id, 'name': student.name, 'age': student.age})
    else:
        return jsonify({'error': 'Student not found'})

@app.route('/student/<int:id>', methods=['DELETE'])
def delete_student(id):
    student = Student.query.get(id)
    if student:
        db.session.delete(student)
        db.session.commit()
        return jsonify({'result': 'Student deleted'})
    else:
        return jsonify({'error': 'Student not found'})



if __name__ == '__main__':
    app.run(debug=True)
