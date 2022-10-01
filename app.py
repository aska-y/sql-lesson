from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import datetime
import os

app = Flask(__name__)

def get_profile():
    conn = sqlite3.connect('profile.sqlite3')
    c = conn.cursor()
    prof_list = []
    for i in c.execute('select * from persons'):
    #    prof_dict = {'name':i[1],'age':i[2], 'sex':i[3]}
        prof_list.append({'id': i[0],'name':i[1],'age':i[2], 'sex':i[3]})
    conn.commit()
    conn.close()
    return prof_list


def update_profile(prof):
    conn = sqlite3.connect('profile.sqlite3')
    c = conn.cursor()
    c.execute('update persons set name=?, age=?, sex=? WHERE id=?', (prof['name'],prof['age'],prof['sex'],prof['id']))
    conn.commit()
    conn.close()


def create_profile(name, age, sex):
    conn = sqlite3.connect('profile.sqlite3')
    c = conn.cursor()
    c.execute('insert into persons (name, age, sex) values(?,?,?)', (name, age, sex))
    conn.commit()
    conn.close()

def delete_profile(id):
    conn = sqlite3.connect('profile.sqlite3')
    c = conn.cursor()
    c.execute('DELETE FROM persons WHERE id=?', (id,))
    conn.commit()
    conn.close()



@app.route('/')
def top():
    return redirect(url_for('profile'))

@app.route('/profile')
def profile():
    prof_dict = get_profile()
    dt_now = datetime.datetime.now()
    return render_template('profile.html', title = 'sql', user=prof_dict, time_stamp=dt_now)


@app.route('/edit/<int:id>')
def edit(id):
    prof_list = get_profile()
    prof_dict = list(filter(lambda x: x['id'] == id, prof_list))[0]
    dt_now = datetime.datetime.now()
    return render_template('edit.html', title ='sql', user=prof_dict, time_stamp = dt_now)


@app.route('/update/<int:id>', methods =['POST'])
def update(id):
    prof_list = get_profile()
    prof_dict = list(filter(lambda x : x['id'] == id, prof_list))[0]
    #prof_dictの値を変更
    prof_dict['name'] = request.form['name']
    prof_dict['age'] = request.form['age']
    prof_dict['sex'] = request.form['sex']
    update_profile(prof_dict)
    return redirect(url_for('profile'))


@app.route('/add')
def add():
    prof_dict = get_profile()
    return render_template('add.html', title = 'sql', user=prof_dict)


@app.route('/create', methods =['POST'])
def create():
    #POSTの値を取得
    name = request.form['name']
    age = request.form['age']
    sex = request.form['sex']
    create_profile(name, age, sex)
    return redirect(url_for('profile'))


@app.route('/delete/<int:id>', methods =['POST'])
def delete(id):
    prof_list = get_profile()
    prof_dict = list(filter(lambda x : x['id'] == id, prof_list))[0]
    delete_profile(id)
    return redirect(url_for('profile'))




if __name__ == '__main__':
    app.run(host = '0.0.0.0', port=5001, threaded=True)



