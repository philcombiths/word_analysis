"""
Updated: 1/7/2021
Author: Philip Combiths

word_analysis takes input from the "Word Match" analysis in Phon, saved to a
file named "probe_words.csv" in the specified input directory and generates
syllable- and word-level information about the phones in each word. See readme
for details about the input file.

WARNING: Currently only compatible with *Spanish* (max 2-element onsets and no
                                                   coda clusters)
         
         For other languages, regex needs to be modified to specify singleton
         vs. cluster codas, include larger clusters, and include left/right 
         appendices, OEHS, and other syllable constituent labels.
         
Usage Steps:
    1. Generate "Word Match" analysis in Phon (see readme)
    2. Save data as "probe_words.csv"
    3. Generate Target Syllables in Phon (see readme)
    4. Copy Target Syllables to "probe_words.csv"
    5. Run word_analysis.py
    6. Specify input/output directories

"""

# -*- coding: utf-8 -*-
# ------------------------------
# Python 3.5
# To-do
# Set directory for input and output.

#### Step 0: Preliminaries
import os
import pandas as pd
import numpy as np

# User input CSV directory path
path = os.path.normpath(input("Enter CSV directory path: "))
if len(path) <= 2:
    path = os.path.normpath("E:\My Drive\Phonological Typologies Lab\Current Probes\EFE (Spanish Probe)\Word Lists and Analyses\EFE\Python Word Analysis\Input")
    print("Default path set to", path)
    
out_path = os.path.normpath(input("Enter output directory path for CSV files: "))
if len(out_path) <= 2:
    out_path = os.path.normpath("E:\My Drive\Phonological Typologies Lab\Current Probes\EFE (Spanish Probe)\Word Lists and Analyses\EFE\Python Word Analysis\Output")
    print("Default path set to", out_path)


# Set CSV file
file = 'probe_words.csv'
file_path = os.path.join(path, file)

# Read CSV into pandas dataframe
data = pd.read_csv(file_path, encoding='utf-8')

# Add Consonant and Vowel Columns (remove dental diacritic)
data['Consonants'] = data['Target'].str.replace(r'[aeiouˈ̪]', r'')
data['Vowels'] = data['Target'].str.replace(r'[^aeiou]', r'')

# Remove dental diacritic from Target Syllables
data['Target Syllables'] = data['Target Syllables'].str.replace(r'̪', r'')

### Syllable position
##
#

# Create onset_dataframe extracting onsets from target syllables
onset_data = data['Target Syllables'].str.extractall(r'(.):O')
# group by first level of multi-index to create all onset consonants columnm
data['Onset'] = onset_data.groupby(level=0)[0].apply(lambda x: ' '.join(x))

# Create onset_singleton dataframe
onset_singleton_data = data['Target Syllables'].str.extractall(r'(?:^|ˈ|[CND])(.):O(?=.:[N|D])')
# group by first level of multi-index to create all onset singleton columnm
data['Onset Singleton'] = onset_singleton_data.groupby(level=0)[0].apply(lambda x: ' '.join(x))

# Create singleton dataframe
VCV_data = data['Target Syllables'].str.extractall(r'[ND]ˈ?(.):[OC].:[DN]')
# group by first level of multi-index to create all VCV columnm
data['Intervocalic Singleton'] = VCV_data.groupby(level=0)[0].apply(lambda x: ' '.join(x))

# Intervocalic_singleton dataframe
VCV_onset_data = data['Target Syllables'].str.extractall(r'[ND]ˈ?(.):O.:[DN]')
# group by first level of multi-index to create all VCV columnm
data['Intervocalic Singleton Onset'] = VCV_onset_data.groupby(level=0)[0].apply(lambda x: ' '.join(x))

# Create coda_dataframe extracting codas from target syllables
coda_data = data['Target Syllables'].str.extractall(r'(.):C')
# group by first level of multi-index to create all coda consonants columnm
data['Coda'] = coda_data.groupby(level=0)[0].apply(lambda x: ' '.join(x))

# Create onset_cluster_dataframe extracting from target syllables
onset_cluster_data = data['Target Syllables'].str.extractall(r'(.):O(.):O')
onset_cluster_data['all'] = onset_cluster_data[0]+onset_cluster_data[1]

# group by first level of multi-index to create consonant cluster C1 and  C2 columns
data['Onset Cluster C1'] = onset_cluster_data.groupby(level=0)[0].apply(lambda x: ' '.join(x))
data['Onset Cluster C2'] = onset_cluster_data.groupby(level=0)[1].apply(lambda x: ' '.join(x))

# group by first level of multi-index to create onset cluster column
data['Onset Cluster'] = onset_cluster_data.groupby(level=0)['all'].apply(lambda x: ' '.join(x))

# Create cluster dataframe
cluster_data = data['Target Syllables'].str.extractall(r'(?:(.):[OC])?(?:(.):[OC])(?:(.):[OC])(?:(.):[OC])?')
cluster_data['all'] = cluster_data[0].fillna('') + cluster_data[1] + cluster_data[2] + cluster_data[3].fillna('')
data['Clusters'] = cluster_data.groupby(level=0)['all'].apply(lambda x: ' '.join(x))

### Word Position
##
#

#Create_WI onset singleton dataframe and add to data
data['WI Onset Singleton'] = data['Target Syllables'].str.extract(r'^ˈ?(.):O.:[^O]')

#Create_WI onset cluster dataframe and add to data
WI_cluster_data = data['Target Syllables'].str.extractall(r'^ˈ?(.):O(.):O')
WI_cluster_data['all'] = WI_cluster_data[0]+WI_cluster_data[1]

