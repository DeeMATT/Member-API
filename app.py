from flask import Flask, g, request, jsonify
from database import get_db
import json

app = Flask(__name__)

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

@app.route('/member', methods=['GET'])
def get_members():
    db = get_db()

    members_cur = db.execute('SELECT * FROM members')
    members = members_cur.fetchall()

    return_values = []
    for member in members:
        member_dict = {}
        member_dict['id'] = member[0]
        member_dict['name'] = member[1]
        member_dict['email'] = member[2]
        member_dict['level'] = member[3]

        return_values.append(member_dict)

    return jsonify({'members' : return_values})

@app.route('/member/<int:member_id>', methods=['GET'])
def get_member(member_id):
    db = get_db()

    member_cur = db.execute('SELECT id, name, email, level FROM members WHERE id = ?', [member_id])
    member = member_cur.fetchone()

    member_dict = {}
    member_dict['id'] = member[0]
    member_dict['name'] = member[1]
    member_dict['email'] = member[2]
    member_dict['level'] = member[3]

    return jsonify({'member' : member_dict})

@app.route('/member', methods=['POST'])
def add_member():
    new_member_data = request.get_json()

    name = new_member_data['name']
    email = new_member_data['email']
    level = new_member_data['level']

    db = get_db()
    db.execute('INSERT INTO members (name, email, level) VALUES (?, ?, ?)', [name, email, level])
    db.commit()

    member_cur = db.execute('SELECT id, name, email, level FROM members WHERE name = ?', [name])
    new_member = member_cur.fetchone()

    return jsonify({'member': {'id': new_member[0], 'name': new_member[1], 'email': new_member[2], 'level': new_member[3]}})

@app.route('/member/<int:member_id>', methods=['PUT', 'PATCH'])
def edit_member(member_id):
    update_data = request.get_json()
    db = get_db()    
    if request.method == 'PATCH':
        if 'name' in update_data.keys():
            db.execute('UPDATE members SET name = ? WHERE id = ?' , [update_data['name'], member_id])
            db.commit()
        if 'email' in update_data.keys():
            db.execute('UPDATE members SET email = ? WHERE id = ?' , [update_data['email'], member_id])
            db.commit()
        if 'level' in update_data.keys():
            db.execute('UPDATE members SET level = ? WHERE id = ?' , [update_data['level'], member_id])
            db.commit()

    elif request.method == 'PUT':
        name = update_data['name']
        email = update_data['email']
        level = update_data['level']

        db.execute('UPDATE members SET name = ?, email = ?, level = ? WHERE id = ?', [name, email, level, member_id])
        db.commit()

    edited_cur = db.execute('SELECT * FROM members WHERE id = ?', [member_id])
    member = edited_cur.fetchone()

    return jsonify(member= {'id': member[0], 'name': member[1], 'email': member[2], 'level': member[3]})

@app.route('/member/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    return 'This removes a member ID.'

if __name__ == '__main__':
    app.run(debug=True)
