from tkinter import *
import pygame
from tkinter import filedialog
import time
from mutagen.mp3 import MP3
import tkinter.ttk as ttk

window = Tk()
window.title("Music Player")
window.tk.call("wm", "iconphoto", window._w, PhotoImage(file="Images/music_note.ico"))
window.geometry("500x400")

# Pygame mixer
pygame.mixer.init()


# Grab Song Length Time Info
def play_time():
    # Grab current song elapsed time
    current_time = pygame.mixer.music.get_pos() / 1000

    # Temp label to get data
    slider_label.config(text=f"Slider: {int(my_slider.get())} and Song Pos: {int(current_time)}")

    # convert to time format
    converted_current_time = time.strftime("%M:%S", time.gmtime(current_time))

    # Get Currently Playing Song
    # next_one = music_box.curselection()
    # Grab song title from playlist
    song = music_box.get(ACTIVE)
    # Add directory structure and mp3 to song title
    song = f"/home/gentle/Music/{song}.mp3"
    # Get Song Length with Mutagen
    song_mut = MP3(song)
    # Get song length
    global song_length
    song_length = song_mut.info.length
    # Covert to time format
    converted_song_length = time.strftime("%M:%S", time.gmtime(song_length))

    # Increase current time by one second
    current_time += 1

    if int(my_slider.get()) == int(song_length):
        status_bar.config(text=f"Time Elapsed: {converted_song_length} ")

    elif int(my_slider.get()) == int(current_time):
        # Slider hasn't been moved
        # Update slider to Position
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=int(current_time))
    else:
        # Slider has been moved
        # Update slider to Position
        slider_position = int(song_length)
        my_slider.config(to=slider_position, value=int(my_slider.get()))
        converted_current_time = time.strftime("%M:%S", time.gmtime(int(my_slider.get())))

        status_bar.config(text=f"Time Elapsed: {converted_current_time}  of  {converted_song_length} ")

        # Move slider by one second
        next_time = int(my_slider.get()) + 1
        my_slider.config(value=next_time)

    # Output time to status bar
    # status_bar.config(text=f"Time Elapsed: {converted_current_time}  of  {converted_song_length}: ")
    # Update slider position value to current song position..
    # my_slider.config(value=int(current_time))

    # Update time
    status_bar.after(1000, play_time)


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

    # Call the play time function to get song length
    play_time()

    # # Update slider to Position
    # slider_position = int(song_length)
    # my_slider.config(to=slider_position, value=0)


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

    # Clear the status bar
    status_bar.config(text="")


# Play next song in the playlist
def next_song():
    # Get current song tuple number
    next_one = music_box.curselection()
    # Add one to the current song number
    next_one = next_one[0]+1
    # Grab song title from playlist
    song = music_box.get(next_one)
    # Add directory structure and mp3 to song title
    song = f"/home/gentle/Music/{song}.mp3"
    # Load and play song
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    # Clear active bar in playlist listbox
    music_box.selection_clear(0, END)
    # Activate new song bar
    music_box.activate(next_one)
    # Set Active Bar to next song
    music_box.selection_set(next_one, last=None)


# Play Previous song in playlist
def previous_song():
    # Get current song tuple number
    prev_one = music_box.curselection()
    # Add one to the current song number
    prev_one = prev_one[0] - 1
    # Grab song title from playlist
    song = music_box.get(prev_one)
    # Add directory structure and mp3 to song title
    song = f"/home/gentle/Music/{song}.mp3"
    # Load and play song
    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0)
    # Clear active bar in playlist listbox
    music_box.selection_clear(0, END)
    # Activate new song bar
    music_box.activate(prev_one)
    # Set Active Bar to next song
    music_box.selection_set(prev_one, last=None)


# Delete A Song From Playlist
def delete_song():
    # Delete currently selected songs
    music_box.delete(ANCHOR)
    # Stop Music if it's Playing
    pygame.mixer.music.stop()


# Delete All Songs From Playlist
def delete_all_songs():
    # Delete all songs
    music_box.delete(0, END)
    # Stop Music if it's Playing
    pygame.mixer.music.stop()


# Create slider function
def slide(x):
    # slider_label.config(text=f"{int(my_slider.get())} of {int(song_length)}")
    song = music_box.get(ACTIVE)
    song = f"/home/gentle/Music/{song}.mp3"

    pygame.mixer.music.load(song)
    pygame.mixer.music.play(loops=0, start=int(my_slider.get()))


# Playlist box
music_box = Listbox(bg="black", fg="green", width=65)
music_box.pack(pady=15)
scroll = Scrollbar(orient=VERTICAL, command=music_box.yview)
music_box.configure(yscrollcommand=scroll.set)
scroll.place(x=482, y=19, height=152)

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
back_button = Button(control_frame, image=back_btn_img, borderwidth=0, padx=9, command=previous_song)
forward_button = Button(control_frame, image=forward_btn_img, borderwidth=0, padx=9, command=next_song)
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

# Create Delete Song Menu
remove_song_menu = Menu(my_menu)
my_menu.add_cascade(label="Remove Songs", menu=remove_song_menu)
remove_song_menu.add_command(label="Remove Song from Playlist", command=delete_song)
remove_song_menu.add_command(label="Remove All Songs from Playlist", command=delete_all_songs)

# Create Status Bar
status_bar = Label(text="", bd=1, relief=GROOVE, anchor=E)
status_bar.pack(fill=X, side=BOTTOM, ipady=2)

# Create music position slider
my_slider = ttk.Scale(from_=0, to=100, orient=HORIZONTAL, value=0, command=slide, length=360)
my_slider.pack(pady=25)

# Temporary slider label
slider_label = Label(text="0")
slider_label.pack(pady=10)

window.mainloop()
