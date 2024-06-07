#Imports
import sqlite3
import tkinter
import random



#Playing check
playing = True



#Imports
data = sqlite3.connect("Songs.db")
cursor = data.cursor()

cursor.execute("SELECT Title FROM Songs")
songs = cursor.fetchall()

# DEBUG -- print(songs)

#print()

cursor.execute("SELECT Artist FROM Songs")
artists = cursor.fetchall()

# DEGUG -- print(artist)



#Pick Random song
def pick():
    cursor.execute("SELECT COUNT(*) FROM Songs")
    item_count = int(cursor.fetchone()[0])

    
    # DEBUG -- print(item_count)

    song_choice = random.randint(0,item_count)

    # DEBUG -- print(song_choice)

    song = songs[song_choice]
    #cursor.execute("SELECT Title FROM Songs WHERE ID = song_choice")
    #song = cursor.fetchone()

    # DEBUG --
    print(song)


    
pick()
