from flask import Flask, request, jsonify
from db import run_migrations, close_connection, query_db

app = Flask(__name__)


@app.before_first_request
def start_up():
    run_migrations()


@app.teardown_appcontext
def tear_down(exception):
    close_connection()


@app.route('/user/show-profile', methods=['GET'])
def show_profile():
    username = request.headers.get('User')
    if username:
        info = query_db('select * from profile where username=?', [username])
        if info:
            return jsonify(info), 200
        else:
            return jsonify({'error': 'Bad request.'}), 400
    else:
        return ({'error': 'Please login first.'}), 401


@app.route('/user/edit-profile', methods=['POST'])
def edit_profile():
    username = request.headers.get('User')
    if username:
        info = query_db('select * from profile where username=?', [username])
        if info:
            email = request.json.get('email')
            phone = request.json.get('phone')
            email = info.get('email') if email is None else email
            phone = info.get('phone') if phone is None else phone
            query_db('update profile set email=?, phone=? where username=?', [email, phone, username], with_commit=True)
            return jsonify({}), 200
        else:
            return jsonify({'error': 'Bad request.'}), 400
    else:
        return ({'error': 'Please login first.'}), 401


@app.route('/user/create-profile', methods=['POST'])
def create_profile():
    username = request.json.get('username')
    email = request.json.get('email')
    phone = request.json.get('phone')
    query_db("""
            insert into profile(username, email, phone, type)
            values (?, ?, ?, ?)
        """, [username, email, phone, 'client'], with_commit=True)
    return jsonify({}), 201


if __name__ == '__main__':
    app.run(port=5002)
