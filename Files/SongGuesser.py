#Imports
import sqlite3
from sys import maxsize
from textwrap import fill
from tkinter import *
import random
import tkinter
from turtle import width
import pygame
from PIL import ImageTk, Image


pygame.init()

#GUI Customisation:
#Fonts:
#Originals: "Cambria" (1), "Century"(2)

#Shortlist
#Monoton
#Lato (2)
#Tw Cen MT (2)

Font_1 = "Monoton"
Font_2 = "Tw Cen MT"

Background = "White"
Contrast = "#01104d"
Contrast_Light = "#bfd2ff"




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
            fail_text = Label(login_f, text = "Your username or password are not correct.\nPlease try again.", font = (Font_2, 10, "italic"), anchor = "center", padx = 10, wrap=True, wraplength=505, justify = "center")
            fail_text.config(fg = "red")
            fail_text.grid(row = 5, column = 0, sticky = W+E+N+S,pady = "10")

            login_f.pack()
            #DEBUG -- print("Incorrect")
    
        
def create_account():
    global username, password, signed_in
    
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
            fail_text = Label(login_f, text = "Please enter a password.\n", font = (Font_2, 10, "italic"), anchor = "center", padx = 10, wrap=True, wraplength=505, justify = "center")
            fail_text.config(fg = "red")
            fail_text.grid(row = 5, column = 0, sticky = W+E+N+S,pady = "10")

            login_f.pack()
            
    else:
        fail_text = Label(login_f, text = "That username already exists.\nPlease try again.", font = (Font_2, 10, "italic"), anchor = "center", padx = 10, wrap=True, wraplength=505, justify = "center")
        fail_text.config(fg = "red")
        fail_text.grid(row = 5, column = 0, sticky = W+E+N+S,pady = "10")

        login_f.pack()

#Make Login Window
login = Tk()
login.geometry("320x525")
#login.resizable(height = False, width = False)
login.title("Login")

#Make login frame / table
login_f = Frame(login)
login_f.rowconfigure(0, weight = 1)
login_f.rowconfigure(2, weight = 1)
login_f.rowconfigure(3, weight = 1)
login_f.rowconfigure(4, weight = 1)
login_f.rowconfigure(5, weight = 150)
login_f.rowconfigure(6, weight = 1)
login_f.rowconfigure(7, weight = 1)
login_f.rowconfigure(8, weight = 500)

#enter data to login table
login_text = Label(login_f, text = "Sign In", font = (Font_1, 35, "bold"), anchor = "center", padx = 10, wrap=True, wraplength=505, justify = "center")
login_text.grid(row = 0, column = 0, sticky = W+E+N+S,pady = "10")
username_text = Label(login_f, text = "Username:", font = (Font_2, 15), anchor = "center", padx = 10, wrap=True, wraplength=505, justify = "center")
username_text.grid(row = 1, column = 0, sticky = W+E+N+S, pady = "10")
username_enter = Entry(login_f, font = (Font_2, 15))
username_enter.grid(row = 2, column = 0, sticky = W+E+N+S)
password_text = Label(login_f, text = "Password:", font = (Font_2, 15), anchor = "center", padx = 10, wrap=True, wraplength=505, justify = "center")
password_text.grid(row = 3, column = 0, sticky = W+E+N+S, pady = "10")
password_enter = Entry(login_f, font = (Font_2, 15))
password_enter.grid(row = 4, column = 0, sticky = W+E+N+S)
fail_text = Label(login_f, text = "\n", font = (Font_2, 10, "italic"), anchor = "center", padx = 10, wrap=True, wraplength=505, justify = "center")
fail_text.config(fg = "red")
fail_text.grid(row = 5, column = 0, sticky = W+E+N+S,pady = "10")


login_submit = Button(login_f,
                      text = "Sign In", 
                      command = login_attempt, 
                      font = (Font_2, 17), 
                      background = Contrast,
                      fg = "White",
                      activebackground = Contrast_Light,
                      pady = "10",
                      border = 0,
                      cursor = "hand2"
                      )
