from kivy.uix.slider import Slider
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty, StringProperty, BooleanProperty, ColorProperty
from color import hsv2rgb
from gradient import Gradient


class ColorSlider(Slider):
    knobsize = NumericProperty(30)
    innerknobsize = NumericProperty(8)
    knobcolor_solid = ColorProperty((0, 1, 0, 1))
    knobcolor_opaque = ColorProperty((0, 1, 0, 0.5))


class HSVColorSlider(ColorSlider):

    def on_value_change(self, instance, value):
        self.knobcolor_solid[0:3] = hsv2rgb((value, 1, 1))
        self.knobcolor_opaque[0:3] = hsv2rgb((value, 1, 1))


class MySlider(BoxLayout):
    min = NumericProperty(0)
    max = NumericProperty(200)
    lbl = StringProperty("myslider")
    color = ColorProperty((0, 0, 0, 0))
    value = NumericProperty(0)

    def on_value_change(self, instance, value):
        self.value = value


if __name__ == '__main__':
    from kivy.app import App
    from kivy.lang import Builder

    kv = """
BoxLayout:
    orientation: 'vertical'

    MySlider:
        id: sldr_hue
        min: 0
        max: 255
        value: 100
        step: 1
        lbl: 'Hue'        


    HSVColorSlider:
        id: sldr_test
        min: 0
        max: 360
        value: 10
        step: 1

    ColorSlider:
        min: 0 
        max: 1
        step: 0.1

    """
    Builder.load_file('mysliders.kv', rulesonly=True)

    class Test(App):
        def build(self):
            return Builder.load_string(kv)

    Test().run()
