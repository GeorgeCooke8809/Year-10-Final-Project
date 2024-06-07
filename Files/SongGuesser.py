#Imports
import sqlite3
from tkinter import *
import random
import pygame
pygame.init()

#Fonts:
#Cambria
#Century

signed_in = False
username = "Guest"
total_points = 0
top_session_points = 0

users = sqlite3.connect("Users.db")
user_cursor = users.cursor()

def login_attempt():
    global signed_in, username, total_points, top_session_points, password
    username = username_enter.get()
    password = password_enter.get()
    
    # DEBUG -- print(password)
    if username != "":
        user_cursor.execute("SELECT Password FROM Users WHERE Username = ?", (username,))
        correct_password = user_cursor.fetchone()
        # DEBUG -- print(correct_password)
        if correct_password != None:
            correct_password = correct_password[0]
    
    # DEBUG -- print(correct_password)
    
        if str(password) == str(correct_password):
            user_cursor.execute("SELECT AllTimeScore FROM Users WHERE Username = ?", (username,))
            total_points = user_cursor.fetchone()[0]

            user_cursor.execute("SELECT TopSessionScore FROM Users WHERE Username = ?", (username,))
            top_session_points = user_cursor.fetchone()[0]

            signed_in = True
            login.destroy()
            # DEBUG -- print("Correct")
        
        else:
            fail_text = Label(login_f, text = "Your username or password are not correct.\nPlease try again.", font = ("Century", 10, "italic"), anchor = "center", padx = 10, wrap=True, wraplength=505, justify = "center")
            fail_text.config(fg = "red")
            fail_text.grid(row = 5, column = 0, sticky = W+E+N+S,pady = "10")

            login_f.pack()
            #DEBUG -- print("Incorrect")
    
        
def create_account():
    global username, password
    
    username = username_enter.get()
    password = password_enter.get()
    
    user_cursor.execute("SELECT Password FROM Users WHERE Username = ?", (username,))
    correct_password = user_cursor.fetchone()
    
    print(correct_password)
    
    if correct_password == None:
        
        if password != "":
            user_cursor.execute("INSERT INTO Users VALUES (?, ?, ?, ?)", (username, password, "0", "0"))
    
            users.commit()
            
            signed_in = True
        
            login.destroy()
            
        else:
            fail_text = Label(login_f, text = "Please enter a password.\n", font = ("Century", 10, "italic"), anchor = "center", padx = 10, wrap=True, wraplength=505, justify = "center")
            fail_text.config(fg = "red")
            fail_text.grid(row = 5, column = 0, sticky = W+E+N+S,pady = "10")

            login_f.pack()
            
    else:
        fail_text = Label(login_f, text = "That username already exists.\nPlease try again.", font = ("Century", 10, "italic"), anchor = "center", padx = 10, wrap=True, wraplength=505, justify = "center")
        fail_text.config(fg = "red")
        fail_text.grid(row = 5, column = 0, sticky = W+E+N+S,pady = "10")

        login_f.pack()

#Make Login Window
login = Tk()
login.geometry("300x480")
login.title("Login")

#Make login frame / table
login_f = Frame(login)
login_f.rowconfigure(0, weight = 1)
login_f.rowconfigure(2, weight = 1)
login_f.rowconfigure(3, weight = 1)
login_f.rowconfigure(4, weight = 1)
login_f.rowconfigure(5, weight = 1)
login_f.rowconfigure(6, weight = 1)
login_f.rowconfigure(7, weight = 1)

