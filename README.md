# Notebook Preview

Notebook Preview is a small GTK application to display Jupyter Notebooks.  Its purpose is to allow the user to quickly read through a notebook without worrying about running Jupyter servers, kernels, or Python environments.

## Installation

Notebook Preview is available as a flatpak bundle for Linux systems.  You will need to [install flatpak](https://flatpak.org/setup/) if your distribution does have it installed.

Download the [`.flatpak` file](https://github.com/rschroll/nbpreview/releases/download/v0.1.0/io.github.rschroll.nbpreview.flatpak) from [Releases](https://github.com/rschroll/nbpreview/releases) page.  Then install it on your system with
```
flatpak install io.github.rschroll.nbpreview.flatpak
```

If you're not on a Linux system, good luck!

## Use

The installation should make Notebook Preview show up in your applications list.  It registers as a handler for notebook files, so you should be able to open notebooks in it by double-clicking them in a directory view.  You may need to adjust default file handlers if another tool is already registered as the default handler for notebook files.  (In GNOME, right-click a notebook file, choose _Properties_, and then select the _Open With_ tab.)

Once Notebook Preview is the default handler for notebook files, you can also open a notebook from the command line with the `open` or `xdg-open` commands.

## Building

Notebook Preview is developed in [GNOME Builder](https://wiki.gnome.org/Apps/Builder).  This does a wonderful job of hiding its build settings, but as best I can figure out, it's building with [`flatpak builder`](https://docs.flatpak.org/en/latest/building-introduction.html#flatpak-builder).

## License

Notebook Preview is copyright 2024 Robert Schroll and released under the BSD 2-clause license.  See COPYING for details.

The logo is derived from [the Noun Project](https://thenounproject.com/icon/jupiter-453568/).
