from tkinter import *
from tkinter.filedialog import askdirectory
from tkinter.messagebox import showinfo
import pygame as pym
from mutagen.mp3 import MP3
import tkinter.ttk as ttk
import time
import os
pym.init()
pym.mixer.init()
txt_file = os.getcwd()+"\\folder_list.txt"
n = 0
play = False
pause = False
mute = False
vol_ = 1
folder_list=[]

"""Creating folder_list.txt"""
if os.path.exists(txt_file):
    pass
else:
    f = open(txt_file, 'x')
    f.close()


with open(txt_file, 'r') as g:
    for i in g.readlines():
        if i.endswith("\n"):
            i = i[0: len(i) - 1]
            if i not in folder_list:
                folder_list.append(i)


if len(folder_list)==0:
    addf = Tk()
    addf.geometry("400x100")

    # making text
    tx = Label(addf,text="Music folder address: ")
    tx.grid(row=1,column=1)

    # making textarea
    area = Entry(addf,font="callibri 10",width=30)
    area.grid(row=1,column=2)

    #making submit command
    def submit():
        with open(txt_file,"w") as h:
            h.write(area.get()+"\n")
            folder_list.append(area.get())
        addf.destroy()
    
    # making submit button
    sub = Button(addf,text="Enter",command=submit)
    sub.grid(row=2,column=2,ipadx=5)
    addf.mainloop()
folder = folder_list[0]
os.chdir(folder)
songs = []
for item in os.listdir():
    if item.endswith(".mp3"):
        songs.append(item)
music = pym.mixer.music.load(songs[0])
current_song = songs[n]
playsong = pym.mixer.music.load(current_song)
pym.mixer.music.play()
pym.mixer.music.pause()
pym.mixer.music.queue(songs[n+1])

