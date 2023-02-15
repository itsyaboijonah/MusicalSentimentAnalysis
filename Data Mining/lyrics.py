# Dorian Desblancs - 260722712
# COMP 550 - Final Project lyrics extraction

# Running the script (terminal):

# python3 lyrics.py file1 file2
# file1 denotes xlsx Moodylyrics file with artist, track name, and sentiment annotations
# file2 denotes txt file output

"""
The lyricwikicase, lyricwikipagename, lyricwikiurl, and getlyrics are from Bart Nagel's
script 'lyrics.py'. The rest of the code was built by me in order to extract the text files
with Moodylyrics tracks lyrics and sentiment.
"""

# Bart Nagel Copyright and information about original script
"""
Copyright 2009~2018 Bart Nagel (bart@tremby.net) and other authors

This program is free software: you can redistribute it and/or modify it under 
the terms of the GNU General Public License as published by the Free Software 
Foundation, either version 3 of the License, or (at your option) any later 
version.

This program is distributed in the hope that it will be useful, but WITHOUT ANY 
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A 
PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with 
this program. If not, see <http://www.gnu.org/licenses/>.
"""

NAME = "lyrics"
VERSION = "2.0"
DESCRIPTION = """Python script making use of LyricWiki (lyrics.wikia.com) to pull 
lyrics from the web from the commandline"""
AUTHOR = "Bart Nagel"
AUTHOR_EMAIL = "bart@tremby.net"
URL = "http://github.com/tremby/py-lyrics"
LICENSE = "Gnu GPL v3"

import urllib
import sys
import os
import re
import subprocess
import lxml.html
from urllib.request import urlopen
import pandas as pd

def lyricwikicase(s):
	"""Return a string in LyricWiki case.
	Substitutions are performed as described at 
	<http://lyrics.wikia.com/LyricWiki:Page_Names>.
	Essentially that means capitalizing every word and substituting certain 
	characters."""

	words = s.split()
	newwords = []
	for word in words:
		newwords.append(word[0].capitalize() + word[1:])
	s = "_".join(newwords)
	s = s.replace("<", "Less_Than")
	s = s.replace(">", "Greater_Than")
	s = s.replace("#", "Number_") # FIXME: "Sharp" is also an allowed substitution
	s = s.replace("[", "(")
	s = s.replace("]", ")")
	s = s.replace("{", "(")
	s = s.replace("}", ")")
	try:
		# Python 3 version
		s = urllib.parse.urlencode([(0, s)])[2:]
	except AttributeError:
		# Python 2 version
		s = urllib.urlencode([(0, s)])[2:]
	return s

def lyricwikipagename(artist, title):
	"""Return the page name for a set of lyrics given the artist and 
	title"""

	return "%s:%s" % (lyricwikicase(artist), lyricwikicase(title))

def lyricwikiurl(artist, title, edit=False, fuzzy=False):
	"""Return the URL of a LyricWiki page for the given song, or its edit 
	page"""

	if fuzzy:
		base = "https://lyrics.fandom.com/index.php?search="
		pagename = artist + ':' + title
		if not edit:
			url = base + pagename
			doc = lxml.html.parse(url)
			return doc.docinfo.URL
	else:
		base = "https://lyrics.fandom.com/wiki/"
		pagename = lyricwikipagename(artist, title)
	if edit:
		if fuzzy:
			url = base + pagename
			doc = lxml.html.parse(url)
			return doc.docinfo.URL + "&action=edit"
		else:
			return base + "index.php?title=%s&action=edit" % pagename
	return base + pagename

def getlyrics(artist, title, fuzzy=False):
	"""Get and return the lyrics for the given song.
	Raises an IOError if the lyrics couldn't be found.
	Raises an IndexError if there is no lyrics tag.
	Returns False if there are no lyrics (it's instrumental)."""

	if (isinstance(artist, int)):
		artist = str(artist)
	
	if (isinstance(title, int)):
		title = str(title)

	try:
		doc = lxml.html.parse(urlopen(lyricwikiurl(artist, title, fuzzy=fuzzy)))
	except IOError:
		raise

	try:
		lyricbox = doc.getroot().cssselect(".lyricbox")[0]
	except IndexError:
		raise

	# look for a sign that it's instrumental - return empty string if so
	if len(doc.getroot().cssselect(".lyricbox a[title=\"Instrumental\"]")):
		return ""

	# Prepare output
	lyrics = []
	if lyricbox.text is not None:
		lyrics.append(lyricbox.text)
	for node in lyricbox:
		if str(node.tag).lower() == "br":
			lyrics.append("\n")
		if node.tail is not None:
			lyrics.append(node.tail)
	return "".join(lyrics).strip()

# Return tracks and their sentiments
def gettracks(f):
	songs = pd.read_excel(f, skiprows=15, usecols=[1, 2])
	sentiments = pd.read_excel(f, skiprows=15, usecols=[3])
	songs = songs.values.tolist()
	sentiments = sentiments.values.tolist()
	flat_list = []
	for sublist in sentiments:
		for item in sublist:
			flat_list.append(item)
	return songs, flat_list

# Get lyrics for all tracks in dataset
def getalllyrics(songs):
	lyrics = []
	l = len(songs)
	print("Getting All Lyrics (This may take a while!)... ")
	index = 0
	for song in songs:
		artist = song[0]
		title = song[1]
		lyr = getlyrics(artist, title, fuzzy=False)
		lyr = lyr.replace('\n', '. ')
		lyrics.append(lyr)
		if (index % 100 == 0):
			print("Index: %i out of %i..." % (index, l))
		index = index + 1
	print("Done Getting Lyrics!\n")
	return lyrics

# Output lyrics to text files, line by line
# Comment or uncomment lines depending on binary/multiclass!
def totext(sentiments, lyrics, fi):
	print("Output lyrics to file...")
	with open(fi, 'w') as f:
		for x in range(len(lyrics)):
			if (sentiments[x] == 'neg'):
				sent = 0
				f.write("%s %s\n" % (str(sent), lyrics[x]))
			elif (sentiments[x] == 'pos'):
				sent = 1
				f.write("%s %s\n" % (str(sent), lyrics[x]))
			else:
				continue
			"""
			if (sentiments[x] == 'happy'):
				sent = 1
				f.write("%s %s\n" % (str(sent), lyrics[x]))
			elif (sentiments[x] == 'angry'):
				sent = 2
				f.write("%s %s\n" % (str(sent), lyrics[x]))
			elif (sentiments[x] == 'sad'):
				sent = 3
				f.write("%s %s\n" % (str(sent), lyrics[x]))
			elif (sentiments[x] == 'relaxed'):
				sent = 4
				f.write("%s %s\n" % (str(sent), lyrics[x]))
			else:
				continue
			"""
	print("Done!\n")

def main():
	try:
		f_to_mine = sys.argv[1]
		f_to_out = sys.argv[2]
		songs, sentiments = gettracks(f_to_mine)
		totext(sentiments, getalllyrics(songs), f_to_out)
	except:
		print("File Paths provided are not adequate!")

main()