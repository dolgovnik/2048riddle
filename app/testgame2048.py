import unittest

from game2048 import Game, GameField

class TestGame(unittest.TestCase):
    def setUp(self):
        self.game = Game(FakeGameField)

    def tearDown(self):
        del self.game

    def test_set_score(self):
        self.game.set_score(2048)
        self.assertEqual(self.game.score, 2048)

    def test_update_score(self):
        self.game._update_score(120)
        self.assertEqual(self.game.score, 120)

    def test_game_push_value(self):
        self.game.push_value()    
        self.assertIn(self.game.field.val, (2,4))

    def test_rotate_90(self):
        field_to_rotate = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
        result_rotate_90 = [[4, 8, 12, 16], [3, 7, 11, 15], [2, 6, 10 , 14], [1, 5, 9, 13]]
        self.game.field = FakeGameField(field_to_rotate)
        self.game._rotate_90()
        self.assertEqual(self.game.field.field, result_rotate_90)

    def test_rotate_180(self):
        field_to_rotate = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
        result_rotate_180 = [[4, 3, 2, 1], [8, 7, 6, 5], [12, 11, 10, 9], [16, 15, 14, 13]]
        self.game.field = FakeGameField(field_to_rotate)
        self.game._rotate_180()
        self.assertEqual(self.game.field.field, result_rotate_180)
        
    def test_rotate_270(self):
        field_to_rotate = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
        result_rotate_270 = [[13, 9, 5, 1], [14, 10, 6, 2], [15, 11, 7, 3], [16, 12, 8, 4]]
        self.game.field = FakeGameField(field_to_rotate)
        self.game._rotate_270()
        self.assertEqual(self.game.field.field, result_rotate_270)

    def test_slide_left(self):
        field_to_slide_left = [[2, 2, None, 4], [None, None, 2, 2], [2, None, 2, 4], [None, None, None, 2]]
        result_slide_left = [[4, 4, None, None], [4, None, None, None], [4, 4, None, None], [2, None, None, None]]
        result_score = 12
        self.game.field = FakeGameField(field_to_slide_left)
        result_slide = self.game.slide_left()
        self.assertTrue(result_slide)
        self.assertEqual(self.game.field.field, result_slide_left)
        self.assertEqual(self.game.score, result_score)

    def test_slide_right(self):
        field_to_slide_right = [[2, 2, None, None], [4, None, 2, 2], [2, None, 2, None], [2, 4, None, 2]]
        result_slide_right = [[None, None, None, 4], [None, None, 4, 4], [None, None, None, 4], [None, 2, 4, 2]]
        result_score = 12
        self.game.field = FakeGameField(field_to_slide_right)
        result_slide = self.game.slide_right()
        self.assertTrue(result_slide)
        self.assertEqual(self.game.field.field, result_slide_right)
        self.assertEqual(self.game.score, result_score)

    def test_slide_up(self):
        field_to_slide_up = [[None, 2, None, 4], [2, None, 2, None], [2, None, 4, 4], [None, 2, 2, 2]]
        result_slide_up = [[4, 4, 2, 8], [None, None, 4, 2], [None, None, 2, None], [None, None, None, None]]
        result_score = 16
        self.game.field = FakeGameField(field_to_slide_up)
        result_slide = self.game.slide_up()
        self.assertTrue(result_slide)
        self.assertEqual(self.game.field.field, result_slide_up)
        self.assertEqual(self.game.score, result_score)

    def test_slide_down(self):
        field_to_slide_down = [[None, 2, None, 4], [2, None, 2, None], [2, None, 4, 4], [None, 2, 2, 2]]
        result_slide_down = [[None, None, None, None], [None, None, 2, None], [None, None, 4, 8], [4, 4, 2, 2]]
        result_score = 16
        self.game.field = FakeGameField(field_to_slide_down)
        result_slide = self.game.slide_down()
        self.assertTrue(result_slide)
        self.assertEqual(self.game.field.field, result_slide_down)
        self.assertEqual(self.game.score, result_score)

    def test_check_avaliable_turn(self):
        field_to_check = [[2, 2, None, None], [4, 4, None, None], [2, 2, None, None], [4, 4, None, None]]
        field_to_test_1 = [[2, 2, None, None], [4, 4, None, None], [2, 2, None, None], [4, 4, None, None]]
        field_to_test_2 = [[4, None, None, None], [8, None, None, None], [4, None, None, None], [8, None, None, None]]
        self.game.field = FakeGameField(field_to_check)
        self.assertFalse(self.game._check_avaliable_turn(field_to_test_1))
        self.assertTrue(self.game._check_avaliable_turn(field_to_test_2))

    def test_check_win(self):
        field_to_check_1 = [[None, None, None, None], [None, None, None, None], [None, None, None, None], [None, None, None, None]]
        self.game.field = FakeGameField(field_to_check_1)
        self.assertFalse(self.game._check_win())

        field_to_check_2 = [[None, None, None, None], [None, None, 2048, None], [None, None, None, None], [None, None, None, None]]
        self.game.field = FakeGameField(field_to_check_2)
        self.assertTrue(self.game._check_win())

    def test_check_game_over(self):
        field_to_check_1 = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
        self.game.field = FakeGameField(field_to_check_1)
        self.assertTrue(self.game._check_game_over())

        field_to_check_2 = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, None]]
        self.game.field = FakeGameField(field_to_check_2)
        self.assertFalse(self.game._check_game_over())

        field_to_check_3 = [[2, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
        self.game.field = FakeGameField(field_to_check_3)
        self.assertFalse(self.game._check_game_over())

        field_to_check_4 = [[1, 2, 3, 4], [5, 6, 7, 4], [9, 10, 11, 12], [13, 14, 15, 16]]
        self.game.field = FakeGameField(field_to_check_4)
        self.assertFalse(self.game._check_game_over())

        field_to_check_5 = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 15]]
        self.game.field = FakeGameField(field_to_check_5)
        self.assertFalse(self.game._check_game_over())

    def test_game_state(self):
        test_score = 1024
        field_to_check_ok = [[2, None, 16, None], [None, 4, None, 8], [32, None, None, 16], [2, 4, None, None]]
        field_to_check_game_over = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
        field_to_check_win = [[None, None, None, None], [None, 2048, None, None], [None, None, None, None], [None, None, None, None]]

        self.game.score = test_score
        self.game.field = FakeGameField(field_to_check_ok)
        result_ok = self.game.game_state()

        self.game.field = FakeGameField(field_to_check_game_over)
        result_game_over = self.game.game_state()

        self.game.field = FakeGameField(field_to_check_win)
        result_win = self.game.game_state()

        self.assertEqual(result_ok, {'win': False, 'game_over': False, 'score': test_score, 'field': field_to_check_ok})
        self.assertEqual(result_game_over, {'win': False, 'game_over': True, 'score': test_score, 'field': field_to_check_game_over})
        self.assertEqual(result_win, {'win': True, 'game_over': False, 'score': test_score, 'field': field_to_check_win})

