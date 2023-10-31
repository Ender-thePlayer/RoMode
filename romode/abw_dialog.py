import gi
from os.path import expanduser
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
from gi.repository import Adw

def on_about_action(self):
        self.hide()
        dialog = Adw.AboutWindow.new()
        dialog.set_transient_for(self.MainWindow)
        dialog.set_application_name('Romanian Mode')
        dialog.set_version('0.2-alpha')
        dialog.set_developer_name('by EnderDatsIt')
        dialog.set_application_icon('face-wink')
        dialog.present()