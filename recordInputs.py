import time
from pynput.mouse import Button, Listener as Mlis


def main():
    with Mlis(on_click=on_click) as mlistener:
        mlistener.join()


def on_click(x, y, button, pressed):
    global recording, startRecTime, buffer

    # Update pressed buttons
    pressedKeys[str(button).split(".")[1]] = pressed

    # Cancel recording and stop listener
    if button == Button.x1 and pressedKeys["x2"] or button == Button.x2 and pressedKeys["x1"]:
        print("Cancelled recording, quitting...")
        return False

    # Start/Stop Recording
    if button == Button.middle and pressed:
        if not recording:
            print("Started recording...")
            startRecTime = time.time()
        else:
            print("Stopped recording.")
            open("recording.txt", "w").write(buffer)
            print("Wrote Hit Objects to file 'recordedInputs.txt', quitting...")
            return False  # Stop program to avoid overwrite
        recording = not recording

    # Record inputs
    if (button == Button.left or button == Button.right) and recording and pressed:
        curRecTime = time.time()
        buffer += f"{curRecTime - startRecTime}\n"


if __name__ == '__main__':
    recording = False
    startRecTime = 0
    buffer = ""
    pressedKeys = {"left": False, "right": False, "x1": False, "x2": False}

    main()
