from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
# CORS(app, resources={r"/attractions/*": {"origins": "http://localhost:3000"}})

# Config MySQL
# app.config['MYSQL_UNIX_SOCKET'] = '/Applications/XAMPP/xamppfiles/var/mysql/mysql.sock'  
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'  
app.config['MYSQL_DB'] = 'travel'  
# app.config['MYSQL_PORT'] = 3306


mysql = MySQL(app)


# Routes
@app.route('/attractions', methods=['GET'])
def get_attractions():
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM attractions')
    data = cur.fetchall()
    cur.close()
    return jsonify(data)

@app.route('/attractions/<int:id>', methods=['GET'])
def get_attraction(id):
    cur = mysql.connection.cursor()
    cur.execute('SELECT * FROM attractions WHERE id = %s', (id,))
    data = cur.fetchone()
    cur.close()
    return jsonify(data)

@app.route('/attractions', methods=['POST'])
def add_attraction():
    name = request.json['name']
    detail = request.json['detail']

    cur = mysql.connection.cursor()
    cur.execute('INSERT INTO attractions (name, detail) VALUES (%s, %s)', (name, detail))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'Attraction added successfully'})

@app.route('/attractions/<int:id>', methods=['PUT'])
def update_attraction(id):
    name = request.json['name']
    detail = request.json['detail']

    cur = mysql.connection.cursor()
    cur.execute('UPDATE attractions SET name = %s, detail = %s WHERE id = %s', (name, detail, id))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'Attraction updated successfully'})

@app.route('/attractions/<int:id>', methods=['DELETE'])
def delete_attraction(id):
    cur = mysql.connection.cursor()
    cur.execute('DELETE FROM attractions WHERE id = %s', (id,))
    mysql.connection.commit()
    cur.close()

    return jsonify({'message': 'Attraction deleted successfully'})

if __name__ == '__main__':
    app.run(debug=True)
