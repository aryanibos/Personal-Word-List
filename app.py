import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask, request, jsonify, render_template, redirect, url_for
from pymongo import MongoClient
import requests
from datetime import datetime

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)

db = client[DB_NAME]

app = Flask(__name__)



@app.route('/')
def main():
    words_result = db.words.find({}, {'_id': False})
    words = []
    for word in words_result:
        definition = word['definitions'][0]['shortdef']
        definition = definition if type(definition) is str else definition[0]
        words.append({
            'word': word['word'],
            'definition': definition,
        })
    return render_template('index.html', words=words)

@app.route('/detail/<keyword>')
def detail(keyword):
    api_key = '4e3d0a0c-f901-416e-ad42-e11b625b4320'
    url = f'https://www.dictionaryapi.com/api/v3/references/collegiate/json/{keyword}?key={api_key}'
    response = requests.get(url)
    definitions = response.json()

    # mengecek apakah keyword yang dicari tidak ditemukan
    if isinstance(definitions, list) and all(isinstance(item, str) for item in definitions):
        return render_template('error.html', word=keyword, suggestions=definitions)

    return render_template('detail.html', word=keyword, definitions=definitions, status=request.args.get('status_give', 'new'))

@app.route('/api/save_word', methods=['POST'])
def save_word():
    #  This handler should save the word in the database
    json_data = request.get_json()
    word = json_data.get('word_give')
    definitions = json_data.get('definitions_give')
    doc = {
        'word': word,
        'definitions': definitions,
        'date': datetime.now().strftime('%Y-%m-%d')
    }
    db.words.insert_one(doc)
    return jsonify({
        'result': 'success',
        'msg': f'the word, {word}, was saved!!!',
    })


@app.route('/api/delete_word', methods=['POST'])
def delete_word():
    #  This handler should delete the word from the database
    word = request.form.get('word_give')
    db.words.delete_one({'word': word})
    return jsonify({
        'result': 'success',
        'msg': f'the word {word} was deleted'
    })

@app.route('/praktik')
def praktik():
    return render_template('praktik.html')

if __name__ == '__main__':
    app.run('0.0.0.0', 5000, debug=True)

