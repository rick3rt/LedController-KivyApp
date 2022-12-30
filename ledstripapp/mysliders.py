from kivy.uix.slider import Slider
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import NumericProperty, StringProperty, BooleanProperty, ColorProperty
from color import hsv2rgb, hsv2rgba
from gradient import Gradient


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
        # print("I was called from ", end="")
        # print(instance)
        # print(" with value %f at %s" %
        #       (value, datetime.now().strftime("%H:%M:%S")))

    # def on_touch_down(self, touch):
    #     if self.collide_point(touch.x, touch.y):
    #         print('down')
    #         return super(BoxLayout, self).on_touch_down(touch)

    # def on_touch_up(self, touch):
    #     if self.collide_point(touch.x, touch.y):
    #         print('up')
    #         return super(BoxLayout, self).on_touch_up(touch)
    #     else:
    #         False

    # def on_touch_move(self, touch):
    #     if self.collide_point(touch.x, touch.y):
    #         print('move')
    #         return super(BoxLayout, self).on_touch_move(touch)
    #     else:
    #         False


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

    HSVSliderGroup:


    """
    Builder.load_file('mysliders.kv', rulesonly=True)

    class Test(App):
        def build(self):
            return Builder.load_string(kv)

    Test().run()