login_submit.grid(row = 6, column = 0, sticky = W+E+N+S)
button_border = tkinter.Frame(login_f,
                              highlightbackground = Contrast,
                              highlightthickness = 5,
                              width = 50,
                              bg = "White",
                              height = 20,
                              )
new_account = Button(button_border, 
                     text = "Create Account", 
                     command = create_account, 
                     font = (Font_2, 17), 
                     pady = "10",
                     bg = "White",
                     fg = Contrast,
                     highlightthickness = 1,
                     highlightbackground = Contrast_Light,
                     border = 0,
                     cursor = "hand2",
                     width = 18,
                     activebackground = Contrast_Light,
                     )
new_account.pack(anchor = "center")
button_border.grid(row = 7, column = 0, sticky = W+E+N+S, pady = "10")

login_f.pack(fill = "y", expand = True)
login.mainloop()




correct = pygame.mixer.Sound('Correct.mp3')
incorrect = pygame.mixer.Sound('Incorrect.mp3')

path = ""

def pick_song():
    global username, total_points, path, song_play
    
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

    user = Label(title, text = username, font = (Font_1, 15, "italic"), anchor = "w", padx = 10,pady = 10, wrap=True, wraplength=505, justify = "left", bg = Background)
    user.grid(row = 0, column = 0, sticky = W+E+N+S)
    
    total = Label(title, text = total_points, font = (Font_1, 15, "italic"), anchor = "e", padx = 10, wrap=True, wraplength=505, justify = "right", bg = Background)
    total.grid(row = 0, column = 1, sticky = W+E+N+S)
    
    row_points = Label(title, text = points, font = (Font_1, 15, "italic"), anchor = "e", padx = 10, wrap=True, wraplength=505, justify = "right", bg = Background)
    row_points.grid(row = 0, column = 2, sticky = W+E+N+S)

    row_1 = Label(title, text = string, font = (Font_1, 25, "bold"), anchor = "w", wrap=True, wraplength=505, justify="left", bg = Background)
    row_1.grid(row = 1, column = 1, columnspan = 2, sticky = W+E+N+S)
    
    row_2 = Label(title, text = (artist + "                              "), font = (Font_2, 15), anchor = "nw",wrap=True, wraplength=505, bg = Background)
    row_2.grid(row = 2, column = 1, columnspan = 2, sticky = N+W)
            

    path = "Songs/" + str(song_choice) + "/Aud.mp3"
    song_play = pygame.mixer.Sound(path)
    song_play.play()
    
    cover_path = "Songs/" + str(song_choice) + "/Cvr.png"
    cover = Image.open(cover_path).resize((100,100))
    image_cover = ImageTk.PhotoImage(cover)
    ins_cover = Label(title, image = image_cover, pady = 10, padx = 10, bg = Background)
    
    ins_cover.image = image_cover

    ins_cover.grid(row = 1, rowspan = 2, column = 0, sticky = "nesw", pady = 10, padx =10)
    title.pack_forget()
    title.pack(fill = "both", expand = True,  anchor="w")
    
    box.delete(0, END)

    return(song)

#Playing check
playing = True

points = 0

def play():
    title.pack(fill = "both", expand = True,  anchor="w")
    all_time_table.pack_forget()
    session_table.pack_forget()
    session_label_table.pack_forget()
    all_time_label_table.pack_forget()
    song_play.play()

