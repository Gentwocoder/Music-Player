from tkinter import *
import pygame
from tkinter import filedialog

window = Tk()
window.title("Music Player")
# window.iconbitmap('/home/gentle/Music_Player/music_note.ico')
window.geometry("500x400")

# Pygame mixer
pygame.mixer.init()


# Add Song Function
def add_song():
    song = filedialog.askopenfilename(initialdir="/home/gentle/Music/", title="Choose a song", filetypes=(("mp3 Files", "*.mp3"),))

    # Strip out directory and .mp3 extension the song
    song = song.replace("/home/gentle/Music/", "")
    song = song.replace(".mp3", "")

    # Add song to listbox
    music_box.insert(END, song)


# Add many songs
def add_many_songs():
    songs = filedialog.askopenfilenames(initialdir="/home/gentle/Music/", title="Choose a song", filetypes=(("mp3 Files", "*.mp3"),))

    # Loop tru song list and replace directory info and mp3
    for song in songs:
        song = song.replace("/home/gentle/Music/", "")
        song = song.replace(".mp3", "")
        # Insert to Playlist
        music_box.insert(END, song)


# Play Selected Song
def play():
    song = music_box.get(ACTIVE)
    song = f"/home/gentle/Music/{song}.mp3"

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)


# Global Pause Variable
# global paused
paused = False


# Pause Selected Song
def pause(is_paused):
    global paused
    paused = is_paused

    if paused:
        # Unpause
        pygame.mixer.music.unpause()
        paused = False
    else:
        # Pause
        pygame.mixer.music.pause()
        paused = True


# Stop Playing Current Song
def stop():
    pygame.mixer.music.stop()
    music_box.selection_clear(ACTIVE)


# Playlist box
music_box = Listbox(bg="black", fg="green", width=65)
music_box.pack(pady=15)

# Player Controls images
back_btn_img = PhotoImage(file="Images/skip_previous.png")
forward_btn_img = PhotoImage(file="Images/skip_next.png")
play_btn_img = PhotoImage(file="Images/play.png")
pause_btn_img = PhotoImage(file="Images/pause.png")
stop_btn_img = PhotoImage(file="Images/stop.png")

# Player control frame
control_frame = Frame()
control_frame.pack(pady=10)

# Player control buttons
back_button = Button(control_frame, image=back_btn_img, borderwidth=0, padx=9)
forward_button = Button(control_frame, image=forward_btn_img, borderwidth=0, padx=9)
play_button = Button(control_frame, image=play_btn_img, borderwidth=0, padx=9, command=play)
pause_button = Button(control_frame, image=pause_btn_img, borderwidth=0, padx=9, command=lambda: pause(paused))
stop_button = Button(control_frame, image=stop_btn_img, borderwidth=0, padx=9, command=stop)

back_button.grid(row=0, column=0)
forward_button.grid(row=0, column=1)
play_button.grid(row=0, column=2)
pause_button.grid(row=0, column=3)
stop_button.grid(row=0, column=4)

# Create menu
my_menu = Menu()
window.config(menu=my_menu)

# Add Song Menu
add_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Add Songs", menu=add_song_menu)
add_song_menu.add_command(label="Add One Song to Playlist", command=add_song)
# Add many songs
add_song_menu.add_command(label="Add Many Song to Playlist", command=add_many_songs)

window.mainloop()
