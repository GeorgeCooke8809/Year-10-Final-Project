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
            

    path = "Songs/" + str(song_choice) + "/Aud.mp3"
    song_play = pygame.mixer.Sound(path)
    song_play.play()
    return(song)

#Playing check
playing = True

points = 0

def play():
    top_table.pack(fill = "x", expand = True, pady = 10,  anchor="w")
    frame.pack()
    all_time_table.pack_forget()
    session_table.pack_forget()
    session_label_table.pack_forget()
    all_time_label_table.pack_forget()

def all_time_lead():
    user_cursor.execute("SELECT Username FROM Users ORDER BY AllTimeScore DESC LIMIT 5")
    top_5_all_name = user_cursor.fetchall()
    user_cursor.execute("SELECT AllTimeScore FROM Users ORDER BY AllTimeScore DESC LIMIT 5")
    top_5_all_score = user_cursor.fetchall()    

    number_one = Label(all_time_table, text = "1st", font = ("Cambria", 15, "bold"), anchor = "w", padx = 10, wrap=True, wraplength=505, justify = "left")
    number_one.grid(row = 0, column = 0, sticky = W+E+N+S)
    name_one = Label(all_time_table, text = top_5_all_name[0], font = ("Cambria", 15, "bold"), anchor = "center", padx = 10, wrap=True, wraplength=505, justify = "center")
    name_one.grid(row = 0, column = 1, sticky = W+E+N+S)
    score_one = Label(all_time_table, text = top_5_all_score[0], font = ("Cambria", 15, "bold"), anchor = "e", padx = 10, wrap=True, wraplength=505, justify = "right")
    score_one.grid(row = 0, column = 2, sticky = W+E+N+S)

    number_two = Label(all_time_table, text = "2nd", font = ("Cambria", 15, "bold"), anchor = "w", padx = 10, wrap=True, wraplength=505, justify = "left")
    number_two.grid(row = 1, column = 0, sticky = W+E+N+S)
    name_two = Label(all_time_table, text = top_5_all_name[1], font = ("Cambria", 15, "bold"), anchor = "center", padx = 10, wrap=True, wraplength=505, justify = "center")
    name_two.grid(row = 1, column = 1, sticky = W+E+N+S)
    score_two = Label(all_time_table, text = top_5_all_score[1], font = ("Cambria", 15, "bold"), anchor = "e", padx = 10, wrap=True, wraplength=505, justify = "right")
    score_two.grid(row = 1, column = 2, sticky = W+E+N+S)

    number_three = Label(all_time_table, text = "3rd", font = ("Cambria", 15, "bold"), anchor = "w", padx = 10, wrap=True, wraplength=505, justify = "left")
    number_three.grid(row = 2, column = 0, sticky = W+E+N+S)
    name_three = Label(all_time_table, text = top_5_all_name[2], font = ("Cambria", 15, "bold"), anchor = "center", padx = 10, wrap=True, wraplength=505, justify = "center")
    name_three.grid(row = 2, column = 1, sticky = W+E+N+S)
    score_three = Label(all_time_table, text = top_5_all_score[2], font = ("Cambria", 15, "bold"), anchor = "e", padx = 10, wrap=True, wraplength=505, justify = "right")
    score_three.grid(row = 2, column = 2, sticky = W+E+N+S)

    number_four = Label(all_time_table, text = "4th", font = ("Cambria", 15), anchor = "w", padx = 10, wrap=True, wraplength=505, justify = "left")
    number_four.grid(row = 3, column = 0, sticky = W+E+N+S)
    name_four = Label(all_time_table, text = top_5_all_name[3], font = ("Cambria", 15), anchor = "center", padx = 10, wrap=True, wraplength=505, justify = "center")
    name_four.grid(row = 3, column = 1, sticky = W+E+N+S)
    score_four = Label(all_time_table, text = top_5_all_score[3], font = ("Cambria", 15), anchor = "e", padx = 10, wrap=True, wraplength=505, justify = "right")
    score_four.grid(row = 3, column = 2, sticky = W+E+N+S)

    number_five = Label(all_time_table, text = "5th", font = ("Cambria", 15), anchor = "w", padx = 10, wrap=True, wraplength=505, justify = "left")
    number_five.grid(row = 4, column = 0, sticky = W+E+N+S)
    name_five = Label(all_time_table, text = top_5_all_name[4], font = ("Cambria", 15), anchor = "center", padx = 10, wrap=True, wraplength=505, justify = "center")
    name_five.grid(row = 4, column = 1, sticky = W+E+N+S)
    score_five = Label(all_time_table, text = top_5_all_score[4], font = ("Cambria", 15), anchor = "e", padx = 10, wrap=True, wraplength=505, justify = "right")
    score_five.grid(row = 4, column = 2, sticky = W+E+N+S)    

    all_time_label_table.pack()
    all_time_table.pack(fill = "x", expand = True, pady = 10,  anchor="nw")
    session_table.pack_forget()
    frame.pack_forget()
    top_table.pack_forget()
    session_label_table.pack_forget()