def all_time_lead():
    song_play.stop()    

    user_cursor.execute("SELECT Username FROM Users ORDER BY AllTimeScore DESC LIMIT 5")
    top_5_all_name = user_cursor.fetchall()
    user_cursor.execute("SELECT AllTimeScore FROM Users ORDER BY AllTimeScore DESC LIMIT 5")
    top_5_all_score = user_cursor.fetchall()    

    number_one = Label(all_time_table, text = "1st", font = (Font_1, 15, "bold"), anchor = "w", padx = 10, wrap=True, wraplength=505, justify = "left", bg = Background)
    number_one.grid(row = 0, column = 0, sticky = W+E+N+S)
    name_one = Label(all_time_table, text = top_5_all_name[0], font = (Font_1, 15, "bold"), anchor = "center", padx = 10, wrap=True, wraplength=505, justify = "center", bg = Background)
    name_one.grid(row = 0, column = 1, sticky = W+E+N+S)
    score_one = Label(all_time_table, text = top_5_all_score[0], font = (Font_1, 15, "bold"), anchor = "e", padx = 10, wrap=True, wraplength=505, justify = "right", bg = Background)
    score_one.grid(row = 0, column = 2, sticky = W+E+N+S)

    number_two = Label(all_time_table, text = "2nd", font = (Font_1, 15, "bold"), anchor = "w", padx = 10, wrap=True, wraplength=505, justify = "left", bg = Background)
    number_two.grid(row = 1, column = 0, sticky = W+E+N+S)
    name_two = Label(all_time_table, text = top_5_all_name[1], font = (Font_1, 15, "bold"), anchor = "center", padx = 10, wrap=True, wraplength=505, justify = "center", bg = Background)
    name_two.grid(row = 1, column = 1, sticky = W+E+N+S)
    score_two = Label(all_time_table, text = top_5_all_score[1], font = (Font_1, 15, "bold"), anchor = "e", padx = 10, wrap=True, wraplength=505, justify = "right", bg = Background)
    score_two.grid(row = 1, column = 2, sticky = W+E+N+S)

    number_three = Label(all_time_table, text = "3rd", font = (Font_1, 15, "bold"), anchor = "w", padx = 10, wrap=True, wraplength=505, justify = "left", bg = Background)
    number_three.grid(row = 2, column = 0, sticky = W+E+N+S)
    name_three = Label(all_time_table, text = top_5_all_name[2], font = (Font_1, 15, "bold"), anchor = "center", padx = 10, wrap=True, wraplength=505, justify = "center", bg = Background)
    name_three.grid(row = 2, column = 1, sticky = W+E+N+S)
    score_three = Label(all_time_table, text = top_5_all_score[2], font = (Font_1, 15, "bold"), anchor = "e", padx = 10, wrap=True, wraplength=505, justify = "right", bg = Background)
    score_three.grid(row = 2, column = 2, sticky = W+E+N+S)

    number_four = Label(all_time_table, text = "4th", font = (Font_1, 15), anchor = "w", padx = 10, wrap=True, wraplength=505, justify = "left", bg = Background)
    number_four.grid(row = 3, column = 0, sticky = W+E+N+S)
    name_four = Label(all_time_table, text = top_5_all_name[3], font = (Font_1, 15), anchor = "center", padx = 10, wrap=True, wraplength=505, justify = "center", bg = Background)
    name_four.grid(row = 3, column = 1, sticky = W+E+N+S)
    score_four = Label(all_time_table, text = top_5_all_score[3], font = (Font_1, 15), anchor = "e", padx = 10, wrap=True, wraplength=505, justify = "right", bg = Background)
    score_four.grid(row = 3, column = 2, sticky = W+E+N+S)

    number_five = Label(all_time_table, text = "5th", font = (Font_1, 15), anchor = "w", padx = 10, wrap=True, wraplength=505, justify = "left", bg = Background)
    number_five.grid(row = 4, column = 0, sticky = W+E+N+S)
    name_five = Label(all_time_table, text = top_5_all_name[4], font = (Font_1, 15), anchor = "center", padx = 10, wrap=True, wraplength=505, justify = "center", bg = Background)
    name_five.grid(row = 4, column = 1, sticky = W+E+N+S)
    score_five = Label(all_time_table, text = top_5_all_score[4], font = (Font_1, 15), anchor = "e", padx = 10, wrap=True, wraplength=505, justify = "right", bg = Background)
    score_five.grid(row = 4, column = 2, sticky = W+E+N+S)    

    all_time_label_table.pack()
    all_time_table.pack(fill = "x", expand = True, pady = 10,  anchor="nw")
    session_table.pack_forget()
    title.pack_forget()
    session_label_table.pack_forget()

