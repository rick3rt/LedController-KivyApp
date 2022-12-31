from kivy.uix.slider import Slider
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty, StringProperty, BooleanProperty, ColorProperty
from itertools import chain
from kivy.graphics.texture import Texture
from ledstripapp.util.color import hsv2rgb, hsv2rgba
from ledstripapp.util.gradient import Gradient


class MySlider(BoxLayout):
    min = NumericProperty(0)
    max = NumericProperty(200)
    lbl = StringProperty("myslider")
    color = ColorProperty((0, 0, 0, 0))
    value = NumericProperty(0)

    def on_value_change(self, instance, value):
        self.value = value


class ColorSlider(Slider):
    knobsize = NumericProperty('32sp')
    innerknobsize = NumericProperty('8sp')
    knobcolor_solid = ColorProperty((0, 1, 0, 1))
    knobcolor_opaque = ColorProperty((0, 1, 0, 0.5))


class HSVColorSlider(ColorSlider):

    def on_value_change(self, instance, value):
        self.knobcolor_solid[0:3] = hsv2rgb((value, 1, 1))
        self.knobcolor_opaque[0:3] = hsv2rgb((value, 1, 1))


class HSVSliderGroup(BoxLayout):
    myrgb = ColorProperty((0, 0, 0, 0))

    def on_value_change(self, instance, value):
        toGet = ["sldr_hue", "sldr_saturation", "sldr_value"]
        hsv = tuple(self.ids[x].value for x in toGet)
        self.myrgb = hsv2rgba(hsv)
