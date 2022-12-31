from kivy.uix.slider import Slider
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty, StringProperty, BooleanProperty, ColorProperty


class SliderWithLabel(BoxLayout):

    def on_value_change(self, instance, value):
        self.value = value
