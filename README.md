TABLE OF CONTENTS
=================
* What Is PyD3 About?
* Which ID3 Tags Can Be Treated?
* Which Operating Systems Are Supported?
* What I Need To PyD3 My Music Library?
  + Prerequisites
  + Python Installation
  + Libraries Installation
  + Use It: PyD3 Your Music Library (or part of it)
* Are There Any Assumptions?
* Has PyD3 A License?
* Has PyD3 Any Cost?
* What Is Next?


What Is PyD3 About?
===================
**PyD3 is a quick [ID3](http://en.wikipedia.org/wiki/ID3 "wikipedia/ID3") data management of [MP3](http://en.wikipedia.org/wiki/Mp3 "wikipedia/MP3") files** which it has been built up into a script process. PyD3 will put your music library into place.


Which ID3 Tags Can Be Treated?
==============================
The ID3 tags which can be treated are: Track number, Album, Artist, Title, Genre, Year.
Images can be attached to a tune: Front Cover, Back Cover & Media (e.g. label side of CD).

**Note: Data of other ID3 tags will be removed.**


Which Operating Systems Are Supported?
======================================
PyD3 is a cross-platform app. This means that the same program will run on multiple platforms without modification. Microsoft Windows and Unix based systems like GNU/Linux and OSX are supported.


What I Need To PyD3 My Music Library?
=====================================
This guide is designed to point you to the best information about getting started with PyD3. 

Prerequisites
-------------
To PyD3 your music library, or just a simple folder, you must have the following stuff installed in your Operating System -- Python and a set of Python libraries (Mutagen, PIL)

* Python 2.7+ *An interpreted, object-oriented programming language.*
* Mutagen 1.20 *A Python module to handle audio metadata.*
* PIL 1.1.17 *Python Imaging Library.*

Python Installation
-------------------
Most of Operating Systems such as OS-X and GNU/Linux distributions come with a preinstalled version of Python. Check Python version on your shell terminal application. `$ python -V`
If you are on Windows you will need to install it from [www.python.org](http://www.python.org "http://www.python.org").

**Note: Do not install Python 3+.**

Libraries Installation
----------------------
A couple os Python libraries are required for a PyD3. A possible way to install them on the most popular architectures Operating Systems is described bellow.

* OSX: Darwin ports repository (MacPorts base version 2.0.3 was used).

`sudo port install py27-mutagen py27-pil`

* Ubuntu: Apt-Get repositories for latest Ubuntu releases. There should be no problem with GNU/Linux Debian based distros. 

`sudo apt-get install python-mutagen python-imaging`

* Windows: There is no official repository for any Windows version.

Download and install the appropriate Python 2.7+ libraries. [Mutagen](http://code.google.com/p/mutagen/downloads/list "code.google.com/mutagen") & [PIL](http://www.pythonware.com/products/pil "pythonware.com/pil").
    
Use It: PyD3 Your Music Library (or part of it)
----------------------------------------------
If it is your first time that you execute PyD3, test it. Use it for example over a directory which contains your lasted tune files.
Execute terminal/console application and surf to the directory where is located pyd3_id.py --with "cd command". 
After that, write python reference program --if you have an alias, puts easier the execution--

	python pyd3_it.py /path/to/your/directory/music /target/path/directory/

Are There Any Assumptions?
==========================
Yes, There are some assumptions that you need to be aware of.

* Only mp3 files are considered as tunes.
* Directories are considered as containers of tunes.
* Each directory might have a cover image, file named as cover.ext or front.ext, which will be attached into ID3 file tune(s). Clarification: .ext must be: .jpg, .jpeg, .png

Note: In case that there is no cover image in tunes container, no worries, there is an option on the menu which allows to include a cover image --whatever name is.

Has PyD3 A License?
===================
PyD3 is open source which means that it is free for anyone to use and the source code is available for anyone to look at and modify it.
Also anyone can contribute on fixes or enhancements to the project.


Has PyD3 Any Cost?
==================
PyD3 is free to edit and also free to use it --you can use it free as any times you want with no cost. No cash is demanded, but it will be appreciated. ;). 


What Is Next?
=============
Use it as many times you want/need. If any improvement raises into you or a bug is found, you can also share it at jordi.marin.valle(at)gmail.com.
