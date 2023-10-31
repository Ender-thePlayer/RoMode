import sys
import gi
import os
import subprocess
import json
from os.path import expanduser
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gio, GLib, Gdk


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


def switch_theme(self, buttons):
    self.MainWindow.style_manager = Adw.StyleManager().get_default()
    if self.MainWindow.style_manager.get_dark():
        self.MainWindow.style_manager.set_color_scheme(Adw.ColorScheme.FORCE_LIGHT)

        config_data['theme'] = 'light'

        with open(config_file, 'w') as f:
            json.dump(config_data, f)
    else:
        self.MainWindow.style_manager.set_color_scheme(Adw.ColorScheme.FORCE_DARK)
        config_data['theme'] = 'dark'

        with open(config_file, 'w') as f:
            json.dump(config_data, f)

def on_id_entry_changed(entry):
    text = entry.get_text()
    config_data['spotify_client_id'] = text

    with open(config_file, 'w') as f:
        json.dump(config_data, f)


def on_secret_entry_changed(entry):
    text = entry.get_text()
    config_data['spotify_client_secret'] = text

    with open(config_file, 'w') as f:
        json.dump(config_data, f)