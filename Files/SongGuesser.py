#Imports
import sqlite3
import tkinter
import random



#Playing check
playing = True

points = 0



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
cursor.execute("SELECT COUNT(*) FROM Songs")
item_count = int(cursor.fetchone()[0])

while playing == True:   
# DEBUG -- print(item_count)

    song_choice = random.randint(1,item_count)

# DEBUG -- print(song_choice)
    
    cursor.execute("SELECT Title FROM Songs WHERE ID =:c", {"c": song_choice})
    song = cursor.fetchone()[0]

# DEBUG -- print(song)
    
    cursor.execute("SELECT Artist FROM Songs WHERE ID =:c", {"c": song_choice})
    artist = cursor.fetchone()[0]

# DEBUG -- print(artist)


    string = ""
    word = 0

    song_letters = song.split(" ")

    for words in song_letters:
    
    # DEBUG -- print(words)
    
        letter = words[0]
        word = word + 1
        string = string + letter + "_____ "

    print(string)
    print(artist)

    correct = False

    for guess in range(1,3):
        if correct == False:
            choice = input("Guess: ")
            if choice.upper() == song.upper():
                print("That Is Correct! Well Done!")
                points = points + (4-guess)
                print("Session Points: " + str(points))
                correct = True
            else:
                print("That's wrong, try again.")
            print()