def session_lead():
    user_cursor.execute("SELECT Username FROM Users ORDER BY TopSessionScore DESC LIMIT 5")
    top_5_session_names = user_cursor.fetchall()
    user_cursor.execute("SELECT TopSessionScore FROM Users ORDER BY TopSessionScore DESC LIMIT 5")
    top_5_session_score = user_cursor.fetchall()


    number_one = Label(session_table, text = "1st", font = ("Cambria", 15, "bold"), anchor = "w", padx = 10, wrap=True, wraplength=505, justify = "left")
    number_one.grid(row = 0, column = 0, sticky = W+E+N+S)
    name_one = Label(session_table, text = top_5_session_names[0], font = ("Cambria", 15, "bold"), anchor = "center", padx = 10, wrap=True, wraplength=505, justify = "center")
    name_one.grid(row = 0, column = 1, sticky = W+E+N+S)
    score_one = Label(session_table, text = top_5_session_score[0], font = ("Cambria", 15, "bold"), anchor = "e", padx = 10, wrap=True, wraplength=505, justify = "right")
    score_one.grid(row = 0, column = 2, sticky = W+E+N+S)

    number_two = Label(session_table, text = "2nd", font = ("Cambria", 15, "bold"), anchor = "w", padx = 10, wrap=True, wraplength=505, justify = "left")
    number_two.grid(row = 1, column = 0, sticky = W+E+N+S)
    name_two = Label(session_table, text = top_5_session_names[1], font = ("Cambria", 15, "bold"), anchor = "center", padx = 10, wrap=True, wraplength=505, justify = "center")
    name_two.grid(row = 1, column = 1, sticky = W+E+N+S)
    score_two = Label(session_table, text = top_5_session_score[1], font = ("Cambria", 15, "bold"), anchor = "e", padx = 10, wrap=True, wraplength=505, justify = "right")
    score_two.grid(row = 1, column = 2, sticky = W+E+N+S)

    number_three = Label(session_table, text = "3rd", font = ("Cambria", 15, "bold"), anchor = "w", padx = 10, wrap=True, wraplength=505, justify = "left")
    number_three.grid(row = 2, column = 0, sticky = W+E+N+S)
    name_three = Label(session_table, text = top_5_session_names[2], font = ("Cambria", 15, "bold"), anchor = "center", padx = 10, wrap=True, wraplength=505, justify = "center")
    name_three.grid(row = 2, column = 1, sticky = W+E+N+S)
    score_three = Label(session_table, text = top_5_session_score[2], font = ("Cambria", 15, "bold"), anchor = "e", padx = 10, wrap=True, wraplength=505, justify = "right")
    score_three.grid(row = 2, column = 2, sticky = W+E+N+S)

    number_four = Label(session_table, text = "4th", font = ("Cambria", 15), anchor = "w", padx = 10, wrap=True, wraplength=505, justify = "left")
    number_four.grid(row = 3, column = 0, sticky = W+E+N+S)
    name_four = Label(session_table, text = top_5_session_score[3], font = ("Cambria", 15), anchor = "center", padx = 10, wrap=True, wraplength=505, justify = "center")
    name_four.grid(row = 3, column = 1, sticky = W+E+N+S)
    score_four = Label(session_table, text = top_5_all_score[3], font = ("Cambria", 15), anchor = "e", padx = 10, wrap=True, wraplength=505, justify = "right")
    score_four.grid(row = 3, column = 2, sticky = W+E+N+S)

    number_five = Label(session_table, text = "5th", font = ("Cambria", 15), anchor = "w", padx = 10, wrap=True, wraplength=505, justify = "left")
    number_five.grid(row = 4, column = 0, sticky = W+E+N+S)
    name_five = Label(session_table, text = top_5_all_name[4], font = ("Cambria", 15), anchor = "center", padx = 10, wrap=True, wraplength=505, justify = "center")
    name_five.grid(row = 4, column = 1, sticky = W+E+N+S)
    score_five = Label(session_table, text = top_5_session_score[4], font = ("Cambria", 15), anchor = "e", padx = 10, wrap=True, wraplength=505, justify = "right")
    score_five.grid(row = 4, column = 2, sticky = W+E+N+S)    

    session_label_table.pack()
    session_table.pack(fill = "x", expand = True, pady = 10,  anchor="nw")
    all_time_table.pack_forget()
    frame.pack_forget()
    top_table.pack_forget()
    all_time_label_table.pack_forget()

