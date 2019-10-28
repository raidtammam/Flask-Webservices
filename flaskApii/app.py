import os

from flask import jsonify, Flask, render_template, request, json

# pip install simplejson
from werkzeug.security import generate_password_hash, check_password_hash
from flaskext.mysql import MySQL
# pip install flask-mysql

project_root = os.path.dirname(__name__)
template_path = os.path.join(project_root)

mysql = MySQL()
app = Flask(__name__)
# mysql configuration
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'flaskdb'
mysql.init_app(app)


@app.route('/')
def main_world():
    return render_template('index.html')


@app.route('/signup', methods=['POST'])
def signUp():
    # open connection

    # read request from UI
    _mapel = request.form['mapel']
    _guru = request.form['guru']
    _ruangan = request.form['ruangan']
    _rfid = request.form['rfid']
    

    if _mapel and _guru and _ruangan and _rfid:
        insert(_mapel, _guru, _ruangan, _rfid)
        # return json.dumps({'html':'<span>Data Inserted </span>'})
        return jsonify({'status': 'ok insert'})
    else:
        return jsonify({'status': 'fail insert'})


def insert(mapel, guru, ruangan, rfid):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(
        """INSERT INTO kelas (
                mapel,
                guru,
                ruangan,
                rfid
            ) 
            VALUES (%s,%s,%s,%s)""", (mapel, guru, ruangan, rfid))
    conn.commit()
    conn.close()


@app.route('/show')
def show():
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM kelas")
    data = cursor.fetchall()
    dataList = []
    if data is not None:
        for item in data:
            dataTempObj = {
                'id': item[0],
                'mapel': item[1],
                'guru': item[2],
                'kelas': item[3],
                'rfid' : item[4]
            }
            dataList.append(dataTempObj)
        return jsonify(dataList)
    else:
        return 'data kosong'


@app.route('/update/<id>', methods=['PUT'])
def update(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    result = cursor.execute("UPDATE guru SET guru = %s, mapel = %s, kelas = %s , rfid = %s WHERE id = %s",
                            (request.form['guru'], request.form['mapel'], request.form['kelas'], request.form['rfid'], int(id)))
    conn.commit()
    conn.close()
    if(result):
        return jsonify({'updated': 'true'})
    else:
        return jsonify({'updated': 'false'})


@app.route('/delete/<id>')
def delete(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    result = cursor.execute("DELETE FROM kelas WHERE id = %s", int(id))
    conn.commit()
    conn.close()
    if(result):
        return jsonify({'delete': 'true'})
    else:
        return jsonify({'delete': 'false'})


if __name__ == '__main__':
    app.run(debug=True)
