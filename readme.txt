Using the format of the probe_words.csv, you can run this analysis on any set of probe words.
To get data for the columns, run the "Word Match" analysis in Phon on a template session that includes target transcription of the probe words.
In the parameters, select "Include syllable boundaries" and "Include implicit boundaries"
The All Results Listing will give you most of the columns.

The CV column must include . for syllable boundaries.
If there are multiple words in a record, they will be made into separate rows. To combine them, merge the rows with a space between.
To simplify, combine multiple words into a single word.

For the syllabification column, go to Query > Data Tiers
Set Tier Name to "IPA Target"
run Query
Double-click the query result to open
In the window that opens, select "Edit table columns". Add "Target Syllables". Click OK. Export or copy the Target Syllables columns into the probe_words.csv

Then run word_analysis.py