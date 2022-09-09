# 2048 Telegram Bot
This is 2048 Telegram Bot. You can play on your mobile or PC Telegram client.  
Try working version of bot:  
https://t.me/riddle2048bot

## Instalaltion
1. Clone this repository:
   ```
   git clone https://github.com/dolgovnik/2048riddle.git
   ```
2. Register your bot via **BotFather** in Telegram client, get bot token
3. Customize **app/settings\_default.ini** and **docker-compose\_default.yaml**
4. Generate SSL certificates, put it to **certs** directory and check certifatate names in **nginx\_ssl.conf**
5. Start bot:
   ```
   docker-compose up
   ```
6. Play the game on your Telegram client

## Technical details
Game field is passed to Telegram client as inline keyboard. Field is saved only on Telegram client side,
and passed to server each time user pushes buttons.
On server side actions with field are performed by means of two python classes: Game and GameField.

Bot saves maximal score user statistics. Data is saved in PostgreSQL by means of SQLAlchemy.
To make actions with DB more clear Bot applies following patterns: *Repository* and *Unit of Work*.

HTTPS requests from Telegram servers are terminated by Flask, which deployed in docker with image
`tiangolo/uwsgi-nginx-flask:python3.8-alpine-2021-10-26`.
For access DB Flask uses service layer.
