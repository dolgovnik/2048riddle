import asyncio
import aiohttp

from flask import Flask
from flask import request

from game2048 import Game
from game2048 import GameField

import services

from config import config

TOKEN = config['telegram']['TOKEN']
URL = config['telegram']['URL']

app = Flask(__name__)

@app.route('/riddle2048bot', methods = ['POST'])
async def riddle2048bot():
    '''
    Telegram bot on Flask. Bot uses GameField and Game classes to keep game field state and perform actions on it.
    Bot saves user data (id, name, max_score) in Postgres DB.
    Game field represents on client as inline keyboard.
    '''
    #do not handle updates without messages and callback queries
    if 'callback_query' not in request.json and 'message' not in request.json:
        #return HTTP 200 on incoming request
        return app.response_class(status=200, mimetype='application/json')

    #parse request data
    message = request.json['callback_query']['message'] if 'callback_query' in request.json else request.json['message']
    callback_query = request.json['callback_query'] if 'callback_query' in request.json else None
    from_user_data = callback_query['from'] if callback_query else message['from']

    #static buttons
    inline_action_buttons = [{'text': '\u2B05', 'callback_data': 'left'}, {'text': '\u2B06', 'callback_data': 'up'},
                             {'text': '\u2B07', 'callback_data': 'down'}, {'text': '\u27A1', 'callback_data': 'right'}]
    inline_new_game_button = [{'text': 'New Game', 'callback_data': 'new_game'}]
    inline_stats_button = [{'text': 'Statistics', 'callback_data': 'stats'}]

    #flags to show buttons
    show_field_buttons, show_action_buttons, show_stats_button, show_new_game_button = False, False, False, False

    #user object to count score statistic
    user = services.get_user(from_user_data['id'])
    #if no user data in DB - create it
    if not user:
        user = services.add_user(from_user_data['id'], from_user_data.get('first_name', None), from_user_data.get('last_name', None), from_user_data.get('username', None), 0)

    #answer to bot template
    reply = {'chat_id': message['chat']['id'],
             'parse_mode': 'HTML',
             'text': '',
             'reply_markup': {'inline_keyboard': []}}
    #handling command messages:
    if not callback_query:
        #welcome message
        if message['text'] == '/start':
            reply['text'] = 'Welcome to the 2048 riddle!\nLet\'s Play!'
            show_new_game_button = True
            show_stats_button = True
    
        #start new game
        elif message['text'] == '/new_game':
            game = Game()
            game.push_value()
            game.push_value()
            game_state = game.game_state()
            reply['text'] = f'Your score: {game_state["score"]}'
            show_field_buttons = True
            show_action_buttons = True
    
        #show statics message
        elif message['text'] == '/stats':
            users = services.get_users_list()
            reply['text'] = gen_stats_text(users, user['tg_id'])
            show_new_game_button = True

    #handling callback queries
    elif callback_query:

        #template answer to callback
        answer_callback_query = {'callback_query_id': callback_query['id'], 'text': ''}

        #field buttons
        if callback_query['data'] == 'None':
            answer_callback_query['text'] = 'Use arrow buttons below'

        #new game button
        elif callback_query['data'] == 'new_game':
            game = Game()
            game.push_value()
            game.push_value()
            game_state = game.game_state()
            reply['text'] = f'Your score: {game_state["score"]}'
            show_field_buttons = True
            show_action_buttons = True

        #statistic button
        elif callback_query['data'] == 'stats':
            users = services.get_users_list()
            reply['text'] = gen_stats_text(users, user['tg_id'])
            show_new_game_button = True

        #action buttons
        elif callback_query['data'] in ('left', 'up', 'down', 'right'):
            #parse field, create game object with current state
            field = buttons_to_field(message['reply_markup']['inline_keyboard'][:4])
            score = int(message['text'].split(': ')[1])
            game = Game(game_field_state=field)
            game.set_score(score)

            #action dict for simple access to actions
            slides = {'left': game.slide_left, 'up':  game.slide_up, 'down': game.slide_down, 'right': game.slide_right}
            #perform action
            next_turn = slides[callback_query['data']]()

            #if there is need to make next turn: push value, check if win or loose, make reply and send message to bot
            if next_turn:
                game.push_value()
                game_state = game.game_state()

                if game_state['game_over']:
                    reply['text'] = f'!!!GAME OVER!!!\nYour score: {game_state["score"]}'
                    show_new_game_button = True
                    show_stats_button = True
                else:
                    if game_state['win']:
                        reply['text'] = f'!!!YOU WIN!!!\nYour score: {game_state["score"]}'
                    else:
                        reply['text'] = f'Your score: {game_state["score"]}'
                    show_action_buttons = True
                show_field_buttons = True

            #no need to make next turn
            else:
                game_state = game.game_state()
                reply['text'] = f'Your score: {game_state["score"]}'
                show_field_buttons = True
                show_action_buttons = True

            #update user score if current score more than saved
            if game_state['score'] > user['max_score']:
                services.set_max_score(user['tg_id'], game_state['score'])

        #send answer to callback query to stop progress bar
        await sendToBot('answerCallbackQuery', answer_callback_query)
        
    #add buttons to reply
    if show_field_buttons:
        reply['reply_markup']['inline_keyboard'].extend(field_to_buttons(game_state['field']))
    if show_action_buttons:
        reply['reply_markup']['inline_keyboard'].append(inline_action_buttons)
    if show_new_game_button:
        reply['reply_markup']['inline_keyboard'].append(inline_new_game_button)
    if show_stats_button:
        reply['reply_markup']['inline_keyboard'].append(inline_stats_button)

    #send message to bot
    await sendToBot('sendMessage', reply)
        
    #return HTTP 200 on incoming request
    return app.response_class(status=200, mimetype='application/json')

