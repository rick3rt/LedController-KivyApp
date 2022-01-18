from itertools import chain
from kivy.graphics.texture import Texture


class Gradient(object):

    @staticmethod
    def horizontal(*args):
        texture = Texture.create(size=(len(args), 1), colorfmt='rgba')
        buf = bytes([int(v * 255) for v in chain(*args)])  # flattens

        texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
        return texture

    @staticmethod
    def vertical(*args):
        texture = Texture.create(size=(1, len(args)), colorfmt='rgba')
        buf = bytes([int(v * 255) for v in chain(*args)])  # flattens
        texture.blit_buffer(buf, colorfmt='rgba', bufferfmt='ubyte')
        return texture


if __name__ == '__main__':
    from kivy.app import App
    from kivy.lang import Builder

    kv = """
#:import get_color_from_hex kivy.utils.get_color_from_hex
#:import Gradient gradient.Gradient
BoxLayout:
    orientation: 'vertical'

    BoxLayout
        id: box
        on_kv_post: print(get_color_from_hex("E91E63"))
        canvas:
            Rectangle:
                size: self.size
                pos: self.pos
                texture: 
                    Gradient.horizontal( \
                    get_color_from_hex("E91E63"), \
                    get_color_from_hex("FCE4EC"))
    BoxLayout
        id: box
        on_kv_post: print(get_color_from_hex("E91E63"))
        canvas:
            Rectangle:
                size: self.size
                pos: self.pos
                texture: 
                    Gradient.horizontal( \
                    (1,0,0,1), \
                    (0,1,0,1),
                    (0,0,1,1),)
    """

    class Test(App):
        def build(self):
            return Builder.load_string(kv)

    Test().run()
