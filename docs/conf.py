#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# synerty-peek documentation build configuration file, created by
# sphinx-quickstart on Fri Dec 16 16:53:26 2016.
#
# This file is execfile()d with the current directory set to its
# containing dir.
#
# Note that not all possible configuration values are present in this
# autogenerated file.
#
# All configuration values have a default; values that are commented out
# serve to show the default.

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))

__project__ = 'Peek Plugin - Chat'
__copyright__ = '2016, Synerty'
__author__ = 'Synerty'
__version__ = '0.0.1'

import sphinx_rtd_theme


# -- General configuration ------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.githubpages']

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = '.rst'

# The master toctree document.
master_doc = 'index'

# General information about the project.
project = __project__
copyright = __copyright__
author = __author__

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.
#
# The short X.Y version.
# The full version, including alpha/beta/rc tags.
release = __version__

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This patterns also effect to html_static_path and html_extra_path
exclude_patterns = ['*Test.*', '_build', 'Thumbs.db', '.DS_Store']

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# If true, `todo` and `todoList` produce output, else they produce nothing.
todo_include_todos = False


# -- Options for HTML output ----------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "sphinx_rtd_theme"
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
# html_theme_options = {}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']


# -- Options for HTMLHelp output ------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = __project__+'doc'


# -- Options for LaTeX output ---------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, __project__+'.tex', __project__+' Documentation',
     __author__, 'manual'),
]


# -- Options for manual page output ---------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, __project__, __project__+' Documentation',
     [author], 1)
]


# -- Options for Texinfo output -------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, __project__, __project__+' Documentation',
     author, __project__, 'Pluggable platform for Python.',
     'Miscellaneous'),
]



###############################################################################
# Begin apidoc hack
###############################################################################

import shutil

import sphinx
from pytmpdir.Directory import Directory
from sphinx.apidoc import *


class _Opts:
    # 'Directory to place all output'
    destdir = None

    # 'file suffix (default: rst)', NO DOT '.'
    suffix = "rst"

    # 'Run the script without creating files'
    dryrun = False

    # 'Overwrite existing files'
    force = False

    # Don't create headings for the module/package
    # packages (e.g. when the docstrings already contain them)
    noheadings = False

    # 'Put module documentation before submodule documentation'
    modulefirst = True

    # 'Put documentation for each module on its own page'
    separatemodules = False

    # Follow symbolic links. Powerful when combined with collective.recipe.omelette.'
    followlinks = False

    # 'Interpret module paths according to PEP-0420 implicit namespaces specification'
    implicit_namespaces = False

    # 'Maximum depth of submodules to show in the TOC '
    maxdepth = 10

    # 'Include "_private" modules'
    includeprivate = False

    # 'Append module_path to sys.path, used when --full is given'
    append_syspath = True


def _listFiles(dir):
    ignoreFiles = set('.lastHash')
    paths = []
    for (path, directories, filenames) in os.walk(dir):

        for filename in filenames:
            if filename in ignoreFiles:
                continue
            paths.append(os.path.join(path[len(dir) + 1:], filename))

    return paths


def _fileCopier(src, dst):
    with open(src, 'rb') as f:
        contents = f.read()

    # If the contents hasn't change, don't write it
    if os.path.isfile(dst):
        with open(dst, 'rb') as f:
            if f.read() == contents:
                return

    with open(dst, 'wb') as f:
        f.write(contents)


def _syncFiles(srcDir, dstDir):
    if not os.path.isdir(dstDir):
        os.makedirs(dstDir)

    # Create lists of files relative to the dstDir and srcDir
    existingFiles = set(_listFiles(dstDir))
    srcFiles = set(_listFiles(srcDir))

    for srcFile in srcFiles:
        srcFilePath = os.path.join(srcDir, srcFile)
        dstFilePath = os.path.join(dstDir, srcFile)

        dstFileDir = os.path.dirname(dstFilePath)
        os.makedirs(dstFileDir, exist_ok=True)
        _fileCopier(srcFilePath, dstFilePath)

    for obsoleteFile in existingFiles - srcFiles:
        obsoleteFile = os.path.join(dstDir, obsoleteFile)

        if os.path.islink(obsoleteFile):
            os.remove(obsoleteFile)

        elif os.path.isdir(obsoleteFile):
            shutil.rmtree(obsoleteFile)

        else:
            os.remove(obsoleteFile)


def create_module_file(package, module, opts):
    """Build the text of the file and write the file."""
    raise Exception("create_module_file shouldn't get called")
    # text = format_heading(1, '(M) %s' % module)
    # # text += format_heading(2, ':mod:`%s` Module' % module)
    # text += format_directive(module, package)
    # write_file(makename(package, module), text, opts)


def create_package_file(root, master_package, subroot, py_files, opts, subs,
                        is_namespace):
    """Build the text of the file and write the file."""

    text = '.. _%s:\n\n' % makename(master_package, subroot)

    text += format_heading(1, '(P) %s' % subroot if subroot else master_package)
    text += format_directive(subroot, master_package)
    text += '\n'

    # build a list of directories that are szvpackages (contain an INITPY file)
    subs = [sub for sub in subs if path.isfile(path.join(root, sub, INITPY))]
    # if there are some package directories, add a TOC for theses subpackages

    if subs:
        text += '.. toctree::\n\n'
        for sub in subs:
            text += '    %s.%s\n' % (makename(master_package, subroot), sub)
        text += '\n'

    submods = [path.splitext(sub)[0] for sub in py_files
               if not shall_skip(path.join(root, sub), opts) and
               sub != INITPY]

    for submod in submods:
        text += format_heading(2, '(M) %s' % submod)
        text += format_directive(makename(subroot, submod), master_package)
        text += '\n'

    text += '\n'

    write_file(makename(master_package, subroot), text, opts)

def is_excluded(root, excludes):
    """Check if the directory is in the exclude list.

    Note: by having trailing slashes, we avoid common prefix issues, like
          e.g. an exlude "foo" also accidentally excluding "foobar".
    """

    fileName = os.path.basename(root)
    dirName = os.path.dirname(root)

    excludes = ['Test.py', 'setup.py']

    for exclude in excludes:
        if fileName.endswith(exclude):
            return True

    return False

# Overwrite the apidoc render methods with ours
sphinx.apidoc.create_package_file = create_package_file
sphinx.apidoc.create_module_file = create_module_file
sphinx.apidoc.is_excluded = is_excluded

def createApiDocs(modFileName):
    moduleName = os.path.basename(os.path.dirname(modFileName))

    rootpath = path.abspath(path.dirname(modFileName))
    realDstDir = os.path.join(os.path.dirname(__file__), "api_autodoc", moduleName)

    tmpDir = Directory()

    opts = _Opts()
    opts.destdir = tmpDir.path

    if not os.path.isdir(opts.destdir):
        os.makedirs(opts.destdir)

    modules = recurse_tree(rootpath, [], opts)
    # create_modules_toc_file(modules, opts)


    # Incrementally update files
    _syncFiles(tmpDir.path, realDstDir)



###############################################################################
# End apidoc hack
###############################################################################

# Create APIs with the AutoAPI hack above
import peek_plugin_chat
createApiDocs(peek_plugin_chat.__file__)

# import peek_platform
# createApiDocs(peek_platform.__file__)


