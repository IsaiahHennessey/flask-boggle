from flask import Flask, render_template, session, request, jsonify
from boggle import Boggle

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'

boggle_game = Boggle()

@app.route('/')
def homepage():
    board = boggle_game.make_board()
    session['board'] = board
    session['times_played'] = session.get('times_played', 0)
    session['high_score'] = session.get('high_score', 0)
    return render_template('index.html', board=board)

@app.route('/check-word')
def check_word():
    word = request.args.get('word', '').lower()
    board = session.get('board')
    
    if board is None:
        return jsonify({'result': 'error', 'message': 'No board found in session'}), 400  

    result = boggle_game.check_valid_word(board, word)
    return jsonify({'result': result})

@app.route('/post-score', methods=['POST'])
def post_score():
    score = request.json.get('score')

    if score is None:
        return jsonify({'success': False, 'error': 'No score provided'}), 400

    try:
        score = int(score)
    except ValueError:
        return jsonify({'success': False, 'error': 'Invalid score'}), 400

    session['times_played'] += 1
    if score > session.get('high_score', 0):
        session['high_score'] = score

    return jsonify({
        'success': True,
        'data': {
            'times_played': session['times_played'],
            'high_score': session['high_score']
        }
    })

if __name__ == '__main__':
    app.run(debug=True)
