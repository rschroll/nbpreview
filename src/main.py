# Copyright 2024 Robert Schroll
# This file is part of nbpreview, and is released under the BSD 2-clause license.

# The webkit webview is blank without this.  But only in this application.  Other,
# simpler, setups work just fine.  Weird.
# https://www.reddit.com/r/suckless/comments/rprzrl/surf_shows_white_screen_on_most_sites/
# https://bugs.webkit.org/show_bug.cgi?id=238513 (Maybe)
import os
os.environ['WEBKIT_DISABLE_COMPOSITING_MODE'] = '1'


import sys
import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')
gi.require_version('WebKit', '6.0')

from gi.repository import Gtk, Gio, Adw
from .window import NbpreviewWindow, AboutDialog


class NbpreviewApplication(Adw.Application):
    """The main application singleton class."""

    def __init__(self):
        super().__init__(application_id='io.github.rschroll.nbpreview',
                         flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.create_action('quit', self.quit, ['<primary>q'])
        self.create_action('about', self.on_about_action)
        self.create_action('preferences', self.on_preferences_action)

    def do_activate(self):
        """Called when the application is activated.

        We raise the application's main window, creating it if
        necessary.
        """
        win = self.props.active_window
        if not win:
            win = NbpreviewWindow(application=self)
        win.present()

    def on_about_action(self, widget, _):
        """Callback for the app.about action."""
        about = AboutDialog(self.props.active_window)
        about.present()

    def on_preferences_action(self, widget, _):
        """Callback for the app.preferences action."""
        print('app.preferences action activated')
        wv = self.props.active_window.webview
        print(wv.get_size(0), wv.get_size(1))

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

