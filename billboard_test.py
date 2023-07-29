#!/usr/bin/env python3
# the above line of code is called a shebang, it tells the computer how to run the program

import billboard
import datetime
from datetime import date
import pandas as pd
import csv

#creates a pandas data frame containing a range of dates:
dates_df = pd.date_range(end = datetime.date(2023, 7, 29), periods = 10, freq = '1W').to_pydatetime().tolist()

#initializes a dictionary for the songs:
select_songs = dict()
#iterates through the date dataframe:
for date_x in dates_df:
    #sets the date equal to the first ten characters because after that it includes time which is not the right format for the API date:
    date_x = str(date_x)[:10]
    #pulls a chart from the billboard website: in this case the hot 100 from the dates it is iterating through:
    chart = billboard.ChartData('hot-100', date = date_x)
    #iterates through each song on the chart:
    for song in chart:
        #determines if the song has reached #1:
        if song.peakPos == 1:
            #determines if the song has been on the chart for 52 weeks:
            if song.weeks >= 2:
                #if the song is already in the dictionary:
                if song.title in select_songs:
                    #if the number of weeks in this entry of the song is greater than the value currently stored:
                    if int(select_songs[song.title]['weeks']) > int(song.weeks):
                        #updates weeks value for the song:
                        select_songs[song.title]['weeks'] = song.weeks
                        print("updating weeks on chart for {}".format(song.title))
                #if the song is not already in the dictionary:
                else:
                    #create a dictionary within the song dictionary that has keys for weeks, artist and peak position and assign their values:
                    select_songs[song.title] = {'weeks': song.weeks, 'artist': song.artist, 'peak position': song.peakPos}
                    print("adding {} to dictionary".format(song.title))
#after all the songs for the date range are added, print the dictionary values:
with open('billboard_output.csv', mode='w') as csv_file:
    csv_file = csv.writer(csv_file, delimiter=',', quotechar='"')
    for song_key in select_songs:
        print("Title: {}, \tArtist: {}, \tWeeks: {}".format(song_key, select_songs[song_key]['artist'], select_songs[song_key]['weeks']))
        csv_file.writerow([song_key, select_songs[song_key]['artist'], select_songs[song_key]['weeks']])
