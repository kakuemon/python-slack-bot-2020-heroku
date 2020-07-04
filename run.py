# coding:utf-8
import os
import re
import sys
import json

from flask import Flask
from slack import WebClient
from slackeventsapi import SlackEventAdapter

""" Usage of Zoom Manager """
from Zoom import ZoomRoom, ZoomManager

import requests

# Flaskを作ってgunicornで動くようにする
app = Flask(__name__)

# Our app's Slack Event Adapter for receiving actions via the Events API
slack_signing_secret = os.environ["SLACK_SIGNING_SECRET"]
slack_events_adapter = SlackEventAdapter(slack_signing_secret, "/slack/events", app)

# Create a WebClient for your bot to use for Web API requests
slack_bot_token = os.environ["SLACK_BOT_TOKEN"]
slack_client = WebClient(slack_bot_token)

ZOOM_USER_ID = os.environ["ZOOM_USER_ID"]
ZOOM_TOKEN = os.environ["ZOOM_TOKEN"]

ZOOM_TOPIC = "20200705Test"

def Zoom_Create_Room():
    url = "https://api.zoom.us/v2/users/%s/meetings" % ZOOM_USER_ID
    payload = "{\"topic\":\"%s\"}" % ZOOM_TOPIC
    headers = {
        "content-type": "application/json",
        "authorization": "Bearer %s" % ZOOM_TOKEN 
        }
    response = requests.request("POST", url, data=payload, headers=headers)
    print(response.text)
    return response.text


# Example responder to greetings
@slack_events_adapter.on("message")
def handle_message_greeting(event_data):
    print("debug:handled function: {}".format(sys._getframe().f_code.co_name))
    print("debug:eventdata:{}".format(event_data))
    message = event_data["event"]
    if message.get("subtype") is None and message.get("bot_id") is None:
        channel = message["channel"]
        res_message = message.get("text") + ":dolphin:"
        slack_client.chat_postMessage(channel=channel, text=res_message)

    # message = event_data["event"]

    # message_pattern = "^hi.*"

    # # subtypeがない場合=普通のメッセージ, 自分自身の内容を取得してもスルーするようにしておく必要がある
    # if message.get("subtype") is None and message.get("bot_id") is None:
    #     # メッセージを適当にTrueで当たるものを探して
    #     matchobj = re.match(message_pattern, message.get("text"))
    #     if matchobj:
    #         print("hi receive")
    #         # 何かを返す
    #         channel = message["channel"]
    #         res_message = "Hi!!! :robot_face::mount_fuji: :shrimp::fish:"
    #         slack_client.chat_postMessage(channel=channel, text=res_message)


@slack_events_adapter.on("message")
def handle_message_greeting_jp(event_data):
    print("debug:handled function: {}".format(sys._getframe().f_code.co_name))
    print("debug:eventdata:{}".format(event_data))
    message = event_data["event"]

    message_pattern = "^こんにちは.*"

    # subtypeがない場合=普通のメッセージ, 自分自身の内容を取得してもスルーするようにしておく必要があ
    if message.get("subtype") is None and message.get("bot_id") is None:
        matchobj = re.match(message_pattern, message.get("text"))
        if matchobj:
            print("hi jp receive")
            channel = message["channel"]
            res_message = "こんにちは！！:robot_face::mount_fuji::shrimp::fish:"
            slack_client.chat_postMessage(channel=channel, text=res_message)

@slack_events_adapter.on("message")
def handle_message_greeting_jp(event_data):
    print("debug:handled function: {}".format(sys._getframe().f_code.co_name))
    print("debug:eventdata:{}".format(event_data))
    message = event_data["event"]

    message_pattern = "^zoom.*"

    # subtypeがない場合=普通のメッセージ, 自分自身の内容を取得してもスルーするようにしておく必要があ
    if message.get("subtype") is None and message.get("bot_id") is None:
        matchobj = re.match(message_pattern, message.get("text"))
        if matchobj:
            room = Zoom_Create_Room()
            slack_client.chat_postMessage(channel=channel, text=room)



# エラー時のイベントのハンドリング
@slack_events_adapter.on("error")
def error_handler(err):
    print("ERROR: " + str(err))


# botアプリを起動する:FlaskサーバーでEvent APIを待機する
if __name__ == "__main__":
    print("run slackbot")
    app.run(port=3000)
