# docs/source/conf.py

import os
import sys
import django

sys.path.insert(0, os.path.abspath('/home/s102/gymquestkingdomZ/'))

# Обязательно укажи модуль настроек Django
os.environ['DJANGO_SETTINGS_MODULE'] = 'GymQuest.settings'
django.setup()

# -- Project information -----------------------------------------------------
project = 'GymQuestKingdom'
copyright = '2026, Лучшая команда красавчиков'
author = 'Лучшая команда красавчиков'
release = '1.0'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
]

templates_path = ['_templates']
exclude_patterns = []

language = 'ru'

# -- Options for autodoc -----------------------------------------------------
autodoc_mock_imports = [
    'django',
]

# -- Options for Napoleon (Google style) ------------------------------------
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True

# -- Options for HTML output -------------------------------------------------
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']