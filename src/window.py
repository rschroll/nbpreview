# Copyright 2024 Robert Schroll
# This file is part of nbpreview, and is released under the BSD 2-clause license.

from gi.repository import Gtk
from gi.repository.WebKit import WebView  # https://stackoverflow.com/a/60136494


@Gtk.Template(resource_path='/io/github/rschroll/nbpreview/window.ui')
class NbpreviewWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'NbpreviewWindow'

    webview = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.webview.load_uri('https://google.com')


class AboutDialog(Gtk.AboutDialog):

    def __init__(self, parent):
        Gtk.AboutDialog.__init__(self)
        self.props.program_name = 'nbpreview'
        self.props.version = "0.1.0"
        self.props.authors = ['Robert Schroll']
        self.props.copyright = '2024 Robert Schroll'
        self.props.logo_icon_name = 'io.github.rschroll.nbpreview'
        self.props.modal = True
        self.set_transient_for(parent)
