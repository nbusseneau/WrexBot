# -*- coding: utf-8 -*-

from os.path import normpath, join, dirname

# Datetime format for logs and stdout
DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
# Plugins
PLUGIN_DIR = normpath(join(dirname(__file__), 'plugins'))
PLUGINS = [] # list here any plugin you want to use