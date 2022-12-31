import kivy
kivy.require('2.1.0')  # replace with your current kivy version !
from kivy.app import App


class DataHolder:

    def __init__(self):
        self.value = 10
        self.app = App.get_running_app()

    def test2(self):
        print(self.app.root.ids)
        for k in self.app.root.ids:
            print(k, self.app.root.ids[k].value)


class MyApp(App):

    # def __init__(self):

    def build(self):
        self.dh = DataHolder()

    # def test(self):
    #     print(self.root.ids)
    #     for k in self.root.ids:
    #         print(k, self.root.ids[k].value)


if __name__ == '__main__':
    MyApp().run()
