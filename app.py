#To-doist Application

from flask import Flask, request, jsonify
import pymysql.cursors

app = Flask(__name__)

connection = pymysql.connect(host = 'localhost',
                             user = 'root', 
                             password = 'admin1234',
                             database = 'cpsc449',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

cur = connection.cursor()

#Checks if the table exists or not. If not creates one
table_creation_query = """
CREATE TABLE IF NOT EXISTS tasks (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL,
    status BOOLEAN NOT NULL DEFAULT FALSE
);
"""
cur.execute(table_creation_query)
connection.commit()

#Error handlers
@app.errorhandler(400)
def bad_request(e):
    return jsonify(error=str(e)), 400

@app.errorhandler(404)
def task_not_found(e):
    return jsonify(error=str(e)), 404

@app.errorhandler(500)
def error_1(e):
    return jsonify(error=str(e)), 500

@app.route("/create", methods = ["POST"])
def create():
    try:
        sql = "INSERT INTO tasks (title, status) VALUES (%s, %s)"
        taskslist = [('Task1', True) , ('Task2', False)]
        for task in taskslist:
            cur.execute(sql, task)
        connection.commit()
        return jsonify("Tasks Created"), 200
    except Exception as e:
        return jsonify("Not created", str(e)), 400

@app.route("/read", methods = ["GET"])
def read():
    try:
        sql = "SELECT * from tasks"
        cur.execute(sql)
        connection.commit()
        result = cur.fetchall()
        return jsonify(result)
    except Exception as e:
        return jsonify("No tasks found!", str(e)), 400

@app.route("/update/<int:task_id>", methods = ["POST"])
def update(task_id):
    try:
        sql = "UPDATE tasks SET title = %s, status = %s WHERE id = %s"
        cur.execute(sql, ('UpdatedTask', True, task_id))
        connection.commit()
        
        if cur.rowcount == 0:
            return jsonify("Task not found"), 404
        
        return jsonify("Task updated"), 200
    except Exception as e:
        connection.rollback()
        return jsonify("Error updating task", str(e)), 400
    
@app.route("/delete/<int:task_id>", methods= ["POST"])
def delete(task_id):
    try:
        sql = "DELETE FROM tasks WHERE id = %s"
        cur.execute(sql, (task_id, ))
        connection.commit()
        if cur.rowcount == 0:
            return jsonify("Task not found"), 404
        
        return jsonify("Task deleted"), 200
    except Exception as e:
        connection.rollback()
        return jsonify("Error deleting task", str(e)), 400

if __name__ == "__main__":
    app.run(debug=True)