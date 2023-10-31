
import sys
import gi
import os
import json
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Gio, GLib, Adw
from romode.window import MainWindow

## Temp fix, it works only in a flatpak enviroment, this isn't yet a flatpak
os.environ["XDG_CONFIG_HOME"] = '/home/ender/.config'

standard_config_dir = os.environ.get('XDG_CONFIG_HOME')
config_dir = os.path.join(standard_config_dir, 'romode')
config_file = os.path.join(config_dir, 'config.json')

config_data = {}
if os.path.exists(config_file):
    with open(config_file, 'r') as f:
        try:
            config_data = json.load(f)
        except json.decoder.JSONDecodeError:
            config_data = {}

try:
    with open(config_file) as file:
        try:
            data = json.load(file)
        except json.decoder.JSONDecodeError:
            data = {}

except FileNotFoundError:
    data = {}
    with open(config_file, 'w') as file:
        json.dump(data, file)

##RUN-APP
class MyApp(Adw.Application):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.connect('activate', self.on_activate)

    def on_activate(self, app):
        self.win = MainWindow(application=app, config_data=config_data, config_file=config_file)
        self.win.present()

app = MyApp()
app.run(sys.argv)