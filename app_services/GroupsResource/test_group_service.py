import unittest
from db import init_db, add_move, getMove, clear
from json import dumps


class Test_Testdb(unittest.TestCase):

    def test_initialize_db_twice(self):
        # Tests invalid attempt to initialize db twice

        # First clear the previously initialized db that
        # remains from Ctrl + C quitting the game
        successful_get_move, last_row = getMove()
        if last_row is not None or successful_get_move:
            clear()

        successful_get_move, last_row = getMove()
        if last_row is not None or successful_get_move:
            return "ERROR: Database failed to clear."

        successful_init = init_db()
        successful_init = init_db()

        self.assertEqual(successful_init, False)

    def test_add_before_initialized(self):
        # Tests invalid add_move() before db is initialized

        # First clear the previously initialized db that
        # remains from Ctrl + C quitting the game
        successful_get_move, last_row = getMove()
        if last_row is not None or successful_get_move:
            clear()

        successful_get_move, last_row = getMove()
        if last_row is not None or successful_get_move:
            return "ERROR: Database failed to clear."

        current_turn = "p1"
        board = dumps([[0 for x in range(7)] for y in range(6)])
        winner = ""
        player1 = "red"
        player2 = "yellow"
        remaining_moves = 42
        move = (current_turn, board, winner, player1, player2, remaining_moves)

        successful_add = add_move(move)

        self.assertEqual(successful_add, False)

    def test_valid_insert(self):
        # Tests for a valid insert into the db

        # First clear the previously initialized db that
        # remains from Ctrl + C quitting the game
        successful_get_move, last_row = getMove()
        if last_row is not None or successful_get_move:
            clear()

        successful_get_move, last_row = getMove()
        if last_row is not None or successful_get_move:
            return "ERROR: Database failed to clear."

        init_db()

        current_turn = "p1"
        board = dumps([[0 for x in range(7)] for y in range(6)])
        winner = ""
        player1 = "red"
        player2 = "yellow"
        remaining_moves = 42
        move = (current_turn, board, winner, player1, player2, remaining_moves)

        successful_add = add_move(move)

        self.assertEqual(successful_add, True)

        clear()

    def test_invalid_insert(self):
        # Tests an invalid insert. board is not string type

        # First clear the previously initialized db that
        # remains from Ctrl + C quitting the game
        successful_get_move, last_row = getMove()
        if last_row is not None or successful_get_move:
            clear()

        successful_get_move, last_row = getMove()
        if last_row is not None or successful_get_move:
            return "ERROR: Database failed to clear."

        init_db()
        current_turn = "p1"
        board = [[0 for x in range(7)] for y in range(6)]
        winner = ""
        player1 = "red"
        player2 = "yellow"
        remaining_moves = 42
        move = (current_turn, board, winner, player1, player2, remaining_moves)

        successful_add = add_move(move)
        self.assertEqual(successful_add, False)
        clear()

    def test_get_move_before_initialized(self):
        # Tests invalid attempt to get move before db is initialized

        # First clear the previously initialized db that
        # remains from Ctrl + C quitting the game
        successful_get_move, last_row = getMove()
        if last_row is not None or successful_get_move:
            clear()

        successful_get_move, last_row = getMove()
        if last_row is not None or successful_get_move:
            return "ERROR: Database failed to clear."

        successful_get_move, _ = getMove()
        self.assertEqual(successful_get_move, False)

    def test_get_move_on_empty_db(self):
        # Tests invalid attempt to get move when db table is empty

        # First clear the previously initialized db that
        # remains from Ctrl + C quitting the game
        successful_get_move, last_row = getMove()
        if last_row is not None or successful_get_move:
            clear()

        successful_get_move, last_row = getMove()
        if last_row is not None or successful_get_move:
            return "ERROR: Database failed to clear."

        init_db()
        successful_get_move, _ = getMove()
        self.assertEqual(successful_get_move, False)
        clear()

    def test_valid_get_move(self):
        # Tests valid getMove() attempt

        # First clear the previously initialized db that
        # remains from Ctrl + C quitting the game
        successful_get_move, last_row = getMove()
        if last_row is not None or successful_get_move:
            clear()

        successful_get_move, last_row = getMove()
        if last_row is not None or successful_get_move:
            return "ERROR: Database failed to clear."

        init_db()
        current_turn = "p1"
        board = dumps([[0 for x in range(7)] for y in range(6)])
        winner = ""
        player1 = "red"
        player2 = "yellow"
        remaining_moves = 42
        move = (current_turn, board, winner, player1, player2, remaining_moves)

        successful_add = add_move(move)

        self.assertEqual(successful_add, True)

        successful_get_move, _ = getMove()

        self.assertEqual(successful_get_move, True)

        clear()

    def test_clear_twice(self):
        # Tests invalid attempt to clear the db twice

        # First clear the previously initialized db that
        # remains from Ctrl + C quitting the game
        successful_get_move, last_row = getMove()
        if last_row is not None or successful_get_move:
            clear()

        successful_get_move, last_row = getMove()
        if last_row is not None or successful_get_move:
            return "ERROR: Database failed to clear."

        init_db()
        clear()
        successful_clear = clear()
        self.assertEqual(successful_clear, False)

    def test_clear_before_init(self):
        # Tests invalid attempt to clear db before db is initialized

        # First clear the previously initialized db that
        # remains from Ctrl + C quitting the game
        successful_get_move, last_row = getMove()
        if last_row is not None or successful_get_move:
            clear()

        successful_get_move, last_row = getMove()
        if last_row is not None or successful_get_move:
            return "ERROR: Database failed to clear."

        successful_clear = clear()
        self.assertEqual(successful_clear, False)


if __name__ == '__main__':
    unittest.main()
