#!/usr/bin/python3
"""
Config Example
==============

This file contains a simple example of how the use the Kivy settings classes in
a real app. It allows the user to change the caption and font_size of the label
and stores these changes.

When the user next runs the programs, their changes are restored.
"""

import ssl
from urllib.error import HTTPError, URLError
from urllib.request import urlopen, Request
import urllib

from kivy.app import App
from kivy.uix.settings import SettingsWithTabbedPanel
from kivy.network.urlrequest import UrlRequest
from kivy.logger import Logger
from kivy.uix.boxlayout import BoxLayout
from kivy.lang import Builder
from kivy.uix import textinput, label
from kivy.properties import NumericProperty, StringProperty, BooleanProperty, ColorProperty
from kivy.uix.slider import Slider


class MySlider(BoxLayout):
    min = NumericProperty(0)
    max = NumericProperty(200)
    lbl = StringProperty("myslider")
    color = ColorProperty((0, 0, 0, 0))
    value = NumericProperty(0)

    def on_value_change(self, instance, value):
        self.value = int(value)


class MyConnection:

    count = 1

    def send_message(self, message):
        POST_data = self._prepare_data(message)
        self._send_message(POST_data)

    def test_connection(self):
        self.root.ids.status_label.text = "Testing connection..."
        UrlRequest(
            url=self._get_target(),
            on_failure=self._on_connection_failure,
            on_error=self._on_connection_error,
            on_success=self._on_connection_success,
        )

    def _prepare_data(self, message):
        auth_data = {"message": message}
        auth_data = urllib.parse.urlencode(auth_data)
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }
        return {"auth_data": auth_data, "headers": headers}

    def _prepare_json_data(self, data: dict):
        auth_data = urllib.parse.urlencode(data)
        headers = {
            "Content-type": "application/x-www-form-urlencoded",
            "Accept": "application/json",
        }
        return {"auth_data": auth_data, "headers": headers}

    def _send_message(self, POST_data):
        self.root.ids.status_label.text = "Sending..."
        req = UrlRequest(
            url=self._get_target(),
            req_body=POST_data["auth_data"],
            # req_headers=POST_data["headers"],
            on_failure=self._on_connection_failure,
            on_error=self._on_connection_error,
            on_success=self._on_message_success,
        )

    def send_GET_request(self, id, content):
        self.root.ids.status_label.text = "Sending GET..."
        GET_req = urllib.parse.urljoin(
            self._get_target(), 'get?' + id+'='+urllib.parse.quote(content))
        UrlRequest(
            url=GET_req,
            on_failure=self._on_connection_failure,
            on_error=self._on_connection_error,
            on_success=self._on_message_success,
        )

    def send_POST_request(self, id, data):
        self.root.ids.status_label.text = "Sending..."
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

    def _on_message_success(self, request, result):
        self.root.ids.status_label.text = "Message %s delivered" % self.count
        if result:
            print(result)
        self.count += 1

    def _on_connection_success(self, request, result):
        self.root.ids.status_label.text = "Connected!"

    def _on_connection_failure(self, request, result):
        print("request: ", request)
        print("result: ", result)
        self.root.ids.status_label.text = "Connection fail"

    def _on_connection_error(self, request, result):
        self.root.ids.status_label.text = "Connection error"

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
        # root = Builder.load_file("myapp.kv")
        # return root

    def get_slider_values(self):
        brightness = self.root.ids.sldr_bright.value
        rgb = (self.root.ids.sldr_red.value,
               self.root.ids.sldr_green.value,
               self.root.ids.sldr_blue.value)
        payload = {"brightness": brightness,
                   "red": rgb[0],
                   "green": rgb[1],
                   "blue": rgb[2]}
        print(payload)
        self.send_POST_request('led', payload)

    def get_wheel_value(self):
        brightness = self.root.ids.sldr_bright.value
        rgb = self.root.ids.colorpicker.color[0:3]
        payload = {"brightness": brightness,
                   "red": int(rgb[0]*255),
                   "green": int(rgb[1]*255),
                   "blue": int(rgb[2]*255)}
        print(payload)
        self.send_POST_request('led', payload)

    def build_config(self, config):
        """
        Set the default values for the configs sections.
        """
        config.setdefaults("Config", {
            "text": "Hello",
            "font_size": 20,
            "url": "http://192.168.0.6/"
        })

    def build_settings(self, settings):
        """
        Add our custom section to the default configuration object.
        """
        # We use the string defined above for our JSON, but it could also be
        # loaded from a file as follows:
        settings.add_json_panel("Config", self.config, "settings.json")

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