def session_lead():
    song_play.stop()    

    user_cursor.execute("SELECT Username FROM Users ORDER BY TopSessionScore DESC LIMIT 5")
    top_5_session_names = user_cursor.fetchall()
    user_cursor.execute("SELECT TopSessionScore FROM Users ORDER BY TopSessionScore DESC LIMIT 5")
    top_5_session_score = user_cursor.fetchall()


    number_one = Label(session_table, text = "1st", font = (Font_1, 15, "bold"), anchor = "w", padx = 10, wrap=True, wraplength=505, justify = "left", bg = Background)
    number_one.grid(row = 0, column = 0, sticky = W+E+N+S)
    name_one = Label(session_table, text = top_5_session_names[0], font = (Font_1, 15, "bold"), anchor = "center", padx = 10, wrap=True, wraplength=505, justify = "center", bg = Background)
    name_one.grid(row = 0, column = 1, sticky = W+E+N+S)
    score_one = Label(session_table, text = top_5_session_score[0], font = (Font_1, 15, "bold"), anchor = "e", padx = 10, wrap=True, wraplength=505, justify = "right", bg = Background)
    score_one.grid(row = 0, column = 2, sticky = W+E+N+S)

    number_two = Label(session_table, text = "2nd", font = (Font_1, 15, "bold"), anchor = "w", padx = 10, wrap=True, wraplength=505, justify = "left", bg = Background)
    number_two.grid(row = 1, column = 0, sticky = W+E+N+S)
    name_two = Label(session_table, text = top_5_session_names[1], font = (Font_1, 15, "bold"), anchor = "center", padx = 10, wrap=True, wraplength=505, justify = "center", bg = Background)
    name_two.grid(row = 1, column = 1, sticky = W+E+N+S)
    score_two = Label(session_table, text = top_5_session_score[1], font = (Font_1, 15, "bold"), anchor = "e", padx = 10, wrap=True, wraplength=505, justify = "right", bg = Background)
    score_two.grid(row = 1, column = 2, sticky = W+E+N+S)

    number_three = Label(session_table, text = "3rd", font = (Font_1, 15, "bold"), anchor = "w", padx = 10, wrap=True, wraplength=505, justify = "left", bg = Background)
    number_three.grid(row = 2, column = 0, sticky = W+E+N+S)
    name_three = Label(session_table, text = top_5_session_names[2], font = (Font_1, 15, "bold"), anchor = "center", padx = 10, wrap=True, wraplength=505, justify = "center", bg = Background)
    name_three.grid(row = 2, column = 1, sticky = W+E+N+S)
    score_three = Label(session_table, text = top_5_session_score[2], font = (Font_1, 15, "bold"), anchor = "e", padx = 10, wrap=True, wraplength=505, justify = "right", bg = Background)
    score_three.grid(row = 2, column = 2, sticky = W+E+N+S)

    number_four = Label(session_table, text = "4th", font = (Font_1, 15), anchor = "w", padx = 10, wrap=True, wraplength=505, justify = "left", bg = Background)
    number_four.grid(row = 3, column = 0, sticky = W+E+N+S)
    name_four = Label(session_table, text = top_5_session_score[3], font = (Font_1, 15), anchor = "center", padx = 10, wrap=True, wraplength=505, justify = "center", bg = Background)
    name_four.grid(row = 3, column = 1, sticky = W+E+N+S)
    score_four = Label(session_table, text = top_5_session_score[3], font = (Font_1, 15), anchor = "e", padx = 10, wrap=True, wraplength=505, justify = "right", bg = Background)
    score_four.grid(row = 3, column = 2, sticky = W+E+N+S)

    number_five = Label(session_table, text = "5th", font = (Font_1, 15), anchor = "w", padx = 10, wrap=True, wraplength=505, justify = "left", bg = Background)
    number_five.grid(row = 4, column = 0, sticky = W+E+N+S)
    name_five = Label(session_table, text = top_5_session_names[4], font = (Font_1, 15), anchor = "center", padx = 10, wrap=True, wraplength=505, justify = "center", bg = Background)
    name_five.grid(row = 4, column = 1, sticky = W+E+N+S)
    score_five = Label(session_table, text = top_5_session_score[4], font = (Font_1, 15), anchor = "e", padx = 10, wrap=True, wraplength=505, justify = "right", bg = Background)
    score_five.grid(row = 4, column = 2, sticky = W+E+N+S)    

    session_label_table.pack()
    session_table.pack(fill = "x", expand = True, pady = 10,  anchor="nw")
    all_time_table.pack_forget()
    title.pack_forget()
    all_time_label_table.pack_forget()

