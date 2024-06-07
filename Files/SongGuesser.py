#Imports
import sqlite3
from tkinter import *
import random
import pygame
pygame.init()


correct = pygame.mixer.Sound('Correct.mp3')

def pick_song():
    cursor.execute("SELECT COUNT(*) FROM Songs")
    item_count = int(cursor.fetchone()[0]) 
    song_choice = random.randint(1,item_count)

# DEBUG -- print(song_choice)
    
    cursor.execute("SELECT Title FROM Songs WHERE ID =:c", {"c": song_choice})
    song = cursor.fetchone()[0]

# DEBUG -- print(song)
    
    cursor.execute("SELECT Artist FROM Songs WHERE ID =:c", {"c": song_choice})
    artist = cursor.fetchone()[0]
    
    cursor.execute("SELECT Blanks FROM Songs WHERE ID =:c", {"c": song_choice})
    string = cursor.fetchone()[0]

# DEBUG -- print(artist)

    #print(string)
    #print(artist)
    
    row_points = Label(top_table, text = points, font = ("Cambria", 15, "italic"), anchor = "e", padx = 10, wrap=True, wraplength=505, justify = "right")
    row_points.grid(row = 0, column = 1, sticky = W+E+N+S)

    row_1 = Label(frame, text = string, font = ("Cambria", 25, "bold"), anchor = "w", padx = 10, wrap=True, wraplength=505, justify="left")
    row_1.grid(row = 0, column = 0, sticky = W+E+N+S)
    
    row_2 = Label(frame, text = artist, font = ("Century", 15), anchor = "w", padx = 10,wrap=True, wraplength=505, justify="left")
    row_2.grid(row = 1, column = 0, sticky = W+E+N+S)
    

    top_table.pack(fill = "x", expand = True, pady = 10,  anchor="w")
    frame.pack(fill = "x", expand = True, pady = 10,  anchor="w")
    
    root.resizable(width = True, height = True)
            

    
    return(song)

#Playing check
playing = True

points = 0



#Window
root = Tk()
root.geometry("525x220")
root.title("Song Guesser - Version 0.2 - 26/05/2024")



#Frame
frame = Frame(root)
frame.rowconfigure(0, weight = 1)
frame.rowconfigure(1, weight = 1)

#Top Table
top_table = Frame(root)
top_table.rowconfigure(0, weight = 1)
top_table.columnconfigure(0, weight = 5)
top_table.columnconfigure(1, weight = 1)

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


while playing == True:
    
    guess = 0

    def submit():
        global points, guess, song 
        
        guess = guess + 1
        
        if guess <= 3:

            choice = box.get()
        
        
            if choice.upper() == song.upper():
                #print("That Is Correct! Well Done!")
                correct.play()
                points = points + (4-guess)
                #print("Session Points: " + str(points))
                song = pick_song()
                guess = 0
            #else:
                #print("That's wrong, try again.")
            #print()
            
        else:
            guess = 0
            song = pick_song()
            
    song = pick_song()
    
    box = Entry(root, width = 500, font = ("Cambria", 22))
    box.pack()
    
    submit_btn = Button(root, text = "Submit Guess", command = submit, font = ("Cambria", 15), width = "250")
    submit_btn.pack()
    
    root.mainloop()

            
    #print(song)
