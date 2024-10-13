from unittest import TestCase
from app import app
from flask import session

class FlaskTests(TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True

    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Boggle Game', response.data)

    def test_check_word_valid(self):
        with self.client:
            self.client.get('/')
            board = session.get('board')
            print("Generated board:", board)

            word = board[0][0]
            response = self.client.get(f'/check-word?word={word}')
            print("Valid word response:", response.json)
            self.assertEqual(response.json, {'result': 'ok'})

    def test_check_word_not_on_board(self):
        with self.client:
            self.client.get('/')
            board = session.get('board')
            print("Generated board:", board)

            response = self.client.get('/check-word?word=COW')
            print("Not on board response:", response.json)
            self.assertEqual(response.json, {'result': 'not-on-board'})

    def test_check_word_not_a_word(self):
        with self.client:
            self.client.get('/')
            response = self.client.get('/check-word?word=INVALIDWORD')
            self.assertEqual(response.json, {'result': 'not-a-word'})

    def test_post_score(self):
        with self.client:
            self.client.get('/')
            score = 10
            response = self.client.post('/post-score', json={'score': score})
            self.assertEqual(response.json, {
                'success': True,
                'data': {
                    'times_played': 1,
                    'high_score': score
                }
            })