#Window
root = Tk()
root.geometry("750x275")
root.config(bg = Background)
root.title("Song Guesser - Version 0.4.1 - 08/06/2024")
root.minsize(width = 750, height = 275)

#Menu
my_menu = Menu(root)
root.config(menu=my_menu)

play_menu = Menu(my_menu)
my_menu.add_command(label = "Play", command = play)

leaderboard_menus = Menu(my_menu)
my_menu.add_cascade(label = "Leaderboards", menu = leaderboard_menus)
leaderboard_menus.add_command(label = "All Time Scores", command = all_time_lead)
leaderboard_menus.add_command(label = "Session Scores", command = session_lead)



#Frame
title = Frame(root, width = 750, height = 270)
title.config(bg = "White")
title.rowconfigure(0, weight = 1)
title.rowconfigure(1, weight = 1)
title.rowconfigure(2, weight = 1)
title.rowconfigure(3, weight = 1)
title.rowconfigure(4, weight = 1)

title.columnconfigure(0, weight = 1)
title.columnconfigure(1, weight = 1000)
title.columnconfigure(2, weight = 200)


#Top 5 All Time Table
all_time_table = Frame(root, width = 750)
all_time_table.rowconfigure(0, weight = 1)
all_time_table.rowconfigure(1, weight = 1)
all_time_table.rowconfigure(2, weight = 1)
all_time_table.rowconfigure(3, weight = 1)
all_time_table.rowconfigure(4, weight = 1)

all_time_table.columnconfigure(0, weight = 1)
all_time_table.columnconfigure(1, weight = 7)
all_time_table.columnconfigure(2, weight = 1)


#Top 5 Session Table
session_table = Frame(root)
session_table.rowconfigure(0, weight = 1)
session_table.rowconfigure(1, weight = 1)
session_table.rowconfigure(2, weight = 1)
session_table.rowconfigure(3, weight = 1)
session_table.rowconfigure(4, weight = 1)

session_table.columnconfigure(0, weight = 1)
session_table.columnconfigure(1, weight = 7)
session_table.columnconfigure(2, weight = 1)

session_label_table = Frame(root)
session_label_table.rowconfigure(0, weight = 1)
session_label = Label(session_label_table, text = "Top 5 Session Scores", font = (Font_1, 25, "bold"), bg = Background)
session_label.grid(row = 0, column = 0, sticky = W+E+N+S)

all_time_label_table = Frame(root)
all_time_label_table.rowconfigure(0, weight = 1)
all_time_label = Label(all_time_label_table, text = "Top 5 All Time Scores", font = (Font_1, 25, "bold"), bg = Background)
all_time_label.grid(row = 0, column = 0, sticky = W+E+N+S)


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

guess = 0

def submit():
    global username, password, total_points, top_session_points, signed_in, points, guess, song, total_points
    
    print(guess)

    guess = guess + 1
      
    choice = box.get()    

    if guess < 3:
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
            song_play.stop()
            song = pick_song()
            guess = 0
        else:
            incorrect.play()
            song_play.stop()
            song_play.play()
    else:
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
            song_play.stop()
            song = pick_song()
            guess = 0
            
        else:
            guess = 0
            incorrect.play()
            song_play.stop()
            song = pick_song()
            song_play.play()
            

while playing == True:
    box = Entry(title, font = (Font_1, 27), width = 33, justify = "center", bg = Contrast_Light, border = 0)
    box.grid(row = 3, columnspan = 3, sticky = W+E+N+S)
    
    submit_btn = Button(title, text = "Submit Guess", command = submit, font = (Font_1, 20, "bold"), anchor = "center", justify = "center", bg = Contrast, fg = "White", border = 0)
    submit_btn.grid(row = 4, columnspan = 3, sticky = W+E+N+S)

    song = pick_song()    

    title.pack()
    root.mainloop()

            
    #print(song)
