# Copyright 2024 Robert Schroll
# This file is part of nbpreview, and is released under the BSD 2-clause license.

import nbformat
from nbconvert import HTMLExporter

from gi.repository import Gtk
from gi.repository.WebKit import WebView  # https://stackoverflow.com/a/60136494


@Gtk.Template(resource_path='/io/github/rschroll/nbpreview/window.ui')
class NbpreviewWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'NbpreviewWindow'

    webview = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.notebook = None
        self.webview.load_html('<h1>Open a File</h1>')

    def load_notebook(self, file):
        success, contents, _ = file.load_contents()
        if not success:
            print(f'Failed to load file contents')
            return

        notebook = nbformat.reads(contents, nbformat.NO_CONVERT)
        html, _ = HTMLExporter(template_name='classic').from_notebook_node(notebook)
        self.webview.load_html(html)
        self.set_title(file.get_basename())
        self.notebook = file.get_path()


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
