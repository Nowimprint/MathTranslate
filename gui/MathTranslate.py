from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from IndexPage import IndexPage
from PreferencesPage import PreferencesPage
import sys


class MathTranslate(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        #self.icon = "./static/icon.ico"
        self.title = "MathTranslate App"

        self.load_kv("guipage/index.kv")  # create a index.kv file
        self.load_kv("guipage/preferencespage.kv")  # create a image.kv file

        self.screen_manager = ScreenManager()
        pages = {"Index_page": IndexPage(), "Preferences_page": PreferencesPage()}

        for item, page in pages.items():
            self.default_page = page
            # add page
            screen = Screen(name=item)
            screen.add_widget(self.default_page)
            # add page from screen manager
            self.screen_manager.add_widget(screen)
        return self.screen_manager


if __name__ == "__main__":
    sys.setrecursionlimit(50000)
    MathTranslate().run()
