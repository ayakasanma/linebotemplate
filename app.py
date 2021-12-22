import re, sqlite3
from flask import Flask, render_template, url_for, request, abort, g
from linebot.models import events
from line_chatbot_api import *
from line_chatbot_handle import *
from access_sqlite_db import *

# create flask server
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)
    return 'OK'

@handler.add(PostbackEvent)
def handle_postback(event):
    line_user_name = line_bot_api.get_profile(event.source.user_id).display_name
    line_user_id = event.source.user_id
    data = dict(parse_qsl(event.postback.data))
    if data.get('action'):
        update_user_action(line_user_id, data.get('action'))

# handle msg
@handler.add(MessageEvent)
def handle_something(event):
    line_user_name = line_bot_api.get_profile(event.source.user_id).display_name
    line_user_id = event.source.user_id
    user_data = read_user_data(line_user_id, line_user_name)
    
    function_handle_something(event, user_data)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)
