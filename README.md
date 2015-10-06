Introduction
============

This program summarises the resultant DNA methylation pattern data from the output of [Bismark](http://www.bioinformatics.babraham.ac.uk/projects/bismark/) bismark_methylation_extractor. Information of the DNA methylation positions for each amplicon, DNA methylation patterns observed within each amplicon and their abundance counts are summarised into a tab delimited text file amenable for further downstream statistical analysis. Methpat also outputs a HTML file containing visualisations of the methylation pattern data.

Homepage
--------

The [homepage for methpat](http://bjpop.github.io/methpat/) contains additional information about the program.


License
-------

Methpat is released as open source software under the terms of the 3 clause BSD License. See the file LICENCE.txt in the [source code repository of methpat](https://github.com/bjpop/methpat).

Installation
------------

Methpat currently requires version 2.7 of Python.

The best way to install Methpat is to use the following command:

    pip install git+https://github.com/bjpop/methpat.git

This will automatically download and install the dependencies of methpat.

Usage
-----

```
usage: methpat [-h] [--version] [--count_thresh THRESH] --amplicons
               AMPLICONS_FILE [--logfile FILENAME] [--html FILENAME]
               [--webassets {package,local,online}] [--title TITLE]
               BISMARK_FILE

Summarise methylation patterns in bismark output, and generate visualisation.

positional arguments:
  BISMARK_FILE          input bismark file

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  --count_thresh THRESH
                        only display methylation patterns with at least THRESH
                        number of matching reads, defaults to "0"
  --amplicons AMPLICONS_FILE
                        file containing amplicon information in TSV format
  --logfile FILENAME    log progress in FILENAME, defaults to "methpat.log"
  --html FILENAME       save visualisation in html FILENAME defaults to
                        "methpat.html"
  --webassets {package,local,online}
                        location of assets used by output visualisation web
                        page, defaults to "package"
  --title TITLE         title of the output visualisation page, defaults to
                        "Methylation Patterns"
```