def main():
    global play
    global pause
    global mute
    global vol_

    root = Tk()
    root.geometry("332x160")
    root.minsize(332, 160)
    root.maxsize(332, 160)
    root.title("Music Player by Ritik")



    # All functions
    def openfolder():
        global folder
        folder = askdirectory()
        # print(folder)
        os.chdir(folder)
        songs.clear()
        for item in os.listdir():
            if item.endswith(".mp3"):
                songs.append(item)
        current_song = songs[n]
        name.config(text=current_song)
        pym.mixer.music.load(current_song)
        # print(songs)

        if folder not in folder_list:
            with open(txt_file, 'a') as h:
                h.write("\n")
                h.write(folder)
        # print(folder_list)


    def playmusic():
        global play
        global pause
        if play == False:
            pym.mixer.music.play()
            play = True
            play_button.config(text="Pause")
        else:
            if pause == False:
                pym.mixer.music.pause()
                pause = True
                play_button.config(text="Play")
            else:
                pym.mixer.music.unpause()
                pause = False
                play_button.config(text="Pause")
        music_time_update()


    def prevsong():
        global length
        global current_song
        global n
        global playsong
        pym.mixer.music.stop()
        if current_song == songs[0]:
            pass
        else:
            n -= 1
            current_song = songs[n]
            playsong = pym.mixer.music.load(current_song)
            pym.mixer.music.play()
            pym.mixer.music.pause()

            name.config(text=current_song)
            if play and not pause:
                pym.mixer.music.play()
            elif play and pause:
                pass
        s1.set(0)
        m = MP3(current_song)
        length = m.info.length
        s1.config(to=length)
        converted_total_time = time.strftime('%M:%S', time.gmtime(length))
        total_time.config(text=converted_total_time)
        current_song_label.config(text=m.get('TIT2'))
        pym.mixer_music.queue(songs[n + 1])


    def nextsong():
        pym.mixer.music.stop()
        global length
        global current_song
        global n
        global playsong
        if current_song == songs[len(songs) - 1]:
            pass
        else:
            n += 1
            current_song = songs[n]
            playsong = pym.mixer.music.load(current_song)
            pym.mixer.music.play()
            pym.mixer.music.pause()

            name.config(text=current_song)
            if play and not pause:
                pym.mixer.music.play()
            elif play and pause:
                pass
        s1.set(0)
        m = MP3(current_song)
        length = m.info.length
        s1.config(to=length)
        converted_total_time = time.strftime('%M:%S', time.gmtime(length))
        total_time.config(text=converted_total_time)
        current_song_label.config(text=m.get('TIT2'))
        pym.mixer_music.queue(songs[n+1])


    def musicpos(event):
        pos = s1.get()
        pym.mixer.music.set_pos(pos)


    def volume(event):
        global vol_
        global mute
        vol = vol_slider.get()/100
        pym.mixer.music.set_volume(vol)
        mute = False
        vol_ = vol


    def mute_command():
        global mute
        if not mute:
            mute = True
            pym.mixer.music.set_volume(0)
            mute_button.config(text="Un mute")
            mute_button.update()
            vol_slider.config(value=0)
            vol_slider.update()
        else:
            mute = False
            pym.mixer.music.set_volume(vol_)
            mute_button.config(text="Mute")
            mute_button.update()
            vol_slider.config(value=vol_*100)
            vol_slider.update()


    def music_time_update():
        current_time = pym.mixer.music.get_pos()/1000
        converted_passed_time = time.strftime('%M:%S', time.gmtime(current_time))
        elapsed.config(text=f"{converted_passed_time}")
        elapsed.after(1000, music_time_update)
        s1.config(value=current_time)


    def about():
        showinfo("About", "Author: Ritik Kujur"
                "\nDate Creation Started: 21-08-2020"
                "\nDate Creation Finished: 23-08-2020"
                "\nPurpose: Self practice"
                "\nThanks for using my product")


    def show():
        global n
        global pause
        root = Tk()
        root.geometry("800x600")
        root.title('Playlist')
        # Functions

        def select(event):
            fol = event.widget.cget("text")
            print(fol)
            for i in folder_list:
                if fol == os.path.basename(i):
                    folderx = i
            os.chdir(folderx)
            for i in range(len(songs)):
                songs_display.delete(END)

            songs.clear()

            for song in os.listdir():
                if song.endswith(".mp3"):
                    songs.append(song)

            # print(songs)

            for song in songs:
                songs_display.insert(END, song)
            songs_display.update()


        def play_selected():
            global n
            global current_song
            global pause
            pause = True
            current_song = songs_display.get(ACTIVE)
            # current_song = current_song[3: len(current_song)]
            pym.mixer.music.load(current_song)
            pym.mixer.music.play()
            pym.mixer.music.pause()

            playmusic()

            # s1.set(0)
            m = MP3(current_song)
            length = m.info.length
            s1.config(to=length)
            converted_total_time = time.strftime('%M:%S', time.gmtime(length))
            total_time.config(text=converted_total_time)
            name.config(text=current_song)
            current_song_label.config(text=m.get('TIT2'))
            current_s_label.config(text=m.get('TIT2'))
            pym.mixer_music.queue(songs[n + 1])
            n = songs.index(current_song)

        f2 = Frame(root, bg='white')
        f2.pack(side=BOTTOM, fill=X)

        """Select folder Button"""
        # Current song
        current_s_label = Label(f2, text=f"Currently Playing:   {m.get('TIT2')}", bg='white')
        current_s_label.pack(side=LEFT)


        # file
        file = Label(f2, text=folder, bg='white')
        file.pack(side=RIGHT)

        if pause:
            statuss = "Paused"
        else:
            statuss = "Playing"

        play_status = Label(f2, text=f"Status:-  {statuss}")
        play_status.pack(side=RIGHT, padx=20)
        # Print Status
        def status():
            if pause:
                statuss = "Paused"
            else:
                statuss = "Playing"

            play_status.config(text=f"Status:-  {statuss}")
            play_status.after(200, status)
        status()

        def add():
            new_folder = askdirectory()
            if new_folder not in folder_list:
                folder_list.append(new_folder)

                b3 = ttk.Button(fol_list, text=f"{os.path.basename(new_folder)}")
                b3.pack(fill=X)
                b3.bind("<Button-1>", select)
                with open("folder_list.txt", 'a') as f:
                    f.write("\n")
                    f.write(new_folder)

            else:
                showinfo("Attention", "This folder is already in the folders list")

        def about():
            showinfo("About", "Author: Ritik Kujur"
                            "\nDate Creation Started: 21-08-2020"
                            "\nDate Creation Finished: 23-08-2020"
                            "\nPurpose: Self practice"
                            "\nThanks for using my product")


        """Making upper buttons and features bar"""
        b_frame = Frame(root, bd=1, relief=GROOVE, bg='blue')
        b_frame.pack(side=TOP, fill=X)


        # Making play button
        b2 = ttk.Button(b_frame, text='Play', command=play_selected)
        b2.pack()


        # Folder label
        fol_text = Label(root, text="Folders Name", font="Constantina 9 bold")
        fol_text.pack(side=TOP, anchor='nw', padx=10)

        """Making Folder List"""
        fol_list = Listbox(root)
        fol_list.pack(side=LEFT, anchor='nw', fill=Y)
        for folders in folder_list:
            folders = os.path.basename(folders)
            b = ttk.Button(fol_list, text=folders)
            b.pack(fill=X)
            b.bind("<Button-1>", select)

        """ScrollBar for folders"""
        fol_scroll = Scrollbar(root, command=fol_list.yview)
        fol_scroll.pack(side=LEFT, fill=Y)
        fol_list.config(yscrollcommand=fol_scroll.set)

        """YScrollBar for songs"""
        song_scroll = Scrollbar(root)
        song_scroll.pack(side=RIGHT, fill=Y)
        """XScrollBar for songs"""
        song_scrollx =Scrollbar(root, orient=HORIZONTAL)
        song_scrollx.pack(side=BOTTOM, fill=X)

        """Music list"""
        songs_display = Listbox(root, width=108, yscrollcommand=song_scroll.set, xscrollcommand=song_scrollx.set, font="Calibri 12")
        songs_display.pack(side=LEFT, fill=Y, anchor='nw')
        for i in os.listdir():
            if i.endswith(".mp3"):
                songs_display.insert(END,i)
        song_scroll.config(command=songs_display.yview)
        song_scrollx.config(command=songs_display.xview)

        """Add folder menu"""
        Mainmenu = Menu(root)
        Mainmenu.add_command(label="Add folder", command=add)
        Mainmenu.add_command(label="About", command=about)
        Mainmenu.add_command(label="Exit", command=quit)

        root.config(menu=Mainmenu)


    # Song Info

    m = MP3(current_song)
    pos = pym.mixer.music.get_pos() / 1000
    pos = int(pos)
    length = m.info.length

    # Music name frame
    name_frame = Frame(root, bg='white', borderwidth=5, relief=SUNKEN)
    name_frame.pack(side=TOP, fill=X)
    name = Label(name_frame, text=current_song, bg='white')
    name.pack(side=LEFT, anchor='w')

    # Statusbar
    status_frame = Frame(root, bg='white')
    status_frame.pack(side=BOTTOM, fill=X)
    # Current song
    current_song_label = Label(status_frame, text=m.get('TIT2'))
    current_song_label.pack(side=LEFT)
    # file
    file = Label(status_frame, text=folder, bg='white')
    file.pack(side=RIGHT)

    # Open Menu
    MainMenu = Menu(root)

    # Creating submenus
    open_menu = Menu(MainMenu, tearoff=0)
    open_menu.add_command(label="Open Folder", command=openfolder)
    open_menu.add_command(label="Show Library", command=show)
    open_menu.add_separator()
    open_menu.add_command(label="Exit", command=quit)

    MainMenu.add_cascade(label="Open", menu=open_menu)

    MainMenu.add_command(label="About", command=about)
    MainMenu.add_command(label="Exit", command=quit)

    root.config(menu=MainMenu)

    root.config(bg='grey')

    # Scale Frame
    sc_frame = Frame(root, relief=GROOVE, borderwidth=1)
    sc_frame.pack(side=TOP, fill=X)


    # Scale
    s1 = ttk.Scale(sc_frame, orient=HORIZONTAL, command=musicpos, from_=0, to=length, value=0)
    s1.pack(side=TOP, padx=10, fill=X)

    s1.set(pos)

    # Print time elapsed
    converted_elapsed_time = time.strftime('%M:%S', time.gmtime(pos))
    elapsed = Label(sc_frame, text='00:00')
    elapsed.pack(side=LEFT)

    # Total time
    converted_total_time = time.strftime('%M:%S', time.gmtime(length))
    total_time = Label(sc_frame, text=converted_total_time)
    total_time.pack(side=RIGHT)

    play_frame = Frame(root, bg='blue')
    play_frame.pack(anchor='w', side=BOTTOM, fill=X)

    # Buttons
    prev_button = Button(play_frame, text="Previous", borderwidth=5, bg='blue', fg='white', padx=32, command=prevsong)
    prev_button.pack(side=LEFT)

    play_button = Button(play_frame, text="play", borderwidth=5, bg='blue', fg='white', padx=25, command=playmusic)
    play_button.pack(side=LEFT)

    next_button = Button(play_frame, text="Next", borderwidth=5, bg='blue', fg='white', padx=40, command=nextsong)
    next_button.pack(side=LEFT)


    # Volume frame
    vol_frame = Frame(root)
    vol_frame.pack(side=BOTTOM, fill=X)
    # Volume slider
    vol_slider = ttk.Scale(vol_frame, command=volume, value=100, from_=0, to=100)
    vol_slider.pack(side=RIGHT)
    # Volume text
    vol_text = Label(vol_frame, text="Volume    ")
    vol_text.pack(side=RIGHT)
    # Mute button
    mute_button = ttk.Button(vol_frame, text="Mute", command=mute_command)
    mute_button.pack(side=LEFT)

    root.mainloop()
main()
