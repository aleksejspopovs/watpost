Overview
========

![Watpost screenshot](http://f.nn.lv/mk/qt/z3/screenshot.png "Watpost")

Watpost is a command-line application meant to allow you to track your parcels sent via carriers such as USPS. It features an extensible system that allows easily adding new carriers and highly customizable output layout.

Supported carriers
==================

You can find out which carriers are supported by your install of Watpost by using the `-c` command-line switch.

At the moment, only two carriers are supported in the main branch:

* United States Postal Service (USPS), the national postal service of the US
    * the implementation has a hardcoded API key inside. I hope that USPS aren't going to ban the key for that, but if they do, you'll have to get your own key (if this happens, I'll provide everything needed to quickly acquire one).
* Latvijas Pasts (LP), the national postal service of Latvia
    * the implementation relies on parsing LP's tracking web page, therefore it might break in the future. Unfortunately, there's not much I can do, as LP doesn't provide an API.

Support for more carriers is in the works. Pull requests implementing new carriers would be highly appreciated.

Development
===========

`README.md` deals with basic usage of Watpost. To learn how to contribute to Watpost, see `DEVELOPMENT.md`.

Source code of Watpost is available under a very relaxed license, which you can find in `LICENSE.md`.

Dependencies & Installation
===========================

Watpost requires Python 3 to run. No external libraries are necessary to run 'bare' Watpost, but the providers (i.e. the implementations of various carriers' tracking services) have their own dependencies:

* `python-requests` is required by LP and USPS
* `pytz` is required by LP and USPS
* `BeautifulSoup 4` is required by LP
* `python-lxml` is required by USPS

There is no installation process required, though you'll probably want to do the following:

* copy the default configuration to your config directory (see below for this) and adjust it to suit your needs
* create a symlink for `watpost.py` somewhere in your PATH (e.g. in `~/bin`, `/usr/local/bin` or `/usr/bin`)

Configuration
=============

The default directory for storing Watpost's configuration files is determined as follows:

* if you're using Windows, it's `%APPDATA%\Watpost`
* if the environment variable `XDG_CONFIG_HOME` is set to something, it's `$XDG_CONFIG_HOME/watpost`
* otherwise, it's `~/.config/watpost` (where `~` is resolved to your home directory)

Watpost expects to find files named `settings.json` and `parcels.json` in these directories, although you can specify alternative paths using command-line arguments `-s` and `-p`.

`settings.json` contains Watpost's settings, mostly pertraining to the way data is displayed. The syntax of templates should be familiar to anyone who has ever used Python's `.format()` function. If you aren't familiar with it, everything you need to know is that `{varname}` in the template will be replaced with contents of a variable named `varname`, `\n` will be replaced with a line break and pretty much everything else will be left as it was. All of the configuration keys are commented in the default `settings.json` and are set to reasonable defaults, therefore I don't see any need to comment on them here. There are some examples of various layouts that can be achieved in `EXAMPLES.md`.

`parcels.json` contains a list of parcels that Watpost will track. The structure is very simple, so the supplied example should be enough to understand it.

Integration with stuff
======================

I personally use Watpost with Conky to display the states of my parcels on my desktop. To do this, insert `${texeci 600 watpost}` in an appropriate place in your `.conkyrc` file, possibly replacing the 600 second interval with one that suits you the best.
