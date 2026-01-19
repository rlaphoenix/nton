#!/usr/bin/env sh
pyside6-rcc nton/gui/resources/icons.qrc -o nton/gui/resources/icons_rc.py
pyside6-uic nton/gui/main.ui -o nton/gui/main.py --absolute-imports --python-paths "."
