from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.uix.widget import Widget
from kivy.uix.slider import Slider
from kivy.graphics import Line, Color, Rectangle
from kivy.properties import NumericProperty, ColorProperty

import random


class MySlider(Slider):
    pass


KV = '''

<MySlider>:
    canvas:
        Color:
            rgb: 1, 0, 0, 1
        BorderImage:
            border: self.border_horizontal if self.orientation == 'horizontal' else self.border_vertical
            pos: (self.x + self.padding, self.center_y - self.background_width / 2) if self.orientation == 'horizontal' else (self.center_x - self.background_width / 2, self.y + self.padding)
            size: (self.width - self.padding * 2, self.background_width) if self.orientation == 'horizontal' else (self.background_width, self.height - self.padding * 2)
            source: (self.background_disabled_horizontal if self.orientation == 'horizontal' else self.background_disabled_vertical) if self.disabled else (self.background_horizontal if self.orientation == 'horizontal' else self.background_vertical)
        Color:
            rgba: root.value_track_color if self.value_track and self.orientation == 'horizontal' else [1, 1, 1, 0]
        Line:
            width: self.value_track_width
            points: self.x + self.padding, self.center_y, self.value_pos[0], self.center_y
        Color:
            rgba: root.value_track_color if self.value_track and self.orientation == 'vertical' else [1, 1, 1, 0]
        Line:
            width: self.value_track_width
            points: self.center_x, self.y + self.padding, self.center_x, self.value_pos[1]
        Color:
            rgb: 1, 1, 1
    Image:
        # pos: (root.value_pos[0] - root.cursor_width / 2, root.center_y - root.cursor_height / 2) if root.orientation == 'horizontal' else (root.center_x - root.cursor_width / 2, root.value_pos[1] - root.cursor_height / 2)
        pos: (root.value_pos[0] - root.cursor_width / 2, root.center_y - root.cursor_height / 2)
        size: root.cursor_size
        source: root.cursor_disabled_image if root.disabled else root.cursor_image
        allow_stretch: True
        keep_ratio: False

BoxLayout:
    orientation: 'vertical'
    Button:
        text: "Go paint"
        font_size: 50
    Slider: 
    MySlider:

'''


KV2 = '''
ScreenManagement:
    MainScreen:
    PaintScreen:

<MainScreen>:
    name:"main"
    FloatLayout:
        Button:
            text: "Go paint"
            font_size: 50
            color: 0,1,0,1
            size_hint: 0.3,0.2
            pos_hint: {"right":1, "top":1}
            on_release:
                root.manager.current = 'paint'

<PaintScreen@Screen>:
    name: 'paint'
    FloatLayout:
        Painter:
            canvas.before:
                Color:
                    rgba: self.color
                Rectangle:
                    pos: self.pos
                    size: self.size
        Button:
            text: "Exit painting"
            font_size: 40
            color: 0,1,0,1
            size_hint: 0.3,0.2
            pos_hint: {"right":1, "top":1}
            on_release:
                root.manager.current = 'main'
        
'''


class Painter(Widget):
    color = ColorProperty((0, 0, 0, 0))

    def on_touch_down(self, touch):
        self.color = (random.uniform(0, 1),
                      random.uniform(0, 1),
                      random.uniform(0, 1),
                      random.uniform(0, 1))
        with self.canvas:
            Color(1, 1, 1, 1)
            touch.ud["line"] = Line(points=(touch.x, touch.y))

    def on_touch_move(self, touch):
        Color(1, 1, 1, 1)
        touch.ud["line"].points += [touch.x, touch.y]


class MainScreen(Screen):
    pass


class ScreenManagement(ScreenManager):
    pass


class MainApp(App):
    def build(self):
        return Builder.load_string(KV)


if __name__ == "__main__":
    app = MainApp()
    app.run()

