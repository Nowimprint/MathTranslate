import importlib
import os
import sys
from io import StringIO

from kivy.app import App
from kivy.clock import Clock
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.popup import Popup
import time

from Dialog import LoadDialog, TranslationDialog, DownloadDialog, DownloadDialogEncapsulation, SuccessDialog, \
    WaitingDialog


class IndexPage(FloatLayout):

    def __init__(self, config, **kwargs):
        print('init')
        self.config = config
        self.dde = DownloadDialogEncapsulation(self.config)
        self.config.updated = False
        try:
            importlib.import_module('mathtranslate')
            self.config.updated = True
        except ImportError:
            self.config.updated = False
        if self.config.updated:
            import mathtranslate
            latest = mathtranslate.update.get_latest_version()
            self.config.updated = mathtranslate.__version__ == latest
        super().__init__(**kwargs)

    @staticmethod
    def page_preferences(*args):
        App.get_running_app().screen_manager.current = "Preferences_page"
        App.get_running_app().screen_manager.transition.direction = 'left'

    def show_load(self):
        # 绑定加载和取消的方法
        content = LoadDialog(load=self._load, cancel=self.dismiss_popup, cwdir='/home/jiace')
        #content = LoadDialog(load=self._load, cancel=self.dismiss_popup, path='/home/jiace')
        self._popup = Popup(title="Load Latex File", content=content, size_hint=(.9, .9))
        self._popup.open()

    def _load(self, path, filename):
        #content = SuccessDialog(cancel=self.success_dismiss_popup)
        self.dismiss_popup()
        self.config.file_path = filename
        #self.success_popup = Popup(title="Successful Loading", content=content, size_hint=(.4, .5))
        #self.success_popup.open()
        basename = os.path.basename(filename)
        self.ids.loaded_filename.text = f'Loaded file: {basename}'

    def dismiss_popup(self):
        self._popup.dismiss()

    def translate_load(self):
        if self.config.file_path is None:
            return
        dirname = os.path.dirname(self.config.file_path)
        filename = os.path.join(dirname, 'translate.tex')
        content = TranslationDialog(load=self.trans_load, cancel=self.dismiss_popup,
                                    file=filename, dirname=dirname)
        self._popup = Popup(title="Output File Path Setting", content=content, size_hint=(.9, .9))
        self._popup.open()

    def trans_load(self, output_path):
        self.config.output_path = output_path
        self.translate()
        self.dismiss_popup()
        # popup_wait.dismiss()

    @staticmethod
    def get_translate_output(selection):
        if selection:
            selected = selection[0]
            if os.path.isdir(selected):
                return os.path.join(selected, 'translate.tex')
            else:
                return selected

    def translate(self):
        if not self.config.updated:
            self.dde.download_load()
            self.config.updated = True

        else:
            from Translate import translate
            translate(self.config)
            self.successful_translate()

    def successful_translate(self):
        content = SuccessDialog(cancel=self.success_dismiss_popup)
        self.success_popup = Popup(title="Successfully translated", content=content, size_hint=(.4, .5))
        self.success_popup.open()

    def success_dismiss_popup(self):
        self.success_popup.dismiss()
