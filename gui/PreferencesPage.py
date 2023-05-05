from kivy.app import App
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup

from Dialog import LanguageDialog, EngineDialog, DownloadDialogEncapsulation


def language_format(language):
    language_dict = {'Afrikaans': 'af', 'Irish': 'ga', 'Albanian': 'sq', 'Italian': 'it', 'Arabic': 'ar', 'Japanese': 'ja',
            'Azerbaijani':'az', 'Kannada':'kn', 'Basque':'eu', 'Korean':'ko', 'Bengali':'bn', 'Latin':'la',
            'Belarusian':'be', 'Latvian':'lv', 'Bulgarian':'bg', 'Lithuanian':'lt', 'Catalan':'ca', 'Macedonian':'mk',
            'Chinese Simplified':'zh-CN', 'Malay':'ms', 'Chinese Traditional':'zh-TW', 'Maltese':'mt', 'Croatian':'hr',
            'Norwegian':'no', 'Czech':'cs', 'Persian':'fa', 'Danish':'da', 'Polish':'pl', 'Dutch':'nl', 'Portuguese':'pt',
            'English':'en', 'Romanian':'ro', 'Esperanto':'eo', 'Russian':'ru', 'Estonian':'et', 'Serbian':'sr',
            'Filipino':'tl', 'Slovak':'sk', 'Finnish':'fi', 'Slovenian':'sl', 'French':'fr', 'Spanish':'es', 'Galician':'gl',
            'Swahili':'sw', 'Georgian':'ka', 'Swedish':'sv', 'German':'de', 'Tamil':'ta', 'Greek':'el', 'Telugu':'te',
            'Gujarati':'gu', 'Thai':'th', 'Haitian Creole':'ht', 'Turkish':'tr', 'Hebrew':'iw', 'Ukrainian':'uk',
            'Hindi':'hi', 'Urdu':'ur', 'Hungarian':'hu', 'Vietnamese':'vi', 'Icelandic':'is', 'Welsh':'cy', 'Indonesian':'id',
            'Yiddish':'yi'}
    return language_dict[language]


class PreferencesPage(BoxLayout):

    def __init__(self, config, **kwargs):
        self.config = config
        self.dde = DownloadDialogEncapsulation(self.config)
        Clock.schedule_interval(self.update_language_format, 1)
        super().__init__(**kwargs)

    def back_index(*args):
        App.get_running_app().screen_manager.current = "Index_page"
        App.get_running_app().screen_manager.transition.direction = 'right'

    def engine_show_load(self, text):
        if not self.config.updated:
            self.dde.download_load()
        else:
            if text == 'Tencent':
                content = EngineDialog(load=self.engine_load, cancel=self.dismiss_popup)
                self._popup = Popup(title="Engine API Setting", content=content, size_hint=(.9, .9))
                self._popup.open()
                self.config.engine = 'tencent'

    def language_show_load(self):
        content = LanguageDialog(load=self.language_load, cancel=self.dismiss_popup)
        self._popup = Popup(title="Translation Language Setting", content=content, size_hint=(.9, .9))
        self._popup.open()

    def engine_load(self, id, key):
        from mathtranslate import config
        print(id, key)
        config.set_variable_4ui(config.tencent_secret_id_path, id)
        config.set_variable_4ui(config.tencent_secret_key_path, key)
        config.tencent_secret_id = config.read_variable(config.tencent_secret_id_path, config.tencent_secret_id_default)
        config.tencent_secret_key = config.read_variable(config.tencent_secret_key_path,
                                                         config.tencent_secret_key_default)
        print(config.tencent_secret_id, config.tencent_secret_key)
        self.dismiss_popup()

    def update_language_format(self, *args):
        self.ids.language_setting.text = self.config.language_from + "=>" + self.config.language_to

    def language_load(self, language_from, language_to):
        print(language_from, language_to)
        self.config.language_from = language_format(language_from)
        self.config.language_to = language_format(language_to)
        print(self.config.language_from, self.config.language_to)
        self.dismiss_popup()

    def dismiss_popup(self):
        self._popup.dismiss()
