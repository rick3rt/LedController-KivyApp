from kivy.uix.boxlayout import BoxLayout
from kivy.properties import ColorProperty
from numpy import insert
from mysliders import HSVColorSlider, MySlider, ColorSlider
from color import hsv2rgba
from datetime import datetime


class HSVSliderGroup(BoxLayout):
    myrgb = ColorProperty((0, 0, 0, 0))

    def on_value_change(self, instance, value):
        toGet = ["sldr_hue", "sldr_saturation", "sldr_value"]
        hsv = tuple(self.ids[x].value for x in toGet)
        self.myrgb = hsv2rgba(hsv)
        # print("I was called from ", end="")
        # print(instance, end="")
        # print(" with value %f at %s" %
        #       (value, datetime.now().strftime("%H:%M:%S")))


if __name__ == '__main__':
    from kivy.app import App
    from kivy.lang import Builder

    kv = """
BoxLayout:
    orientation: 'vertical'

    # MySlider:
    #     id: sldr_hue
    #     min: 0
    #     max: 255
    #     value: 100
    #     step: 1
    #     lbl: 'Hue'
    # HSVColorSlider:
    #     id: sldr_test
    #     min: 0
    #     max: 360
    #     value: 10
    #     step: 1

    ColorSlider:
        min: 0
        max: 1
        step: 0.1
    
    HSVSliderGroup:


"""

    Builder.load_file('mysliders.kv', rulesonly=True)
    Builder.load_file('hsvslidergroup.kv', rulesonly=True)

    class Test(App):
        def build(self):
            return Builder.load_string(kv)

    Test().run()
