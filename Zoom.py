# coding:utf-8

""" Rich Menu Manager for Line Messaging API """
import json
import requests

class Zoom_API:
    """ Datamodel of Zoom """
    def __init__(self,userId,zoom_token,topic):
        """
        :topic : str
        """
        self.headers = {
            "content-type": "application/json",
            "authorization": "Bearer %s" %  zoom_token
            }      
        self.info = []
        self.url = "https://api.zoom.us/v2/users/%s/meetings" % userId
        self.payload = "{\"topic\":\"{%s}\"}" % topic

    def create(self):
        """ Register RichMenu
        :param zoom_userId: userID
        """
        res = requests.request("POST", self.url, data=self.payload, headers=self.headers)
        return res
    
    def roomList(self):
        """ Register RichMenu
        :param zoom_userId: userID
        """
        querystring = {"page_number":"1","page_size":"30","type":"1"}
        res = requests.request("GET", self.url, headers=self.headers, params=querystring)
        return res

    