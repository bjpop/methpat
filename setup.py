#!/usr/bin/env python

from distutils.core import setup

setup(
    name='methpat',
    version='1.4.0',
    author='Bernie Pope',
    author_email='bjpope@unimelb.edu.au',
    packages=['methpat'],
    package_dir={'methpat': 'methpat'},
    package_data={'methpat': ['data/*.js']},
    scripts=[],
    entry_points={
        'console_scripts': ['methpat = methpat.methpat:main']
    },
    url='https://github.com/bjpop/methpat',
    license='LICENSE.txt',
    description=(
        'This program summarises the resultant DNA methylation '
        'pattern data from the output of bismark_methylation_extractor.'),
    long_description=(
        'This program summarises the resultant DNA methylation '
        'pattern data from the output of bismark_methylation_extractor. '
        'Information of the DNA methylation positions for each amplicon, '
        'DNA methylation patterns observed within each amplicon and their '
        'abundance counts are summarised into a tab delimited text file '
        'amenable for further downstream statistical analysis and visualization.'),
    install_requires=[],
)
