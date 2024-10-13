from random import choice
import string

class Boggle:
    def __init__(self):
        self.words = self.read_dict("words.txt")

    def read_dict(self, dict_path):
        with open(dict_path) as dict_file:
            words = [w.strip() for w in dict_file]
        return words

    def make_board(self):
        return [[choice(string.ascii_uppercase) for _ in range(5)] for _ in range(5)]

    def check_valid_word(self, board, word):
        word_exists = word in self.words
        valid_word = self.find(board, word.upper())
        if word_exists and valid_word:
            return "ok"
        elif word_exists:
            return "not-on-board"
        else:
            return "not-a-word"


    def find(self, board, word):
        for y in range(5):
            for x in range(5):
                if self.find_from(board, word, y, x, seen=set()):
                    return True
        return False

    def find_from(self, board, word, y, x, seen):
        if x < 0 or y < 0 or x >= 5 or y >= 5:
            return False
        if board[y][x] != word[0] or (y, x) in seen:
            return False
        if len(word) == 1:
            return True

        seen = seen | {(y, x)}

        for dy, dx in [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]:
            if self.find_from(board, word[1:], y + dy, x + dx, seen):
                return True

        return False