#enter data to login table
login_text = Label(login_f, text = "Sign In", font = ("Cambria", 35, "bold"), anchor = "center", padx = 10, wrap=True, wraplength=505, justify = "center")
login_text.grid(row = 0, column = 0, sticky = W+E+N+S,pady = "10")
username_text = Label(login_f, text = "Username:", font = ("Century", 15), anchor = "center", padx = 10, wrap=True, wraplength=505, justify = "center")
username_text.grid(row = 1, column = 0, sticky = W+E+N+S, pady = "10")
username_enter = Entry(login_f, font = ("Century", 15))
username_enter.grid(row = 2, column = 0, sticky = W+E+N+S)
password_text = Label(login_f, text = "Password:", font = ("Century", 15), anchor = "center", padx = 10, wrap=True, wraplength=505, justify = "center")
password_text.grid(row = 3, column = 0, sticky = W+E+N+S, pady = "10")
password_enter = Entry(login_f, font = ("Century", 15))
password_enter.grid(row = 4, column = 0, sticky = W+E+N+S)
fail_text = Label(login_f, text = "\n", font = ("Century", 10, "italic"), anchor = "center", padx = 10, wrap=True, wraplength=505, justify = "center")
fail_text.config(fg = "red")
fail_text.grid(row = 5, column = 0, sticky = W+E+N+S,pady = "10")
login_submit = Button(login_f, text = "Sign In", command = login_attempt, font = ("Century", 17), pady = "10")
login_submit.grid(row = 6, column = 0, sticky = W+E+N+S)
new_account = Button(login_f, text = "Create Account", command = create_account, font = ("Century", 17), pady = "10")
new_account.grid(row = 7, column = 0, sticky = W+E+N+S, pady = "10")

login_f.pack()
login.mainloop()




correct = pygame.mixer.Sound('Correct.mp3')

def pick_song():
    global username, total_points
    
    cursor.execute("SELECT COUNT(*) FROM Songs")
    item_count = int(cursor.fetchone()[0]) 
    song_choice = random.randint(1,item_count)

# DEBUG -- print(song_choice)
    
    cursor.execute("SELECT Title FROM Songs WHERE rowid =:c", {"c": song_choice})
    song = cursor.fetchone()[0]

# DEBUG -- print(song)
    
    cursor.execute("SELECT Artist FROM Songs WHERE rowid =:c", {"c": song_choice})
    artist = cursor.fetchone()[0]
    
    #assemble string with only first letters
    words = song.split()
    # DEBUG -- print(words)
    string = ""
    for word in words:
        letter = word[0]
        letters = len(word)
        # DEBUG -- print(letters)
        for x in range(1,letters):
            letter = letter + " _"
        string = string + letter + "  "
        # DEBUG -- print(string)

# DEBUG -- print(artist)

    #print(string)
    #print(artist)  

    user = Label(top_table, text = username, font = ("Cambria", 15, "italic"), anchor = "w", padx = 10, wrap=True, wraplength=505, justify = "left")
    user.grid(row = 0, column = 0, sticky = W+E+N+S)
    
    total = Label(top_table, text = total_points, font = ("Cambria", 15, "italic"), anchor = "e", padx = 10, wrap=True, wraplength=505, justify = "right")
    total.grid(row = 0, column = 1, sticky = W+E+N+S)
    
    row_points = Label(top_table, text = points, font = ("Cambria", 15, "italic"), anchor = "e", padx = 10, wrap=True, wraplength=505, justify = "right")
    row_points.grid(row = 0, column = 2, sticky = W+E+N+S)

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
top_table.columnconfigure(2, weight = 1)

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
        global username, password, total_points, top_session_points, signed_in      

        global points, guess, song, total_points
        
        guess = guess + 1
        
        if guess <= 3:

            choice = box.get()
        
        
            if choice.upper() == song.upper():
                #print("That Is Correct! Well Done!")
                correct.play()
                points = points + (4-guess)
                total_points = total_points + (4-guess)
                
                if signed_in == True:
                    user_cursor.execute("DELETE FROM Users WHERE Username = ?", (username, ))
                    
                    if points > top_session_points:
                        top_session_points = points
                
                    user_cursor.execute("INSERT INTO Users VALUES (?, ?, ?, ?)", (username, password, total_points, top_session_points))
    
                    users.commit()

                #print("Session Points: " + str(points))
                song = pick_song()
                guess = 0
            
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
