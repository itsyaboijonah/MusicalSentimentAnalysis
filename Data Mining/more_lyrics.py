# Dorian Desblancs - 260722712
# COMP 550 - Final Project lyrics extraction for SebinDuke Dataset

import pandas as pd

# Extract track lyrics and sentiments
def get_tracks(f):
    lyrics = pd.read_csv(f, usecols=[5], header=None, encoding="utf-8")
    sentiments = pd.read_csv(f, usecols=[4], header=None, encoding="utf-8")
    lyrics = lyrics.values.tolist()
    sentiments = sentiments.values.tolist()
    flat_list1 = []
    for sublist in sentiments:
        for item in sublist:
            flat_list1.append(item)
    flat_list2 = []
    for sublist in lyrics:
        for item in sublist:
            _item = item.replace('â', "\'")
            _item = _item.replace('¦', '')
            _item = _item.replace('ï¼', '\'')
            _item = _item.replace('\\', '')
            flat_list2.append(_item)
    return flat_list1, flat_list2

# Output lyrics to text files, line by line
def totext(sentiments, lyrics, fi):
	with open(fi, 'w') as f:
		for x in range(len(lyrics)):
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

def main():
    sentiments1, lyrics1 = get_tracks('Other Dataset/Test.csv')
    sentiments2, lyrics2 = get_tracks('Other Dataset/Train.csv')
    sentiments = sentiments1 + sentiments2
    lyrics = lyrics1 + lyrics2
    totext(sentiments, lyrics, 'more_lyrics.txt')

main()