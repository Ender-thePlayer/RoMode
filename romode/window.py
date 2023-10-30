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
from romode.settings import SettingsWindow
from gi.repository import Gtk, Adw, Gio, GLib, Gdk

## Temp fix, it works only in a flatpak enviroment, this isn't yet a flatpak
os.environ["XDG_CONFIG_HOME"] = '/home/ender/.config'

standard_config_dir = os.environ.get('XDG_CONFIG_HOME')
config_dir = os.path.join(standard_config_dir, 'romode')
config_file = os.path.join(config_dir, 'config.json')

if not os.path.isdir(config_dir):
    os.mkdir(config_dir) 

config_data = {}
if os.path.exists(config_file):
    with open(config_file, 'r') as f:
        try:
            config_data = json.load(f)
        except json.decoder.JSONDecodeError:
            config_data = {}


class MainWindow(Gtk.ApplicationWindow):
    def __init__(self, *args, **kwargs):
        with open(config_file, 'r') as file:
            data = json.load(file)
        
        self.style_manager = Adw.StyleManager().get_default()

        if not data['theme']:
            print(self.style_manager.get_system_supports_color_schemes())
            self.style_manager.set_color_scheme(Adw.ColorScheme.PREFER_LIGHT)
        if data['theme'] == 'light':
            self.style_manager.set_color_scheme(Adw.ColorScheme.FORCE_LIGHT)
        if data['theme'] == 'dark':
            self.style_manager.set_color_scheme(Adw.ColorScheme.FORCE_DARK)


        super().__init__(*args, **kwargs)
        self.set_default_size(1000, 400)
        self.set_title("Codename: RoMode")

        self.header = Gtk.HeaderBar()
        self.set_titlebar(self.header)
        # self.set_resizable(False)

        self.settbutton = Gtk.Button()
        self.settbutton.set_icon_name(icon_name='preferences-system-symbolic')    
        self.settbutton.connect("clicked", self.on_settings_button_clicked)
        self.header.pack_end(child=self.settbutton)

    ##BOX FOR EVERYTHING
        mainbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        mainbox.set_spacing(10)
        mainbox.set_margin_top(10)
        mainbox.set_margin_bottom(10)
        mainbox.set_margin_start(10)
        mainbox.set_margin_end(10)
        self.set_child(mainbox)


        self.entry = Gtk.Entry()
        self.entry.set_size_request(600, 40)
        self.entry.set_halign(Gtk.Align.CENTER)
        mainbox.append(self.entry)


        self.start_button_clicked = False
        self.button = Gtk.Button.new_with_label("Start")
        self.button.set_size_request(400, 80)
        self.button.connect("clicked", lambda btn:self.download_fn())
        self.button.set_halign(Gtk.Align.CENTER)
        self.button.set_size_request(100, 40)
        mainbox.append(self.button)


        separator = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)
        separator.set_size_request(5, -1)
        mainbox.append(separator)


        # Things will go here
        
    ##BOX FOR TEXTVIEW
        self.scrolled_window = Gtk.ScrolledWindow()
        self.scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)

        mainbox.append(self.scrolled_window)


        self.text_view = Gtk.TextView()
        self.text_view.set_editable(False)
        self.text_view.set_wrap_mode(Gtk.WrapMode.WORD)
        self.text_view.set_cursor_visible(False)
        self.text_view.set_hexpand(True)
        self.text_view.set_vexpand(True)
        self.scrolled_window.set_child(self.text_view)
        self.timer_id = None
        self.text_buffer = self.text_view.get_buffer()


## Actual Functional 100% confirmed functions
    def on_settings_button_clicked(self, button):
        settings_window = SettingsWindow(self)
        settings_window.present()
