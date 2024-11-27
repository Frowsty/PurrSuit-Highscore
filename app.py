from flask import Flask, render_template, jsonify, request
import json

app = Flask(__name__, template_folder='templates', static_folder='static')

token = "wjYXGWljQAegaPlQd0YohIdQ"
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
    if token != request.form['token']:
        return jsonify({'message': 'Invalid token'})
    name = request.form['name'].split('@')
    score = int(request.form['score'])
    for entry in highscores:
        if entry['name'].split('@')[1] == name[1]:
            if entry['name'].split('@')[0] != name[0]:
                did_replace = True
                entry['name'] = name[0] + '@' + name[1]
            found_entry = True
            if score > entry['score']:
                entry['score'] = score
                did_replace = True
                break

    if not found_entry:
        highscores.append({'name': name[0] + '@' + name[1], 'score': score})

    if not found_entry or did_replace:
        bubble_sort(highscores)
        with open('highscores.json', 'w') as f:
            json.dump(highscores, f, indent=4)
        return jsonify({'message': 'Score updated successfully!'})
    return jsonify({'message': 'Score not added, highscore is larger than new entry'})

@app.route('/get_highscores', methods=['GET'])
def get_highscores():
    bubble_sort(highscores)

    player_entry = None
    player_position = None

    if token != request.args.get('token', default='no token', type=str):
        return jsonify({'message': 'Invalid token'})

    limit = request.args.get('limit', default=len(highscores), type=int)
    limited_highscores = highscores[:limit]

    player_name = request.args.get('player_name', default='', type=str)
    if player_name:
        for entry in highscores:
            if entry['name'] == player_name:
                player_entry = entry
        
    if player_entry:
        player_position = highscores.index(player_entry)

    response = {
        "highscores": limited_highscores,
        "player_info": {
            "position": player_position,
            "entry": player_entry
        }
    }

    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True, host='195.181.245.221')