class TestGameField(unittest.TestCase):
    def setUp(self):
        self.game_field = GameField()

    def tearDown(self):
        del self.game_field

    def test_new_game_filed(self):
        self.assertEqual(self.game_field.field, [[None, None, None, None], [None, None, None, None], [None, None, None, None], [None, None, None, None]])

        field_to_check = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
        self.game_field = GameField(field_to_check)
        self.assertEqual(self.game_field.field, field_to_check)

    def test_set_game_field(self):
        field_to_check = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
        self.game_field.field = field_to_check
        self.assertEqual(self.game_field.field, field_to_check)

    def test_delete_game_field(self):
        test_game_field = [[1,2,3,4], [5,6,7,8], [9,10,11,12], [13,14,15,16]]
        self.game_field.field = test_game_field
        self.assertEqual(self.game_field.field, test_game_field)
        del self.game_field.field
        self.assertEqual(self.game_field.field, [[None, None, None, None], [None, None, None, None], [None, None, None, None], [None, None, None, None]])

    def test_push_value(self):
        self.game_field.push_value(32)
        test_val_list = list(filter(lambda x: x != None, [self.game_field.field[y][x] for y in range(4) for x in range(4)]))
        self.assertEqual(len(test_val_list), 1)
        self.assertEqual(test_val_list[0], 32)

        field_to_check = [[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 12], [13, 14, 15, 16]]
        self.game_field.field = field_to_check        
        self.game_field.push_value(32)
        test_val_list = list(filter(lambda x: x != None, [self.game_field.field[y][x] for y in range(4) for x in range(4)]))
        self.assertEqual(len(test_val_list), 16)
        self.assertNotIn(32, test_val_list)
        
class FakeGameField:
    def __init__(self, field=None):
        self.field = field
    def push_value(self, val):
        self.val = val

if __name__ == '__main__':
    unittest.main()
