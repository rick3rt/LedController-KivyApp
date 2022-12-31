import ssl
import urllib
from urllib.request import urlopen, Request
from kivy.network.urlrequest import UrlRequest
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.app import App
import time
from ledstripapp.util.limiter import limit_rate
# ssl._create_default_https_context = ssl._create_unverified_context


class MyClient:
    count = 1

    # def __init__(self):
    #     pass

    @limit_rate(2)
    def test_connection(self):
        UrlRequest(
            url=urllib.parse.urljoin(self._get_target(), 'test'),
            on_failure=self._on_connection_failure,
            on_error=self._on_connection_error,
            on_success=self._on_connection_success,
        )

    @limit_rate(2)
    def test_leds(self):
        brightness = self.send_GET_request('brightness')

        for _ in range(5):
            self.send_POST_request('led', {'brightness': 0})
            time.sleep(0.2)
            self.send_POST_request('led', {'brightness': brightness})
            time.sleep(0.3)

    # @limit_rate(1 / 60)
    def send_GET_request(self, id, content=None):
        req = 'get?' + id
        if content:
            req += '=' + urllib.parse.quote(content)
        GET_req = urllib.parse.urljoin(self._get_target(), req)
        req = UrlRequest(
            url=GET_req,
            on_failure=self._on_connection_failure,
            on_error=self._on_connection_error
        )
        req.wait()
        return req.result

    # @limit_rate(1 / 60)
    def send_POST_request(self, id, data):
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
        if result:
            print(result)
        self.count += 1

    def _on_connection_success(self, request, result):
        # self.root.ids.debug_lbl.text = "Connected!"
        popup = Popup(title='Connection status',
                      content=Label(text='Connection Success'),
                      size_hint=(None, None), size=(400, 400))
        popup.open()

    def _on_connection_failure(self, request, result):
        print("request: ", request)
        print("result: ", result)
        popup = Popup(title='Connection status',
                      content=Label(text='Connection Failed :('),
                      size_hint=(None, None), size=(400, 400))
        popup.open()

    def _on_connection_error(self, request, result):
        popup = Popup(title='Connection status',
                      content=Label(text='Connection Error :('),
                      size_hint=(None, None), size=(400, 400))
        popup.open()

    def _get_target(self):
        app = App.get_running_app()
        return app.config.get("Config", "url")
