TTS Text Cleaner for Voice Clone App
===========================================================

This module is for cleaning up text for use in the Voice Clone App.

It accepts a full script such as an ebook in .txt format and returns 
a text file ready to be used in the Voice Clone App dataset creator.

There's no current way to use the module without getting into the code,
but I will be adding a CLI interface soon.

"""

Currently it is capable of:

 - Changing numbers from numerals to words
   - including years
 - Splicing some multi-line titles into a single line
 - Removing unprintable characters
 - Removing problematic whitespace characters
 - Encodes to UTF-8

Future features include:

 - A CLI interface
 - Removing citation lists
 - Removing footnotes
 - Removing tables and other non-standard text

Features I'd like but cannot promise:

 - Conversion from ePub to txt
 - Conversion from HTML to txt
 - Running a pre-conversion check of the text against the audio
 - A GUI, possibly one that integrates with the VCA Flask page
 - A full fork of VCA with the added text-cleaning and other wish-list features

"""
