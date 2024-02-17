# Copyright 2024 Robert Schroll
# This file is part of nbpreview, and is released under the BSD 2-clause license.

import nbformat
from nbconvert import HTMLExporter

from gi.repository import Gtk, WebKit
from gi.repository.WebKit import WebView  # https://stackoverflow.com/a/60136494


OPEN_URI = "/open-notebook"
OPEN_HTML = f"""
<html>
    <head>
        <style>
            body {{
                height: 100vh;
                margin: 0;
                display: flex;
                justify-content: center;
                align-items: center;
            }}
            button {{
                font-size: 2em;
                font-weight: bold;
                padding: 0.5em;
            }}
        </style>
    </head>
    <body>
        <form action="{OPEN_URI}" method="GET">
            <button type="submit">Open a Notebook</input>
        </form>
    </body>
</html>
"""


@Gtk.Template(resource_path='/io/github/rschroll/nbpreview/window.ui')
class NbpreviewWindow(Gtk.ApplicationWindow):
    __gtype_name__ = 'NbpreviewWindow'

    webview = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.notebook = None
        self.webview.load_html(OPEN_HTML)
        self.webview.connect('decide-policy', self.do_decide_policy)

    def do_decide_policy(self, webview, decision, decision_type):
        if decision_type != WebKit.PolicyDecisionType.NAVIGATION_ACTION:
            return False  # Handle as usual

        uri = decision.get_navigation_action().get_request().get_uri()
        if uri == 'about:blank':  # Loading a string
            return False  # No decision; continue as usual

        decision.ignore()
        if uri == OPEN_URI:
            self.get_application().activate_action('open')
        else:
            Gtk.UriLauncher.new(uri).launch()
        return True  # Stop other handlers

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
