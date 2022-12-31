import os
import sys
from time import time
from kivy.app import App
from os.path import dirname, join
from kivy.lang import Builder
from kivy.logger import Logger
from kivy.uix.settings import SettingsWithTabbedPanel
from kivy.properties import NumericProperty, StringProperty, BooleanProperty, ListProperty
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.uix.screenmanager import Screen

from kivy.resources import resource_add_path
resource_add_path(os.path.dirname(__file__))
# sys.path.append(os.path.dirname(__file__))

from ledstripapp.client import MyClient
from ledstripapp.ledcontroller import LEDController

from kivy.lang import Builder
Builder.load_file('ledstripapp/widgets/mysliders.kv')
Builder.load_file('ledstripapp/widgets/newwidgets.kv')


class ShowcaseScreen(Screen):
    fullscreen = BooleanProperty(False)

    def add_widget(self, *args, **kwargs):
        if 'content' in self.ids:
            return self.ids.content.add_widget(*args, **kwargs)
        return super(ShowcaseScreen, self).add_widget(*args, **kwargs)


class ShowcaseApp(App):

    index = NumericProperty(-1)
    current_title = StringProperty()
    time = NumericProperty(0)
    show_sourcecode = BooleanProperty(False)
    sourcecode = StringProperty()
    screen_names = ListProperty([])
    hierarchy = ListProperty([])

    def build(self):
        """
        Build and return the root widget.
        """
        self.title = 'LedStripApp'
        self.settings_cls = SettingsWithTabbedPanel

        self.client = MyClient()
        self.controller = LEDController()

        Clock.schedule_interval(self._update_clock, 1 / 60.)
        self.screens = {}
        self.available_screens = [
            'Select Preset', 'Color Picker', 'Connection', 'Empty',
        ]
        self.screen_names = self.available_screens
        curdir = dirname(__file__)
        self.available_screens = [fn.replace(
            ' ', '') for fn in self.available_screens]
        self.available_screens = [join(curdir, 'screens',
                                       '{}.kv'.format(fn).lower()) for fn in self.available_screens]
        self.go_next_screen()

    # --------------------------------------------------------------------------
    # Config menu
    # --------------------------------------------------------------------------
    def build_config(self, config):
        """
        Set the default values for the configs sections.
        """
        config.setdefaults("Config", {
            "text": "Hello",
            "font_size": 20,
            "url": "http://localhost:5000"
        })

    def build_settings(self, settings):
        """
        Add our custom section to the default configuration object.
        """
        # We use the string defined above for our JSON, but it could also be
        # loaded from a file as follows:
        settings.add_json_panel("Config", self.config,
                                "resource/settings.json")

    def on_config_change(self, config, section, key, value):
        """
        Respond to changes in the configuration.
        """
        Logger.info(
            "main.py: App.on_config_change: {0}, {1}, {2}, {3}".format(
                config, section, key, value
            )
        )

    def close_settings(self, settings=None):
        """
        The settings panel has been closed.
        """
        Logger.info("main.py: App.close_settings: {0}".format(settings))
        super(ShowcaseApp, self).close_settings(settings)

    # --------------------------------------------------------------------------
    # Screen management
    # --------------------------------------------------------------------------
    def on_pause(self):
        return True

    def on_resume(self):
        pass

    def on_current_title(self, instance, value):
        self.root.ids.spnr.text = value

    def go_previous_screen(self):
        self.index = (self.index - 1) % len(self.available_screens)
        screen = self.load_screen(self.index)
        sm = self.root.ids.sm
        sm.switch_to(screen, direction='right')
        self.current_title = screen.name
        # self.update_sourcecode()

    def go_next_screen(self):
        self.index = (self.index + 1) % len(self.available_screens)
        screen = self.load_screen(self.index)
        sm = self.root.ids.sm
        sm.switch_to(screen, direction='left')
        self.current_title = screen.name
        # self.update_sourcecode()

    def go_screen(self, idx):
        self.index = idx
        self.root.ids.sm.switch_to(self.load_screen(idx), direction='left')
        # self.update_sourcecode()

    def go_hierarchy_previous(self):
        ahr = self.hierarchy
        if len(ahr) == 1:
            return
        if ahr:
            ahr.pop()
        if ahr:
            idx = ahr.pop()
            self.go_screen(idx)

    def load_screen(self, index):
        if index in self.screens:
            return self.screens[index]
        screen = Builder.load_file(self.available_screens[index])
        self.screens[index] = screen
        return screen

    def _update_clock(self, dt):
        self.time = time()


# ==============================================================================
# Main routine (not used since called from main.py in parent folder)
# ==============================================================================
if __name__ == '__main__':
    ShowcaseApp().run()
