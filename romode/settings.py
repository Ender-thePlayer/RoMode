import sys
import gi
import os
import subprocess
import json
from os.path import expanduser
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from functools import partial
from romode.abw_dialog import on_about_action
from romode.functions import *
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Gtk, Adw, Gio, GLib, Gdk


class SettingsWindow(Gtk.Window):
    def __init__(self, parent_window, config_file):

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


        self.MainWindow = parent_window

        ## Window properties
        super().__init__(title="Settings")
        self.set_transient_for(parent_window)
        self.set_modal(True)
        self.set_default_size(600, 350)

        self.settings_header = Gtk.HeaderBar()
        self.set_titlebar(self.settings_header)
        self.set_resizable(False)


        ## Main box for the settings window
        mainsettings_hbox = Gtk.Box.new(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
        mainsettings_hbox.set_margin_top(margin=12)
        mainsettings_hbox.set_margin_end(margin=12)
        mainsettings_hbox.set_margin_bottom(margin=12)
        mainsettings_hbox.set_margin_start(margin=12)
        self.set_child(child=mainsettings_hbox)


        ## Main for the left side buttons and the buttons
        leftside_vbox = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=12)
        mainsettings_hbox.prepend(child=leftside_vbox)

        importbtn = Gtk.Button(label="Import")
        leftside_vbox.append(importbtn)

        exportbtn = Gtk.Button(label="Export")
        leftside_vbox.append(exportbtn)

        aboutbtn = Gtk.Button(label="About")
        aboutbtn.connect("clicked", lambda btn:on_about_action(self))
        leftside_vbox.append(aboutbtn)

        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        separator.set_size_request(-1, 50)
        mainsettings_hbox.append(separator)

        rightside_vbox = Gtk.Box.new(orientation=Gtk.Orientation.VERTICAL, spacing=12)

        spotifycat_label = Gtk.Label()
        spotifycat_label.set_markup("<span size='20000'>Spotify</span>")
        spotifycat_label.set_halign(Gtk.Align.START)
        rightside_vbox.append(spotifycat_label)

        id_entry_label = Gtk.Label(label="Spotify Client ID")
        id_entry_label.set_halign(Gtk.Align.START)
        rightside_vbox.append(id_entry_label)

        id_entry = Gtk.Entry()
        id_entry.set_size_request(600, 40)
        id_entry.set_halign(Gtk.Align.CENTER)
        id_entry.set_placeholder_text("Enter your Spotify Client ID here")
        id_entry.connect("changed", on_id_entry_changed)
        rightside_vbox.append(id_entry)

        secret_entry_label = Gtk.Label(label="Spotify Client Secret")
        secret_entry_label.set_halign(Gtk.Align.START)
        rightside_vbox.append(secret_entry_label)

        secret_entry = Gtk.Entry()
        secret_entry.set_size_request(600, 40)
        secret_entry.set_halign(Gtk.Align.CENTER)
        secret_entry.connect("changed", on_secret_entry_changed)
        rightside_vbox.append(secret_entry)

        spotify_client_secret = data.get('spotify_client_secret', None)
        # theme = data.get('theme', None)

        if spotify_client_secret is not None and spotify_client_secret != "":
            secret_entry.set_text(spotify_client_secret)
        else:
            secret_entry.set_placeholder_text("Enter your Spotify Client Secret here")

        leftside_settings_separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        leftside_settings_separator.set_size_request(5, -1)
        rightside_vbox.append(leftside_settings_separator)

        misccat_label = Gtk.Label()
        misccat_label.set_markup("<span size='20000'>Theming</span>")
        misccat_label.set_halign(Gtk.Align.START)
        rightside_vbox.append(misccat_label)

        misc_toggle_button = Gtk.Button(label="Switch Theme")
        misc_toggle_button.connect("clicked", partial(switch_theme, self))
        rightside_vbox.append(misc_toggle_button)


        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.NEVER, Gtk.PolicyType.AUTOMATIC)
        scrolled_window.set_child(rightside_vbox)

        mainsettings_hbox.append(scrolled_window)