#Window
root = Tk()
root.geometry("525x210")
root.title("Song Guesser - Version 0.3.0 - 27/05/2024")

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
frame = Frame(root, width = 525, height = 190)
frame.rowconfigure(0, weight = 1)
frame.rowconfigure(1, weight = 1)
frame.rowconfigure(2, weight = 1)
frame.rowconfigure(3, weight = 1)

#Top Table
top_table = Frame(root, width = 525, height = 20)
top_table.rowconfigure(0, weight = 1)
top_table.columnconfigure(0, weight = 5)
top_table.columnconfigure(1, weight = 1)
top_table.columnconfigure(2, weight = 1)



#Top 5 All Time Table
all_time_table = Frame(root, width = 500)
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
session_label = Label(session_label_table, text = "Top 5 Session Scores", font = ("Cambria", 25, "bold"))
session_label.grid(row = 0, column = 0, sticky = W+E+N+S)

all_time_label_table = Frame(root)
all_time_label_table.rowconfigure(0, weight = 1)
all_time_label = Label(all_time_label_table, text = "Top 5 All Time Scores", font = ("Cambria", 25, "bold"))
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


user_cursor.execute("SELECT Username FROM Users ORDER BY AllTimeScore DESC LIMIT 5")
top_5_all_name = user_cursor.fetchall()
user_cursor.execute("SELECT AllTimeScore FROM Users ORDER BY AllTimeScore DESC LIMIT 5")
top_5_all_score = user_cursor.fetchall()


number_one = Label(all_time_table, text = "1st", font = ("Cambria", 15, "bold"), anchor = "w", padx = 10, wrap=True, wraplength=505, justify = "left")
number_one.grid(row = 0, column = 0, sticky = W+E+N+S)
name_one = Label(all_time_table, text = top_5_all_name[0], font = ("Cambria", 15, "bold"), anchor = "center", padx = 10, wrap=True, wraplength=505, justify = "center")
name_one.grid(row = 0, column = 1, sticky = W+E+N+S)
score_one = Label(all_time_table, text = top_5_all_score[0], font = ("Cambria", 15, "bold"), anchor = "e", padx = 10, wrap=True, wraplength=505, justify = "right")
score_one.grid(row = 0, column = 2, sticky = W+E+N+S)

