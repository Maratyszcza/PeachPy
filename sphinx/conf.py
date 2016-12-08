import sphinx_bootstrap_theme
from peachpy import __version__

extensions = [
    'sphinx.ext.autodoc'
]

source_suffix = '.rst'
master_doc = 'index'

autoclass_content = "both"

project = u'PeachPy'
copyright = u'2013-2015, Georgia Institute of Technology'

version = __version__
release = __version__

pygments_style = 'sphinx'

html_theme = 'bootstrap'
html_theme_path = sphinx_bootstrap_theme.get_html_theme_path()
