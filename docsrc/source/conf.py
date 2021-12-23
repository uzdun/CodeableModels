# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import sys

# sys.path.insert(0, os.path.abspath('C:/work/dev/python/CodeableModelsDocs/'))
print("PATH = %s" % sys.path)

# -- Project information -----------------------------------------------------

project = 'CodeableModels'
copyright = '2016-2021, Uwe Zdun'
author = 'Uwe Zdun'

# The full version, including alpha/beta/rc tags
release = '1.00'

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autodoc', 'sphinx.ext.napoleon', 'sphinx.ext.autosummary', 'sphinx_rtd_theme',
              'sphinx_markdown_builder', 'sphinxcontrib.images'
              ]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = [
    'build/*'
]

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# document class and __init__ docstrings
autoclass_content = 'both'

# generate class stubs
autosummary_generate = True

# don't show rst sources in HTML
html_show_sourcelink = False