number_two = Label(all_time_table, text = "2nd", font = ("Cambria", 15, "bold"), anchor = "w", padx = 10, wrap=True, wraplength=505, justify = "left")
number_two.grid(row = 1, column = 0, sticky = W+E+N+S)
name_two = Label(all_time_table, text = top_5_all_name[1], font = ("Cambria", 15, "bold"), anchor = "center", padx = 10, wrap=True, wraplength=505, justify = "center")
name_two.grid(row = 1, column = 1, sticky = W+E+N+S)
score_two = Label(all_time_table, text = top_5_all_score[1], font = ("Cambria", 15, "bold"), anchor = "e", padx = 10, wrap=True, wraplength=505, justify = "right")
score_two.grid(row = 1, column = 2, sticky = W+E+N+S)

number_three = Label(all_time_table, text = "3rd", font = ("Cambria", 15, "bold"), anchor = "w", padx = 10, wrap=True, wraplength=505, justify = "left")
number_three.grid(row = 2, column = 0, sticky = W+E+N+S)
name_three = Label(all_time_table, text = top_5_all_name[2], font = ("Cambria", 15, "bold"), anchor = "center", padx = 10, wrap=True, wraplength=505, justify = "center")
name_three.grid(row = 2, column = 1, sticky = W+E+N+S)
score_three = Label(all_time_table, text = top_5_all_score[2], font = ("Cambria", 15, "bold"), anchor = "e", padx = 10, wrap=True, wraplength=505, justify = "right")
score_three.grid(row = 2, column = 2, sticky = W+E+N+S)

number_four = Label(all_time_table, text = "4th", font = ("Cambria", 15), anchor = "w", padx = 10, wrap=True, wraplength=505, justify = "left")
number_four.grid(row = 3, column = 0, sticky = W+E+N+S)
name_four = Label(all_time_table, text = top_5_all_name[3], font = ("Cambria", 15), anchor = "center", padx = 10, wrap=True, wraplength=505, justify = "center")
name_four.grid(row = 3, column = 1, sticky = W+E+N+S)
score_four = Label(all_time_table, text = top_5_all_score[3], font = ("Cambria", 15), anchor = "e", padx = 10, wrap=True, wraplength=505, justify = "right")
score_four.grid(row = 3, column = 2, sticky = W+E+N+S)

number_five = Label(all_time_table, text = "5th", font = ("Cambria", 15), anchor = "w", padx = 10, wrap=True, wraplength=505, justify = "left")
number_five.grid(row = 4, column = 0, sticky = W+E+N+S)
name_five = Label(all_time_table, text = top_5_all_name[4], font = ("Cambria", 15), anchor = "center", padx = 10, wrap=True, wraplength=505, justify = "center")
name_five.grid(row = 4, column = 1, sticky = W+E+N+S)
score_five = Label(all_time_table, text = top_5_all_score[4], font = ("Cambria", 15), anchor = "e", padx = 10, wrap=True, wraplength=505, justify = "right")
score_five.grid(row = 4, column = 2, sticky = W+E+N+S)






user_cursor.execute("SELECT Username FROM Users ORDER BY TopSessionScore DESC LIMIT 5")
top_5_session_names = user_cursor.fetchall()
user_cursor.execute("SELECT TopSessionScore FROM Users ORDER BY TopSessionScore DESC LIMIT 5")
top_5_session_score = user_cursor.fetchall()


number_one = Label(session_table, text = "1st", font = ("Cambria", 15, "bold"), anchor = "w", padx = 10, wrap=True, wraplength=505, justify = "left")
number_one.grid(row = 0, column = 0, sticky = W+E+N+S)
name_one = Label(session_table, text = top_5_session_names[0], font = ("Cambria", 15, "bold"), anchor = "center", padx = 10, wrap=True, wraplength=505, justify = "center")
name_one.grid(row = 0, column = 1, sticky = W+E+N+S)
score_one = Label(session_table, text = top_5_session_score[0], font = ("Cambria", 15, "bold"), anchor = "e", padx = 10, wrap=True, wraplength=505, justify = "right")
score_one.grid(row = 0, column = 2, sticky = W+E+N+S)

