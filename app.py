import tkinter as tk
import os
import pygame
import math
from datetime import datetime


def defineWidgets():
    title = tk.Label(root, text="Osu! Tap2Map", bd=9, relief=tk.GROOVE,
                     font=("times new roman", 42, "bold"), bg="white", fg="#aa36d1")
    inputtxt = tk.Text(root, height=1, width=50)
    dlButton = tk.Button(root, text="Download Song!", font=("Helvetica", 20), relief=tk.GROOVE,
                         command=lambda: dlSong(inputtxt.get(1., "end-1c")), fg="#bc51e0")
    label1 = tk.Label(root,
                      text="Either enter the youtube link to the song to tap to, or place an song.mp3 file in root directory!",
                      font=("times new roman", 15, "bold"))
    volume = tk.Scale(root, from_=0, to=1, orient=tk.HORIZONTAL, digits=3, resolution=0.01, showvalue=0, label="Volume",
                      command=lambda _: updateVolume())
    volume.set(.42)
    play_button = tk.Button(root, text="Play Song!", font=("Helvetica", 20), relief=tk.GROOVE, command=play,
                            fg="#bc51e0")
    label2 = tk.Label(root, text="Click on the button above or start tapping (with E & R) to start recording inputs!",
                      font=("times new roman", 15, "bold"))
    countdown = tk.Label(root, font=("times new roman", 42, "bold"))
    cancelButton = tk.Button(root, text="Cancel Recording", font=("Helvetica", 20), relief=tk.GROOVE,
                             command=showMain, fg="#c42535")
    saveRecButton = tk.Button(root, text="Save Recording!", font=("Helvetica", 20), relief=tk.GROOVE,
                              command=saveRecording, fg="#6ec21b")
    timeLabel = tk.Label(root, font=("times new roman", 15, "bold"))
    keysFrame = tk.Frame(root)
    eButton = tk.Button(keysFrame, text="E", font=("times new roman", 25, "bold"), state=tk.DISABLED,
                        relief=tk.RAISED, width=5)
    rButton = tk.Button(keysFrame, text="R", font=("times new roman", 25, "bold"), state=tk.DISABLED,
                        relief=tk.RAISED, width=5)

    return (title, inputtxt, dlButton, label1, volume, play_button, label2, countdown, cancelButton, saveRecButton,
            timeLabel, keysFrame, eButton, rButton)


def clearScreen():
    for widget in root.winfo_children():
        widget.pack_forget()


def saveRecording():
    open("recording.txt", "w").write(buffer)
    showMain()


def dlSong(url):
    global dlButton
    if os.path.isfile("song.mp3"):
        pygame.mixer.music.unload()
        os.remove("song.mp3")
    dlButton.config(state=tk.DISABLED, text="Downloading Song...")
    os.system(f"yt-dlp -x --audio-format mp3 -o song {url}")
    dlButton.config(state=tk.DISABLED, text="Song Downloaded!", bg="#22e06b")
    root.after(5000, lambda: dlButton.config(state=tk.NORMAL, text="Download Song!", bg="#f0f0f0"))


def play():
    global volume, state, buffer
    clearScreen()
    state = "record"
    buffer = ""

    title.pack()
    volume.pack(pady=20)
    countdown.pack(pady=20)
    keysFrame.pack(pady=10)
    eButton.pack(side=tk.LEFT, padx=20)
    rButton.pack(side=tk.LEFT, padx=20)
    saveRecButton.pack(pady=20)
    cancelButton.pack(pady=20)

    countdown.config(text="3")
    root.after(1000, lambda: countdown.config(text="2"))
    root.after(2000, lambda: countdown.config(text="1"))
    root.after(3000, lambda: countdown.config(text="Tap to Map using E and R..."))
    root.after(3000, playSong)


def updateTimeLabel():
    timer = ":".join(str(datetime.now() - t0).split(':')[1:]).split('.')
    timeLabel.config(text=f"Recording for {timer[0]}.{0 if not timer[1] else timer[1][:1]}")
    if state == "record":
        root.after(99, updateTimeLabel)
    else:
        root.after(2000, updateTimeLabel)


def playSong():
    global t0
    pygame.mixer.music.load("song.mp3")
    updateVolume()
    pygame.mixer.music.play()
    t0 = datetime.now()
    timeLabel.pack(pady=20)


def updateVolume():
    global volume
    pygame.mixer.music.set_volume(1 - math.pow(1 - volume.get(), 1 / 3))

def showMain():
    global state
    state = "main"
    clearScreen()
    pygame.mixer.music.stop()

    title.pack(side=tk.TOP)

    inputtxt.pack(pady=20)

    dlButton.pack(pady=20)

    label1.pack(pady=20)

    volume.pack(pady=20)

    play_button.pack()

    label2.pack(pady=20)


def onKeyPress(event):
    global e, r, buffer

    recThisInput = False
    if str(event.char) == "e" and not e:
        e = True
        eButton.config(relief=tk.SUNKEN)
        recThisInput = True
    elif str(event.char) == "r" and not r:
        r = True
        rButton.config(relief=tk.SUNKEN)
        recThisInput = True

    if recThisInput:
        curRecTime = datetime.now()
        buffer += f"{(curRecTime - t0).total_seconds()}\n"


def onKeyRelease(event):
    global e, r
    if str(event.char) == "e":
        e = False
        eButton.config(relief=tk.RAISED)
    elif str(event.char) == "r":
        r = False
        rButton.config(relief=tk.RAISED)


if __name__ == "__main__":
    root = tk.Tk()
    root.title('Osu! Tap2Map')
    root.geometry("842x642")
    pygame.init()
    pygame.mixer.init()

    (title, inputtxt, dlButton, label1, volume, play_button, label2, countdown, cancelButton,
     saveRecButton, timeLabel, keysFrame, eButton, rButton) = defineWidgets()

    state = "main"
    t0 = datetime.now()
    buffer = ""
    e = False
    r = False
    root.bind('<KeyPress>', onKeyPress)
    root.bind('<KeyRelease>', onKeyRelease)

    showMain()
    root.config()
    root.after(1000, updateTimeLabel)
    root.mainloop()
