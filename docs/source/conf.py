# Configuration file for the Sphinx documentation builder.
import os
import sys
sys.path.insert(0, os.path.abspath('../..'))

# -- Project information -----------------------------------------------------
project = 'pyLOM'
copyright = '2024, [Your Name]'
author = '[Your Name]'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.duration',
    'sphinx.ext.doctest',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    'sphinx_copybutton',
    'sphinx.ext.mathjax',
    'sphinx_design',
]

templates_path = ['_templates']
exclude_patterns = []

# -- Options for autodoc ----------------------------------------------------
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'show-inheritance': True,
    # 'special-members': '__init__',
    'ignore-module-all': True,  # If True, ignore __all__ variable defined in the package's __init__.py
    'undoc-members': False, # If True, include members without docstrings
    'exclude-members': '__weakref__'
}
# without this, the undocumented members are still shown, even with undoc-members=False
autodoc_member_order = 'bysource'
autodoc_preserve_defaults = True


# -- Options for Napoleon --------------------------------------------------
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = True
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_use_ivar = True
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_type_aliases = None

# -- Intersphinx configuration --------------------------------------------
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'numpy': ('https://numpy.org/doc/stable/', None),
    'scipy': ('https://docs.scipy.org/doc/scipy/', None),
    'torch': ('https://pytorch.org/docs/stable/', None),
}

# -- Options for HTML output ----------------------------------------------
html_theme = 'pydata_sphinx_theme'
html_theme_options = {
    "github_url": "https://github.com/ArnauMiro/pyLowOrder",
    "use_edit_page_button": True,
    "show_nav_level": 2,
    "show_toc_level": 2,
    "navigation_depth": 4,
    "collapse_navigation": False,
    "logo": {
        "text": "pyLOM",
    },
}

# These folders are copied to the documentation's HTML output
html_static_path = ['_static']
html_css_files = [
    'custom.css',
]
# html_favicon = '_static/placeholder_favicon.ico'
# -- Options for HTML theme -----------------------------------------------
html_context = {
    "github_user": "ArnauMiro",
    "github_repo": "pyLowOrder",
    "github_version": "master",
    "doc_path": "docs/source",
}