number_two = Label(session_table, text = "2nd", font = ("Cambria", 15, "bold"), anchor = "w", padx = 10, wrap=True, wraplength=505, justify = "left")
number_two.grid(row = 1, column = 0, sticky = W+E+N+S)
name_two = Label(session_table, text = top_5_session_names[1], font = ("Cambria", 15, "bold"), anchor = "center", padx = 10, wrap=True, wraplength=505, justify = "center")
name_two.grid(row = 1, column = 1, sticky = W+E+N+S)
score_two = Label(session_table, text = top_5_session_score[1], font = ("Cambria", 15, "bold"), anchor = "e", padx = 10, wrap=True, wraplength=505, justify = "right")
score_two.grid(row = 1, column = 2, sticky = W+E+N+S)

number_three = Label(session_table, text = "3rd", font = ("Cambria", 15, "bold"), anchor = "w", padx = 10, wrap=True, wraplength=505, justify = "left")
number_three.grid(row = 2, column = 0, sticky = W+E+N+S)
name_three = Label(session_table, text = top_5_session_names[2], font = ("Cambria", 15, "bold"), anchor = "center", padx = 10, wrap=True, wraplength=505, justify = "center")
name_three.grid(row = 2, column = 1, sticky = W+E+N+S)
score_three = Label(session_table, text = top_5_session_score[2], font = ("Cambria", 15, "bold"), anchor = "e", padx = 10, wrap=True, wraplength=505, justify = "right")
score_three.grid(row = 2, column = 2, sticky = W+E+N+S)

number_four = Label(session_table, text = "4th", font = ("Cambria", 15), anchor = "w", padx = 10, wrap=True, wraplength=505, justify = "left")
number_four.grid(row = 3, column = 0, sticky = W+E+N+S)
name_four = Label(session_table, text = top_5_session_score[3], font = ("Cambria", 15), anchor = "center", padx = 10, wrap=True, wraplength=505, justify = "center")
name_four.grid(row = 3, column = 1, sticky = W+E+N+S)
score_four = Label(session_table, text = top_5_all_score[3], font = ("Cambria", 15), anchor = "e", padx = 10, wrap=True, wraplength=505, justify = "right")
score_four.grid(row = 3, column = 2, sticky = W+E+N+S)

number_five = Label(session_table, text = "5th", font = ("Cambria", 15), anchor = "w", padx = 10, wrap=True, wraplength=505, justify = "left")
number_five.grid(row = 4, column = 0, sticky = W+E+N+S)
name_five = Label(session_table, text = top_5_all_name[4], font = ("Cambria", 15), anchor = "center", padx = 10, wrap=True, wraplength=505, justify = "center")
name_five.grid(row = 4, column = 1, sticky = W+E+N+S)
score_five = Label(session_table, text = top_5_session_score[4], font = ("Cambria", 15), anchor = "e", padx = 10, wrap=True, wraplength=505, justify = "right")
score_five.grid(row = 4, column = 2, sticky = W+E+N+S)




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
                song_play.stop()
                song = pick_song()
                guess = 0
            else:
                incorrect.play()
                song_play.stop()
                song_play.play()
            
        else:
            guess = 0
            song_play.stop()
            song = pick_song()
            
    song = pick_song()
    
    box = Entry(frame, font = ("Cambria", 22), width = 33, justify = "center")
    box.grid(row = 2, column = 0, sticky = W+E+N+S)
    
    submit_btn = Button(frame, text = "Submit Guess", command = submit, font = ("Cambria", 15), anchor = "center", justify = "center")
    submit_btn.grid(row = 3, column = 0, sticky = W+E+N+S)

    
    frame.pack()
    root.mainloop()

            
    #print(song)
