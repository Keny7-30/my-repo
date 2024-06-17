from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
import os

app = Flask(__name__)

# 環境變數
LINE_CHANNEL_SECRET = os.getenv('45673cf3d362fb95dec1052f18774fc3')
LINE_CHANNEL_ACCESS_TOKEN = os.getenv('GNnRgamrjN2p6I1vkYyzukKhB7/u3Zx8e133LuMjo1a88Rpter7fF9iRp8QA31LPRaN0tp9S8c4dTxxuPtWuTYbwMqykOonLR40ieakTtGS59DbUEt/EpwXbTnZ+rIsbNDrJ5P70S4+S+QUpeAedtgdB04t89/1O/w1cDnyilFU=')

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)


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
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()