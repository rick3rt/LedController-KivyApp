from kivy.app import App
from ledstripapp.widgets.mysliders import HSVSliderGroup
from ledstripapp.util.limiter import limit_rate


class LEDController:

    def __init__(self):
        self.app = App.get_running_app()
        self.LED_on = True
        self.presets = (
            'Fire',
            'Rainbow',
            'Confetti',
            'Sine',
            'BPM',
            'Juggle',
            'Test',
        )

    @limit_rate(1 / 60)
    def send_color_slider_values(self, rgb):
        payload = {
            # 'brightness': int(255), # dont need brightness, encoded in rgb in this case (hsv 2 rgb conversion)
            'r': int(rgb[0] * 255),
            'g': int(rgb[1] * 255),
            'b': int(rgb[2] * 255),
        }
        print("going to send payload: ", payload)
        self.app.client.send_POST_request('led', payload)

    @limit_rate(1 / 60)
    def send_toggle_led(self, value):
        if value == 'down':  # ON
            self.app.client.send_POST_request('led', {'status': 1})
        else:  # OFF
            self.app.client.send_POST_request('led', {'status': 0})

    def set_preset(self, preset_name):
        payload = {'name': preset_name.lower()}
        print("going to send payload: POST /preset", payload)
        self.app.client.send_POST_request(
            'preset', payload)

    @limit_rate(1 / 60)
    def send_fire_slider_values(self, spark, cool, fps, palno):
        payload = {
            'name': 'fire',
            'spark': int(spark),
            'cool': int(cool),
            'fps': int(fps),
            'palno': int(palno),
        }
        print("going to send payload: ", payload)
        self.app.client.send_POST_request('preset', payload)

    @limit_rate(1 / 60)
    def send_slider_values(self, root):
        preset_name = root.ids.spin_select.text
        self.set_preset(preset_name)
        # start preparing payload
        # payload = {'name': preset_name}
        payload = {}
        # get slider parameters
        for id in root.ids:
            if 'sldr' in id:
                parname = id.replace('sldr_', '')
                value = root.ids[id].value
                payload[parname] = int(value)
        # send payload
        print("going to send payload: POST /preset", payload)
        self.app.client.send_POST_request('preset', payload)
