# Copyright 2024 Robert Schroll
# This file is part of nbpreview, and is released under the BSD 2-clause license.

import sys
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
gi.require_version('WebKit', '6.0')

from gi.repository import GLib, Gtk, Gio, Adw
from .window import NbpreviewWindow, AboutDialog


class NbpreviewApplication(Adw.Application):
    """The main application singleton class."""

    def __init__(self):
        super().__init__(application_id='io.github.rschroll.nbpreview',
                         flags=Gio.ApplicationFlags.HANDLES_OPEN)
        self.create_action('quit', self.quit, ['<primary>q'])
        self.create_action('about', self.on_about_action)
        self.create_action('preferences', self.on_preferences_action)
        self.create_action('open', self.on_open, ['<primary>o'])

    def get_active_window(self):
        """Get or create a window."""
        win = self.props.active_window
        if not win:
            win = NbpreviewWindow(application=self)
        return win

    def do_activate(self):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """
        win = self.get_active_window()
        win.present()

    def do_open(self, files, _, _):
        for file in files:
            self.load_notebook(file)

    def on_about_action(self, widget, _):
        """Callback for the app.about action."""
        about = AboutDialog(self.props.active_window)
        about.present()

    def on_preferences_action(self, widget, _):
        """Callback for the app.preferences action."""
        print('app.preferences action activated')

    def on_open(self, widget, _):
        """Callback for the app.open action."""
        win = self.get_active_window()

        filt = Gtk.FileFilter()
        filt.set_name("Notebooks")
        filt.add_mime_type('application/x-ipynb+json')

        filts = Gio.ListStore.new(Gtk.FileFilter)
        filts.append(filt)

        dialog = Gtk.FileDialog()
        dialog.set_title("Open Notebook")
        dialog.set_filters(filts)
        dialog.set_default_filter(filt)
        dialog.open(win, None, self.on_open_callback)

    def on_open_callback(self, dialog, result):
        """Callback to finish the app.open action."""
        try:
            file = dialog.open_finish(result)
            if file:
                self.load_notebook(file)
        except GLib.Error as error:
            print(f'Error opening file: {error.message}')

    def load_notebook(self, file):
        for win in self.get_windows():
            if win.notebook == file.get_path():
                win.present()
                return
            if not win.notebook:
                break
        else:
            win = NbpreviewWindow(application=self)
        win.load_notebook(file)
        win.present()

    def create_action(self, name, callback, shortcuts=None):
        """Add an application action.

        Args:
            name: the name of the action
            callback: the function to be called when the action is
              activated
            shortcuts: an optional list of accelerators
        """
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)


def main(version):
    """The application's entry point."""
    app = NbpreviewApplication()
    return app.run(sys.argv)