# group by first level of multi-index to create WI onset cluster column
data['WI Onset Cluster'] = WI_cluster_data.groupby(level=0)['all'].apply(lambda x: ' '.join(x))

#Create WF Coda singleton dataframe and add to data
data['WF Coda Singleton'] = data['Target Syllables'].str.extract(r'(.):C$')

### Stressed Syllable
##
#

# Extract stressed syllable, Works but needs to remove tags
stressed_syl_data = data['Target Syllables'].str.extractall(r'ˈ((?:.:O){0,3}(?:.:(?:N|D))(?:.:D)?(?:.:C)?)')
data['Stressed Syllable'] = stressed_syl_data.groupby(level=0)[0].apply(lambda x: ' '.join(x))

###### REMOVE THIS LINE IF DO NOT WANT TO INCLUDE MONOSYLLABLE AS STRESSED
# Create Monosyllable column
data['Monosyllable'] = data['Target Syllables'].apply(lambda x: x if 'ˈ' not in x else np.nan)

# Stress_or_monosyllable
data['Stressed Syllable'] = data['Stressed Syllable'].combine_first(data['Monosyllable'])

# Create stressed onset column
stress_onset_data = data['Stressed Syllable'].str.extractall(r'(.):O(?:(.):O)?')
stress_onset_data['all'] = stress_onset_data[0].fillna('') + stress_onset_data[1].fillna('')
data['Stressed Onset'] = stress_onset_data.groupby(level=0)['all'].apply(lambda x: ' '.join(x))

# Stressed nucleus
stress_nucleus_data = data['Stressed Syllable'].str.extractall(r'(?:(.):[ND])?(.):[ND](?:(.):[ND])?')
stress_nucleus_data['all'] = stress_nucleus_data[0].fillna('') + stress_nucleus_data[1].fillna('')
data['Stressed Nucleus'] = stress_nucleus_data.groupby(level=0)['all'].apply(lambda x: ' '.join(x))

# Stressed coda
data['Stressed Coda'] = data['Stressed Syllable'].str.extract(r'(.):[C]')

### Might be used if multiple codas per line
"""
stress_coda_data = data['Stressed Syllable'].str.extractall(r'(.):[C]')
stress_coda_data['all'] = stress_coda_data[0].fillna('') + stress_coda_data[1].fillna('') # Only if coda clusters (not in Spanish)
data['Stressed Coda'] = stress_coda_data.groupby(level=0)['all'].apply(lambda x: ' '.join(x))
"""

###
##
#

# Extract unstressed syllable, Works but needs to remove tags
data['Unstressed Syllables'] = data['Target Syllables'].str.replace(r'ˈ((?:.:O){0,3}(?:.:(?:N|D))(?:.:D)?(?:.:C)?)', r' ')

# UnStressed onset
unstress_onset_data = data['Unstressed Syllables'].str.extractall(r'(.):O(?:(.):O)?')
unstress_onset_data['all'] = unstress_onset_data[0].fillna('') + unstress_onset_data[1].fillna('')
data['Unstressed Onsets'] = unstress_onset_data.groupby(level=0)['all'].apply(lambda x: ' '.join(x))




# UnStressed nucleus
unstress_nucleus_data = data['Unstressed Syllables'].str.extractall(r'(?:(.):[ND])?(.):[ND](?:(.):[ND])?')
unstress_nucleus_data['all'] = unstress_nucleus_data[0].fillna('') + unstress_nucleus_data[1].fillna('')
data['Unstressed Nucleus'] = unstress_nucleus_data.groupby(level=0)['all'].apply(lambda x: ' '.join(x))

# Stressed coda
unstress_coda_data = data['Unstressed Syllables'].str.extractall(r'(.):[C]')
data['Unstressed Codas'] = unstress_coda_data.groupby(level=0)[0].apply(lambda x: ' '.join(x))

# Create multiple words column
data['Multiple Words'] = data['Orthography'].apply(lambda x: 'Yes' if ' ' in x else np.nan)

## To do
# Singleton Onset (Phonetically controlled)
# Monosyllable, Stressed bisyllable, non-homorganic??

### Counts
## Stressed Onsets
s_onset = stress_onset_data['all'].str.split(' ').apply(pd.Series, 1).stack()
s_onset.index = s_onset.index.droplevel(-1) # to line up with df's index
s_onset.name = 'Stressed Onsets' # needs a name to join
s_onset_counts = s_onset.value_counts()

## Stressed Nucleus
s_nucleus = stress_nucleus_data['all'].str.split(' ').apply(pd.Series, 1).stack()
s_nucleus.index = s_nucleus.index.droplevel(-1) # to line up with df's index
s_nucleus.name = 'Stressed Nucleus' # needs a name to join
s_nucleus_counts = s_nucleus.value_counts()

## Stressed Coda
s_coda = data['Stressed Coda'].str.split(' ').apply(pd.Series, 1).stack()
s_coda.index = s_coda.index.droplevel(-1) # to line up with df's index
s_coda.name = 'Stressed Coda' # needs a name to join
s_coda_counts = s_coda.value_counts()

### Export
##
#

#Export to CSV
data.to_csv(os.path.join(out_path, 'Word_Analysis.csv'), encoding = 'utf-8')
s_onset_counts.to_csv(os.path.join(out_path, 'Stressed_Onset_Counts.csv'), encoding = 'utf-8')
s_nucleus_counts.to_csv(os.path.join(out_path, 'Stressed_Nucleus_Counts.csv'), encoding = 'utf-8')
s_coda_counts.to_csv(os.path.join(out_path, 'Stressed_Coda_Counts.csv'), encoding = 'utf-8')