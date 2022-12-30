#!/usr/bin/python3
"""
My App to Control a LED strip
==============
"""
import sys
import os
import ssl
import urllib
from urllib.request import urlopen, Request

# kivy imports
from kivy.app import App
from kivy.logger import Logger
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix import textinput, label
from kivy.uix.settings import SettingsWithTabbedPanel
from kivy.properties import NumericProperty, StringProperty, BooleanProperty, ColorProperty
from kivy.uix.slider import Slider
from kivy.graphics import Color, Rectangle
from kivy.resources import resource_add_path
from kivy.network.urlrequest import UrlRequest

# add paths
sys.path.append(os.path.dirname(__file__))
resource_add_path(os.path.dirname(__file__))

# my modules
from mysliders import MySlider

# load other kv files
Builder.load_file('mysliders.kv')


class MyConnection:
    count = 1

    def test_connection(self):
        self.root.ids.debug_lbl.text = "Testing connection..."
        UrlRequest(
            url=urllib.parse.urljoin(self._get_target(), 'test'),
            on_failure=self._on_connection_failure,
            on_error=self._on_connection_error,
            on_success=self._on_connection_success,
        )

    # def send_message(self, message):
    #     POST_data = self._prepare_data(message)
    #     self._send_message(POST_data)

    # def _send_message(self, POST_data):
    #     self.root.ids.debug_lbl.text = "Sending..."
    #     req = UrlRequest(
    #         url=self._get_target(),
    #         req_body=POST_data["auth_data"],
    #         # req_headers=POST_data["headers"],
    #         on_failure=self._on_connection_failure,
    #         on_error=self._on_connection_error,
    #         on_success=self._on_message_success,
    #     )

    # def _prepare_data(self, message):
    #     auth_data = {"message": message}
    #     auth_data = urllib.parse.urlencode(auth_data)
    #     headers = {
    #         "Content-type": "application/x-www-form-urlencoded",
    #         "Accept": "application/json",
    #     }
    #     return {"auth_data": auth_data, "headers": headers}

    def send_GET_request(self, id, content):
        self.root.ids.debug_lbl.text = "Sending GET..."
        GET_req = urllib.parse.urljoin(
            self._get_target(), 'get?' + id + '=' + urllib.parse.quote(content))
        UrlRequest(
            url=GET_req,
            on_failure=self._on_connection_failure,
            on_error=self._on_connection_error,
            on_success=self._on_message_success,
        )

    def send_POST_request(self, id, data):
        self.root.ids.debug_lbl.text = "Sending..."
        POST_data = self._prepare_json_data(data)
        GET_req = urllib.parse.urljoin(self._get_target(), id)
        req = UrlRequest(
            url=GET_req,
            req_body=POST_data["auth_data"],
            req_headers=POST_data["headers"],
            on_failure=self._on_connection_failure,
            on_error=self._on_connection_error,
            on_success=self._on_message_success,
        )

    def _prepare_json_data(self, data: dict):
        auth_data = urllib.parse.urlencode(data)
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }
        return {"auth_data": auth_data, "headers": headers}

    def _on_message_success(self, request, result):
        self.root.ids.debug_lbl.text = "Message %s delivered" % self.count
        if result:
            print(result)
        self.count += 1

    def _on_connection_success(self, request, result):
        self.root.ids.debug_lbl.text = "Connected!"

    def _on_connection_failure(self, request, result):
        print("request: ", request)
        print("result: ", result)
        self.root.ids.debug_lbl.text = "Connection fail"

    def _on_connection_error(self, request, result):
        self.root.ids.debug_lbl.text = "Connection error"

    def _get_target(self):
        return self.config.get("Config", "url")


class MyApp(App, MyConnection):

    def build(self):
        """
        Build and return the root widget.
        """
        # The line below is optional. You could leave it out or use one of the
        # standard options, such as SettingsWithSidebar, SettingsWithSpinner
        # etc.
        self.settings_cls = SettingsWithTabbedPanel
        # We apply the saved configuration settings or the defaults
        root = Builder.load_file("client.kv")
        return root

    def send_slider_values(self):
        # toGet = {
        #     'brightness': 'sldr_bright',
        #     'red': 'sldr_red',
        #     'green': 'sldr_green',
        #     'blue': 'sldr_blue',
        # }
        # payload = dict()
        # for key, val in toGet.items():
        #     payload[key] = self.root.ids[val].value
        # print(payload)
        rgb = self.root.ids.sldrgrp_hsv.myrgb
        payload = {
            # 'brightness': int(255), # dont need brightness, encoded in rgb in this case (hsv 2 rgb conversion)
            'r': int(rgb[0] * 255),
            'g': int(rgb[1] * 255),
            'b': int(rgb[2] * 255),
        }
        print("going to send payload: ", payload)
        self.send_POST_request('led', payload)

    def send_toggle_led(self):
        print('SWTICH')
        print(self)

    def build_config(self, config):
        """
        Set the default values for the configs sections.
        """
        config.setdefaults("Config", {
            "text": "Hello",
            "font_size": 20,
            "url": "http://localhost:5000"
        })

    def build_settings(self, settings):
        """
        Add our custom section to the default configuration object.
        """
        # We use the string defined above for our JSON, but it could also be
        # loaded from a file as follows:
        settings.add_json_panel("Config", self.config,
                                "resource/settings.json")

    def on_config_change(self, config, section, key, value):
        """
        Respond to changes in the configuration.
        """
        Logger.info(
            "main.py: App.on_config_change: {0}, {1}, {2}, {3}".format(
                config, section, key, value
            )
        )

    def close_settings(self, settings=None):
        """
        The settings panel has been closed.
        """
        Logger.info("main.py: App.close_settings: {0}".format(settings))
        super(MyApp, self).close_settings(settings)


if __name__ == "__main__":
    ssl._create_default_https_context = ssl._create_unverified_context
    MyApp().run()
