from os.path import join, dirname
from kivy.app import App
from kivy.resources import resource_add_path
from quantiz.playground import QuantizPlayground


class QuantizApp(App):

    def __init__(self):
        self.data_dir = join(dirname(__file__), 'data')
        super(QuantizApp, self).__init__(
            kv_directory=self.data_dir)
        resource_add_path(self.data_dir)

    def build(self):
        self.root = self.create_playground()

    def create_playground(self):
        return QuantizPlayground()

    def switch_to(self, screen):
        win = self.root.parent
        win.remove_widget(self.root)
        self.root = screen
        win.add_widget(self.root)

    def on_pause(self):
        return True

