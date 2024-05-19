from flask import Flask, request, render_template, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId
from werkzeug.utils import secure_filename
from datetime import datetime
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

app = Flask(__name__)

@app.route('/', methods=['GET'])
def dashboard():
    fruits = list(db.fruits.find({}))
    return render_template('dashboard.html', fruits=fruits)

@app.route('/fruit', methods=['GET'])
def fruit():
    fruits = list(db.fruits.find({}))
    return render_template('fruit.html', fruits=fruits)

@app.route('/addfruit', methods=['GET', 'POST'])
def addfruit():
    if request.method=='POST':
        nama = request.form['nama']
        harga = request.form['harga']
        deskripsi = request.form['deskripsi']
        
        gambar = request.files['gambar']
        extension = gambar.filename.split('.')[-1]
        nama_gambar = gambar.filename.split('.')[0]
        mytime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        gambar_name = f'{nama_gambar}_{mytime}.{extension}'
        save_to = f'static/assets/Imagefruit/{gambar_name}'
        gambar.save(save_to)
        
        doc = {
            'nama': nama,
            'harga': harga,
            'deskripsi': deskripsi,
            'gambar': gambar_name,
        }
        
        db.fruits.insert_one(doc)
        
        return redirect(url_for('fruit'))

    return render_template('addfruit.html')

@app.route('/editfruit/<_id>', methods=['GET', 'POST'])
def editfruit(_id):
    if request.method=='POST':
        nama = request.form['nama']
        harga = request.form['harga']
        deskripsi = request.form['deskripsi']
        
        gambar = request.files['gambar']
        extension = gambar.filename.split('.')[-1]
        nama_gambar = gambar.filename.split('.')[0]
        mytime = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        gambar_name = f'{nama_gambar}_{mytime}.{extension}'
        save_to = f'static/assets/Imagefruit/{gambar_name}'
        gambar.save(save_to)
        
        doc = {
            'nama': nama,
            'harga': harga,
            'deskripsi': deskripsi,
        }
        if gambar:
            doc['gambar'] = gambar_name
        
        db.fruits.update_one({'_id': ObjectId(_id)}, {'$set': doc})
        
        return redirect(url_for('fruit'))
    
    id = ObjectId(_id)
    data = list(db.fruits.find({'_id': id}))
    return render_template('editfruit.html', data=data)

@app.route('/deletefruit/<_id>', methods=['GET', 'POST'])
def deletefruit(_id):
    id = ObjectId(_id)
    db.fruits.delete_one({'_id': id})
    return redirect(url_for('fruit'))

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)