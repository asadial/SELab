from flask import Flask, request, jsonify, make_response
import requests
import jwt

from db import run_migrations, close_connection, query_db

app = Flask(__name__)
jwt_secret_key = 'random secret'
create_profile_endpoint = 'http://localhost:5002/user/create-profile'


@app.before_first_request
def start_up():
    run_migrations()


@app.teardown_appcontext
def tear_down(exception):
    close_connection()


@app.route('/auth/sign-up', methods=['POST'])
def sign_up():
    username = request.json.get('username')
    password = request.json.get('password')
    email = request.json.get('email')
    phone = request.json.get('phone')
    # TODO: Validate this values

    response = requests.post(create_profile_endpoint, json={
        'username': username,
        'email': email,
        'phone': phone
    })

    if response.status_code != 201:
        return jsonify(response.json()), response.status_code

    query_db("""
            insert into auth_user(username, password)
            values (?, ?);
        """, args=(username, password), with_commit=True)

    return jsonify({}), 201


@app.route('/auth/sign-in', methods=['POST'])
def sign_in():
    username = request.json.get('username')
    password = request.json.get('password')
    # TODO: Validate this values

    user = query_db('select * from auth_user where username = ? and password = ?',
                    args=(username, password), one=True)
    if not user:
        return jsonify({"error": "You should enter correct username and password."}), 401

    token = jwt.encode(
        payload={"username": username},
        key=jwt_secret_key,
        algorithm="HS256"
    )

    response = make_response(jsonify({}))
    response.headers['Authorization'] = token
    return response


@app.route('/auth/get-username', methods=['GET'])
def get_username():
    token = request.headers.get('Authorization')
    if token is None:
        return jsonify({"error": "Authorization header is not available."}), 401

    data = jwt.decode(
        jwt=token,
        key=jwt_secret_key,
        algorithms=["HS256"]
    )

    if 'username' not in data:
        return jsonify({"error": "Authorization header is not valid."}), 401

    return jsonify({'username': data['username']}), 200


if __name__ == '__main__':
    app.run(port=5001)
