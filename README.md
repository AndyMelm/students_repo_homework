This is a readme file.

let's start with app.py:

app.py is a python folder for Flask app.

app.py has imports like:

<!-- from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS -->

also it has SQLALCHEMY config:

<!-- app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///students.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
CORS(app) -->

Now, we create a database:

<!-- class Student(db.Model):
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
 -->

And, we got our CRUD methods:

First method to "get" the data from a server and to "Add" a new student.

<!-- @app.route('/student', methods=['GET', 'POST'])
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
        return jsonify({'students': all_students}) -->


The second method to "get" only a specific student with a unique ID:

<!-- @app.route('/student/<int:id>', methods=['GET'])
def get_student(id):
    student = Student.query.get(id)
    if student:
        return jsonify({'id': student.id, 'name': student.name, 'age': student.age})
    else:
        return jsonify({'error': 'Student not found'}) -->


The third method is to update a student using a unique ID:

<!-- @app.route('/student/<int:id>', methods=['PUT'])
def update_student(id):
    student = Student.query.get(id)
    if student:
        student.name = request.json.get('name', student.name)
        student.age = request.json.get('age', student.age)
        db.session.commit()
        return jsonify({'id': student.id, 'name': student.name, 'age': student.age})
    else:
        return jsonify({'error': 'Student not found'}) -->


The fourth method is to delete a student using a unique ID:

<!-- @app.route('/student/<int:id>', methods=['DELETE'])
def delete_student(id):
    student = Student.query.get(id)
    if student:
        db.session.delete(student)
        db.session.commit()
        return jsonify({'result': 'Student deleted'})
    else:
        return jsonify({'error': 'Student not found'})
 -->


Finally, we run the server:

<!-- if __name__ == '__main__':
    app.run(debug=True) -->


After we up and running with our flask app, we need to use index.html file to display all the functionality we created.

First, we added css bootsrap stylesheet link to head tag, to have more decorative flexabilty for our HTML pages.

<!-- <!DOCTYPE html>
<html>
<head>
    <title>Student Management System</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css">
</head> -->

Then, we built a div tag with container , labels and headers:

<!-- <body>
    <div class="container">
        <h2>Student Management System</h2>
        <div class="form-group">
            <label for="name">Name:</label>
            <input type="text" class="form-control" id="name">
        </div>
        <div class="form-group">
            <label for="age">Age:</label>
            <input type="number" class="form-control" id="age">
        </div> -->

We created a button to use "addStudent" function and created a table to display all existing students:

<!-- 
        <button type="submit" class="btn btn-primary" onclick="addStudent()">Add Student</button>
        <br><br>
        <table class="table table-striped">
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Age</th>
                    <th>Action</th>
                </tr>
            </thead>
            <tbody id="student-table">
            </tbody>
        </table>
    </div> -->

Added axios to body:
    <!-- <script src="https://unpkg.com/axios/dist/axios.min.js"></script> -->


Then, we built our fucntions in Javascript, to display, add, delete and update students:
    <!-- <script>
        function getStudents() {
            axios.get('http://127.0.0.1:5000/student')
            .then(response => {
                const students = response.data.students;
                const studentTable = document.getElementById('student-table');
                studentTable.innerHTML = '';
                students.forEach(student => {
                    const row = `<tr>
                        <td>${student.id}</td>
                        <td>${student.name}</td>
                        <td>${student.age}</td>
                        <td>
                            <button class="btn btn-primary" onclick="editStudent(${student.id})">Edit</button>
                            <button class="btn btn-danger" onclick="deleteStudent(${student.id})">Delete</button>
                        </td>
                    </tr>`;
                    studentTable.innerHTML += row;
                });
            })
            .catch(error => console.log(error));
        }
        function addStudent() {
            const name = document.getElementById('name').value;
            const age = document.getElementById('age').value;
            axios.post('http://127.0.0.1:5000/student', {
                name: name,
                age: age
            })
            .then(response => {
                console.log(response.data);
                getStudents();
                document.getElementById('name').value = '';
                document.getElementById('age').value = '';
            })
            .catch(error => console.log(error));
        }
        function deleteStudent(id) {
            axios.delete(`http://127.0.0.1:5000/student/${id}`)
            .then(response => {
                console.log(response.data);
                getStudents();
            })
            .catch(error => console.log(error));
        }
        function editStudent(id) {
            const name = prompt('Enter new name');
            const age = prompt('Enter new age');
            axios.put(`http://127.0.0.1:5000/student/${id}`, {
                name: name,
                age: age
            })
            .then(response => {
                console.log(response.data);
                getStudents();
            })
            .catch(error => console.log(error));
        }
        getStudents();
    </script></body></html> -->
