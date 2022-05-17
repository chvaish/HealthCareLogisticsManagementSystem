import pymysql
from app import app
from db_config import mysql

from flask import jsonify
from flask import flash, request
from werkzeug.security import generate_password_hash, check_password_hash


#user controllers
@app.route('/user/add', methods=['POST'])
def add_user():
	conn = mysql.connect()
	cursor = conn.cursor()
	print("Conn")
	try:
		_json = request.json
		_firstName = _json['firstName']
		_lastName = _json['lastName']
		_email = _json['email']
		_password = _json['password']
		_userType = _json['userType']
		print(_json)
		if request.method == 'POST':
			_hashed_password = generate_password_hash(_password)
			sql = "INSERT INTO user_table(first_name, last_name, email_id, password, user_type) VALUES(%s, %s, %s, %s, %s )"
			data = (_firstName, _lastName, _email, _hashed_password, _userType)
			cursor.execute(sql, data)
			conn.commit()
			resp = jsonify('User added successfully!')
			resp.status_code = 200
			return resp
		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
@app.route('/users')
def users():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM user_table")
		rows = cursor.fetchall()
		resp = jsonify(rows)
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
@app.route('/user/<int:id>')
def user(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM user_table WHERE iduser=%s", id)
		row = cursor.fetchone()
		resp = jsonify(row)
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()

@app.route('/user/update', methods=['POST'])
def update_user():
	try:
		_json = request.json
		_iduser = _json['iduser']
		_firstName = _json['firstName']
		_lastName = _json['lastName']
		_email = _json['email']
		_password = _json['password']
		_userType = _json['userType']	
		if request.method == 'POST':
			_hashed_password = generate_password_hash(_password)
			sql = "UPDATE user_table SET first_name=%s, last_name=%s, email_id=%s, user_type=%s, password=%s WHERE iduser=%s"
			data = (_firstName, _lastName, _email, _userType, _hashed_password, _iduser)
			conn = mysql.connect()
			cursor = conn.cursor()
			cursor.execute(sql, data)
			conn.commit()
			resp = jsonify('User updated successfully!')
			resp.status_code = 200
			return resp
		else:
			return not_found()
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
@app.route('/user/delete/<int:id>')
def delete_user(id):
	try:
		conn = mysql.connect()
		cursor = conn.cursor()
		cursor.execute("DELETE FROM user_table WHERE iduser=%s", (id,))
		conn.commit()
		resp = jsonify('User deleted successfully!')
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
		
# default controllers
@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp
		
if __name__ == "__main__":
    app.run()
