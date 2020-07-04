# coding:utf-8

""" Rich Menu Manager for Line Messaging API """
import json
import requests

class Zoom_API:
    """ Datamodel of Zoom """
    def __init__(self,zoom_token,verify=True):
        """
        :topic : str
        """
        self.headers = {"Authorization": "Bearer {%s}" % zoom_token}
        self.verify=verify
        self.info = []

    def add_info(self, topic):
        """ Add an area with action
        :param topic: topic zoom
        """
        bounds = {"topic": topic}
        self.info.append(bounds)
        return self.info

    def create(self,info, zoom_userId):
        """ Register RichMenu
        :param zoom_userId: userID
        """
        url = "https://api.zoom.us/v2/users/%s/meetings" % zoom_userId
        res = requests.post(url, headers=dict(self.headers, **{"content-type": "application/json"}), data=info.to_json(), verify=self.verify).json()