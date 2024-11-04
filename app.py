from flask import Flask, render_template, jsonify, request
import json

app = Flask(__name__, template_folder='templates', static_folder='static')

highscores = None

with open('highscores.json', 'r') as f:
    try:
        highscores = json.load(f)
    except:
        print("Json failed to load from file, most likely empty, empty list created")
        highscores = []

def bubble_sort(arr):
    for n in range(len(arr) - 1, 0, -1):
        for i in range(n):
           if arr[i]['score'] < arr[i + 1]['score']:
                arr[i], arr[i + 1] = arr[i + 1], arr[i]

bubble_sort(highscores)

@app.route('/')
def index():
    return render_template('index.html', highscores=highscores)

@app.route('/add_score', methods=['POST'])
def add_score():
    found_entry = False
    did_replace = False
    name = request.form['name']
    score = int(request.form['score'])
    for entry in highscores:
        if entry['name'] == name:
            found_entry = True
            if score > entry['score']:
                entry['score'] = score
                did_replace = True
                break

    if not found_entry:
        highscores.append({'name': name, 'score': score})

    if not found_entry or did_replace:
        bubble_sort(highscores)
        with open('highscores.json', 'w') as f:
            json.dump(highscores, f, indent=4)
        return jsonify({'message': 'Score updated successfully!'})
    return jsonify({'message': 'Score not added, highscore is larger than new entry'})

@app.route('/get_highscores', methods=['GET'])
def get_highscores():
    bubble_sort(highscores)
    return jsonify(highscores)

if __name__ == '__main__':
    app.run(debug=True)
