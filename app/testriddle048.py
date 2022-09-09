import unittest
import riddle2048

class TestRiddle2048(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_field_to_buttons(self):
        test_field = [[2, None, 4, None], [None, 16, 32, 2], [None, None, None, None], [2, 4, 8, 16]]
        test_buttons = [[{'text': '2', 'callback_data': 'None'}, {'text': ' ', 'callback_data': 'None'}, {'text': '4', 'callback_data': 'None'}, {'text': ' ', 'callback_data': 'None'}],
                        [{'text': ' ', 'callback_data': 'None'}, {'text': '16', 'callback_data': 'None'}, {'text': '32', 'callback_data': 'None'}, {'text': '2', 'callback_data': 'None'}],
                        [{'text': ' ', 'callback_data': 'None'}, {'text': ' ', 'callback_data': 'None'}, {'text': ' ', 'callback_data': 'None'}, {'text': ' ', 'callback_data': 'None'}],
                        [{'text': '2', 'callback_data': 'None'}, {'text': '4', 'callback_data': 'None'}, {'text': '8', 'callback_data': 'None'}, {'text': '16', 'callback_data': 'None'}]]
        self.assertEqual(riddle2048.field_to_buttons(test_field), test_buttons)

    def test_buttons_to_field(self):
        test_field = [[2, None, 4, None], [None, 16, 32, 2], [None, None, None, None], [2, 4, 8, 16]]
        test_buttons = [[{'text': '2', 'callback_data': 'None'}, {'text': ' ', 'callback_data': 'None'}, {'text': '4', 'callback_data': 'None'}, {'text': ' ', 'callback_data': 'None'}],
                        [{'text': ' ', 'callback_data': 'None'}, {'text': '16', 'callback_data': 'None'}, {'text': '32', 'callback_data': 'None'}, {'text': '2', 'callback_data': 'None'}],
                        [{'text': ' ', 'callback_data': 'None'}, {'text': ' ', 'callback_data': 'None'}, {'text': ' ', 'callback_data': 'None'}, {'text': ' ', 'callback_data': 'None'}],
                        [{'text': '2', 'callback_data': 'None'}, {'text': '4', 'callback_data': 'None'}, {'text': '8', 'callback_data': 'None'}, {'text': '16', 'callback_data': 'None'}]]
        self.assertEqual(riddle2048.buttons_to_field(test_buttons), test_field)

    def test_gen_stats_text(self):
        user_1 = {'tg_id': 123, 'first_name': 'Test_1', 'last_name': 'Test_1', 'username': 'Test_1', 'max_score': 5000}
        user_2 = {'tg_id': 456, 'first_name': 'Test_2', 'last_name': None, 'username': 'Test_2', 'max_score': 4000}
        user_3 = {'tg_id': 789, 'first_name': None, 'last_name': None, 'username': 'Test_3', 'max_score': 3000}
        user_4 = {'tg_id': 321, 'first_name': 'Test_4', 'last_name': 'Test_4', 'username': 'Test_4', 'max_score': 2000}
        user_5 = {'tg_id': 654, 'first_name': 'Test_5', 'last_name': 'Test_5', 'username': 'Test_5', 'max_score': 1000}
        users = [user_1, user_2, user_3, user_4, user_5]

        result_1 = '<b>1. Test_1 Test_1  5000</b>\n2. Test_2   4000\n3. Test_3  3000'
        result_2 = '1. Test_1 Test_1  5000\n2. Test_2   4000\n<b>3. Test_3  3000</b>'
        result_3 = '1. Test_1 Test_1  5000\n2. Test_2   4000\n3. Test_3  3000\n<b>4. Test_4 Test_4  2000</b>'
        result_4 = '1. Test_1 Test_1  5000\n2. Test_2   4000\n3. Test_3  3000\n.\n.\n<b>5. Test_5 Test_5  1000</b>'

        test_result_1 = riddle2048.gen_stats_text(users, user_1['tg_id'])
        test_result_2 = riddle2048.gen_stats_text(users, user_3['tg_id'])
        test_result_3 = riddle2048.gen_stats_text(users, user_4['tg_id'])
        test_result_4 = riddle2048.gen_stats_text(users, user_5['tg_id'])

        self.assertEqual(test_result_1, result_1)
        self.assertEqual(test_result_2, result_2)
        self.assertEqual(test_result_3, result_3)
        self.assertEqual(test_result_4, result_4)

if __name__ == '__main__':
    unittest.main()
