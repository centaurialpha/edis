========
Edis-IDE
========

.. image:: ./src/images/sources/logo.png

.. Contents::
    :backlinks: none

.. sectnum::

What is this?
=============

**Edis** is a free cross-platform IDE for C programming language, developed in pure Python, using PyQt for the UI, has simple interface but with advanced functionalities, is based on simplicity: *¡write, compile and run!*

.. image:: ./src/images/sources/edis_screenshot.png

Awesome features
================

* **Syntax highlighter**
* **Code folding**
* **Minimap**
* **Highlighting words**
* **Code style checker**
* **File selector**
* **Tree symbols**
* **Auto completion based on document and keywords**
* **Markers**

Platforms
=========

* GNU/Linux
* Windows
     
Installing and running
======================

Prerequisites
-------------

* `Python <https://python.org>`_ 3.x
* `PyQt4 <http://www.riverbankcomputing.co.uk/software/pyqt/intro>`_ >= 4.8
* `QScintilla2 <http://www.riverbankcomputing.com/software/qscintilla/intro>`_
* `Ctags <http://ctags.sourceforge.net/>`_

Easy install
------------

*GNU/Linux:*

Download source code from  `here <https://github.com/centaurialpha/edis/releases>`_ or clone the repository:

::

    git clone https://github.com/centaurialpha/edis.git
    cd edis
    sudo python setup.py install
    
Running from source code
------------------------

::

   cd edis
   python bin/edis

*Windows:*

Binaries are `here <https://github.com/centaurialpha/edis/releases>`_

Tests status
============

**Edis** has automated tests that run through  `Travis CI <https://travis-ci.org>`_.
The current status is as follows:

.. image:: https://travis-ci.org/centaurialpha/edis.svg?branch=master
     :target: https://travis-ci.org/centaurialpha/edis

Contact
=======

* `Edis Web <http://centaurialpha.github.io/edis>`_
* `Mailing list <http://groups.google.com/group/edis-ide/topics>`_

Contributing
============

To contribute to the project please read the following: `Contributing Edis <https://github.com/centaurialpha/edis/blob/master/CONTRIBUTING.md>`_.

License
=======

* **Edis** is Free Software! distributed under the terms of the `GPLv3+ <http://gnu.org/licenses/gpl.html>`_.
