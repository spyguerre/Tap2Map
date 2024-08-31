import tkinter as tk
import os
import pygame
import math
from datetime import datetime
import random
import shutil


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
    label2 = tk.Label(root, text="Click on the button above to start recording inputs!",
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
    settingsFrame = tk.Frame(root)
    bpmTxt = tk.Entry(settingsFrame, width=5)
    maxBeatDivTxt = tk.Entry(settingsFrame, width=2)
    startTimeTxt = tk.Entry(settingsFrame, width=6)
    inputOffsetTxt = tk.Entry(settingsFrame, width=4)
    maxTurnSpeedTxt = tk.Entry(settingsFrame, width=3)
    distancePerBeatTxt = tk.Entry(settingsFrame, width=3)
    genMapButton = tk.Button(root, text="Generate Map!", font=("Helvetica", 20, "bold"), relief=tk.GROOVE,
                             command=genOsuMapFolder, fg="#bc51e0")
    label3 = tk.Label(root, text="Fill in the settings above and click the button to generate the map!",
                      font=("times new roman", 15, "bold"))
    label4 = tk.Label(root, text="            BPM                   Max Beat Div                Start Time"
                                 "                  Input Offset         Max Turn Speed    Distance Per Beat",
                      font=("times new roman", 10, "bold"))
    smallBlank = tk.Label(root, text="", font=("times new roman", 5))


    return (title, inputtxt, dlButton, label1, volume, play_button, label2, countdown, cancelButton, saveRecButton,
            timeLabel, keysFrame, eButton, rButton, genMapButton, settingsFrame, bpmTxt, maxBeatDivTxt, startTimeTxt,
            inputOffsetTxt, maxTurnSpeedTxt, distancePerBeatTxt, label3, label4, smallBlank)


def clearScreen():
    for widget in root.winfo_children():
        widget.pack_forget()


def formatMap(startTime, osuBeatLength, maxBeatDiv, hitObjects):
    template = open("format.txt", "r").read()

    template = template.replace("<startTime>", str(startTime))
    template = template.replace("<osuBeatLength>", str(osuBeatLength))
    template = template.replace("<maxBeatDiv>", str(maxBeatDiv))
    template = template.replace("<hitObjects>", hitObjects)

    return template


def writeMapFolder(startTime, bpm, maxBeatDiv, hitObjectsText):
    if not os.path.isdir("./map/"):
        os.mkdir("./map/")

    open("map/-song_name- (-mapper-) [-difficulty_name-].osu", "w").write(
        formatMap(startTime, 60/bpm*1000, maxBeatDiv, hitObjectsText)
    )

    shutil.copyfile("song.mp3", "./map/song.mp3")


def findIndexForXmsBack(inputList, i, ms):
    inputTime = inputList[i]
    res = 0
    while inputList[res] < inputTime - ms:
        res += 1
    res -= 1
    return res


def checkPositions(inputList, osuPixels):
    # Returns wether the last circle from the list is at least this many osu pixels away from any other
    for i in range(len(inputList) - 1):
        if math.sqrt((inputList[i][0] - inputList[-1][0])**2 + (inputList[i][1] - inputList[-1][1])**2) < osuPixels:
            return False
    return True


def computePositions(cleanedInputs, beatLength, maxTurnSpeed, distancePerBeat):
    pos = [random.uniform(0, 512), random.uniform(0, 384)]
    vect = random.uniform(0, 2 * math.pi)
    vectSpeed = 0
    hitObjectsPos = []
    timesWentBack = 0
    i = 0
    while i < len(cleanedInputs):
        correctFlag = False
        tries = 0
        while not correctFlag and tries < 42:
            if i == 0:
                closeness = 1
            else:
                closeness = (cleanedInputs[i] - cleanedInputs[i - 1]) / beatLength
            vectSpeed += (closeness ** 3) * random.uniform(-maxTurnSpeed, maxTurnSpeed)
            vectSpeed = min(max(-maxTurnSpeed, vectSpeed), maxTurnSpeed)

            vect += vectSpeed

            pos = [pos[0] + math.cos(vect) * distancePerBeat * closeness,
                   pos[1] + math.sin(vect) * distancePerBeat * closeness]
            if pos[0] < 0:
                pos[0] = -pos[0]
                vect = math.pi - vect
                vectSpeed = -vectSpeed
            elif pos[0] > 512:
                pos[0] = 2 * 512 - pos[0]
                vect = math.pi - vect
                vectSpeed = -vectSpeed
            if pos[1] < 0:
                pos[1] = -pos[1]
                vect = math.pi - vect
                vectSpeed = -vectSpeed
            elif pos[1] > 384:
                pos[1] = 2 * 384 - pos[1]
                vect = math.pi - vect
                vectSpeed = -vectSpeed
            if not (0 <= pos[0] <= 512 and 0 <= pos[1] <= 384):
                pos = [random.uniform(0, 512), random.uniform(0, 384)]

            backTo = findIndexForXmsBack(cleanedInputs, i, 1000)
            correctFlag = checkPositions(hitObjectsPos[backTo:], distancePerBeat*0.9)
            tries += 1

            if correctFlag:
                hitObjectsPos.append(pos)
                i += 1
            elif tries == 42 and timesWentBack < 100:
                i = backTo
                hitObjectsPos = hitObjectsPos[:backTo]
                timesWentBack += 1
            elif tries == 42:
                hitObjectsPos.append(pos)
                i += 1

    return hitObjectsPos


def cleanInputs(inputs, time, beatLength, maxBeatDiv, inputOffset):
    # Function puts hit objects timings on the closest hard beat

    # cleanedInputs1 contains input list with inputs converted to miliseconds
    # and inputs that are too close to each other removed, compared to beat length
    cleanedInputs1 = []
    for input_ in inputs:
        input_ *= 1000
        if not cleanedInputs1:
            cleanedInputs1.append(input_)
        elif input_ > cleanedInputs1[-1] + beatLength/2:
            cleanedInputs1.append(input_)

    # cleanedInputs2 contains the list of inputs with corrected offsets
    cleanedInputs2 = []
    for input_ in cleanedInputs1:
        input_ = round((input_ - inputOffset - time) / beatLength) * beatLength + time
        cleanedInputs2.append(input_)

    # cleanedInputs3 contains the list of inputs corrcted to the closest hard beat (if alone)
    cleanedInputs3 = []
    osuBeatLength = beatLength * maxBeatDiv
    for i, input_ in enumerate(cleanedInputs2):
        correctedInput = round((input_ - time) / osuBeatLength) * osuBeatLength + time
        if i == 0:
            if (input_ <= cleanedInputs2[i+1] - osuBeatLength/4 + .0000001
                    and abs(correctedInput - input_) <= osuBeatLength/8 + .0000001):
                cleanedInputs3.append(correctedInput)
            else:
                cleanedInputs3.append(input_)
        elif i == len(cleanedInputs2) - 1:
            if (cleanedInputs3[i-1] + osuBeatLength/4 <= input_ + .0000001
                    and abs(correctedInput - input_) <= osuBeatLength/8 + .0000001):
                cleanedInputs3.append(correctedInput)
            else:
                cleanedInputs3.append(input_)
        else:
            if (cleanedInputs3[i-1] + osuBeatLength/4
                    <= input_ + .0000001
                    <= cleanedInputs2[i+1] - osuBeatLength/4 + .0000002
                    and abs(correctedInput - input_) <= osuBeatLength/8 + .0000001):
                cleanedInputs3.append(correctedInput)
            else:
                cleanedInputs3.append(input_)

    return cleanedInputs3


def genOsuMapFolder():
    # Map settings
    bpm = float(bpmTxt.get())
    maxBeatDiv = int(maxBeatDivTxt.get())
    time = float(startTimeTxt.get())
    inputOffset = int(inputOffsetTxt.get())
    maxTurnSpeed = int(maxTurnSpeedTxt.get())/360*2*math.pi
    distancePerBeat = int(distancePerBeatTxt.get())

    # Read data from recording.txt
    inputs = open("recording.txt").readlines()
    inputs = [float(input_[:-2]) for input_ in inputs]
    beatLength = 60 / bpm * 1000 / maxBeatDiv

    # Set inputs on the beats and remove the duplicates
    cleanedInputs = cleanInputs(inputs, time, beatLength, maxBeatDiv, inputOffset)

    # Compute random hit objects' position
    hitObjectsPos = computePositions(cleanedInputs, beatLength, maxTurnSpeed, distancePerBeat)

    hitObjectsText = "\n".join([
        f"{hitObjectsPos[i][0]},{hitObjectsPos[i][1]},{cleanedInputs[i]},{5 if i == 0 else 1},0,1:0:0:0:" for i in
        range(len(cleanedInputs))
    ])

    writeMapFolder(time, bpm, maxBeatDiv, hitObjectsText)

    genMapButton.config(state=tk.DISABLED, text="Map Generated!", bg="#22e06b")
    root.after(5000, lambda: genMapButton.config(state=tk.NORMAL, text="Generate Map!", bg="#f0f0f0"))

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
    pygame.mixer.music.load("song.mp3")
    osuBeatLength = int(60 / int(bpmTxt.get()) * 1000) if bpmTxt.get() != "" else 1000
    root.after(osuBeatLength, lambda: countdown.config(text="2"))
    root.after(2*osuBeatLength, lambda: countdown.config(text="1"))
    root.after(3*osuBeatLength, lambda: countdown.config(text="Tap to Map using E and R..."))
    root.after(3*osuBeatLength, playSong)


def updateTimeLabel():
    timer = ":".join(str(datetime.now() - t0).split(':')[1:]).split('.')
    timeLabel.config(text=f"Recording for {timer[0]}.{0 if not timer[1] else timer[1][:1]}")
    if state == "record":
        root.after(99, updateTimeLabel)
    else:
        root.after(2000, updateTimeLabel)


def playSong():
    global t0
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

    dlButton.pack()

    label1.pack(pady=20)

    volume.pack(pady=20)

    play_button.pack()

    label2.pack(pady=20)

    label4.pack()

    settingsFrame.pack()
    bpmTxt.pack(side=tk.LEFT, padx=42)
    maxBeatDivTxt.pack(side=tk.LEFT, padx=42)
    startTimeTxt.pack(side=tk.LEFT, padx=42)
    inputOffsetTxt.pack(side=tk.LEFT, padx=42)
    maxTurnSpeedTxt.pack(side=tk.LEFT, padx=42)
    distancePerBeatTxt.pack(side=tk.LEFT, padx=42)

    smallBlank.pack()

    genMapButton.pack()

    label3.pack(pady=20)


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
    root.geometry("842x690")
    pygame.init()
    pygame.mixer.init()

    (title, inputtxt, dlButton, label1, volume, play_button, label2, countdown, cancelButton,
     saveRecButton, timeLabel, keysFrame, eButton, rButton, genMapButton, settingsFrame, bpmTxt, maxBeatDivTxt, startTimeTxt,
     inputOffsetTxt, maxTurnSpeedTxt, distancePerBeatTxt, label3, label4, smallBlank) = defineWidgets()

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