def field_to_buttons(field):
    '''
    Transforms internal game field to inline keyboard buttons array on client
    '''
    buttons = []
    for y in field:
        row = []
        for x in y:
            row.append({'text': ' ' if x == None else str(x), 'callback_data': 'None'})
        buttons.append(row)
    return buttons

def buttons_to_field(buttons):
    '''
    Transforms inline keyboard buttons from client to internal game field
    '''
    field = []
    for y in buttons:
        row = []
        for x in y:
            row.append(None if x['text'] == ' ' else int(x['text']))
        field.append(row)
    return field

def gen_stats_text(users, tg_id):
    '''
    Generate users statistics message
    '''
    result_list = []
    user_found = False
    for idx, user in enumerate(users[:3]):
        name = '{0} {1}'.format(user['first_name'], user['last_name'] if user['last_name'] else '') if user['first_name'] else user['username']
        t = '{0}. {1}  {2}'.format(idx+1, name, user['max_score'])
        if user['tg_id'] == tg_id:
            user_found = True
            t = '<b>{0}</b>'.format(t)
        result_list.append(t)

    if not user_found:
        for idx, user in enumerate(users[3:]):
            if user['tg_id'] == tg_id:
                name = '{0} {1}'.format(user['first_name'], user['last_name'] if user['last_name'] else '') if user['first_name'] else user['username']
                t = '<b>{0}. {1}  {2}</b>'.format(idx+4, name, user['max_score'])
                break
            else: 
                continue
        if idx == 0:
            result_list.append(t)
        else:
            result_list.extend(['.', '.', t])

    return '\n'.join(result_list)
        
async def sendToBot(method, data):
    '''
    Send message to telegram api
    '''
    async with aiohttp.ClientSession() as session:
        async with session.post('{0}{1}/{2}'.format(URL, TOKEN, method), json=data) as resp:
            return None

if __name__ == '__main__':
    app.run(host=config['flask']['HOST'], port=config['flask']['PORT'], debug=True, ssl_context=('../certs/2048pubkey.pem', '../certs/2048botprivkey.key'))
