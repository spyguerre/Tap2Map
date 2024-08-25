import random
import math


# Map settings
bpm = 200
maxBeatDiv = 4
time = 2481
recordSpeed = 0.8
maxTurnSpeed = math.pi/3
distancePerBeat = 30

# Read data from recordings.txt
inputs = open("recording.txt").readlines()
inputs = [float(input_[:-2]) for input_ in inputs]
beatLength = 60/bpm*1000/maxBeatDiv

# Set inputs on the beats and remove the duplicates
cleanedInputs = []
for input_ in inputs:
    input_ = round((input_*1000*recordSpeed - time)/beatLength)*beatLength + time
    if not cleanedInputs:
        cleanedInputs.append(input_)
    elif input_ > cleanedInputs[-1]:
        cleanedInputs.append(input_)

# Compute random hit objects' position
pos = [random.uniform(0, 512), random.uniform(0, 384)]
vect = random.uniform(0, 2*math.pi)
vectSpeed = 0
hitObjectsPos = []
for i in range(len(cleanedInputs)):
    if i == 0:
        closeness = 1
    else:
        closeness = (cleanedInputs[i] - cleanedInputs[i-1])/beatLength
    vectSpeed += (closeness ** 3)* random.uniform(-maxTurnSpeed, maxTurnSpeed)
    vectSpeed = min(max(-maxTurnSpeed, vectSpeed), maxTurnSpeed)

    vect += vectSpeed

    pos = [pos[0] + math.cos(vect) * distancePerBeat * closeness, pos[1] + math.sin(vect) * distancePerBeat * closeness]
    if pos[0] < 0:
        pos[0] = -pos[0]
        vect = math.pi - vect
        vectSpeed = -vectSpeed
    elif pos[0] > 512:
        pos[0] = 2*512 - pos[0]
        vect = math.pi - vect
        vectSpeed = -vectSpeed
    if pos[1] < 0:
        pos[1] = -pos[1]
        vect = math.pi - vect
        vectSpeed = -vectSpeed
    elif pos[1] > 384:
        pos[1] = 2*384 - pos[1]
        vect = math.pi - vect
        vectSpeed = -vectSpeed
    if not 0 <= pos[0] <= 512 and 0 <= pos[1] <= 384:
        pos = [random.uniform(0, 512), random.uniform(0, 384)]

    hitObjectsPos.append(pos)

open("hitObjects.txt", "w").write("\n".join(
    [
        f"{hitObjectsPos[i][0]},{hitObjectsPos[i][1]},{cleanedInputs[i]},{5 if i == 0 else 1},0,1:0:0:0:" for i in range(len(cleanedInputs))
    ]
))
