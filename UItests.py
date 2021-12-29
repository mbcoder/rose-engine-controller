# Mock up of UI

from guizero import App, Text, TextBox, PushButton, Window, yesno, ButtonGroup, Combo


class OpMode:
    def __init__(self):
        pass

    STOPPED = 1
    SETUP_POS = 2
    SETUP_ADV = 3
    ENGRAVING = 4


class Motion:
    def __init__(self):
        pass

    LINEAR = 1
    ROTARY = 2


currentMode = OpMode.STOPPED
setupMode = Motion.LINEAR
advanceMode = Motion.LINEAR


def changeOpMode(selected_value):
    global currentMode

    if selected_value == "Stopped":
        currentMode = OpMode.STOPPED
        print("--mode ", currentMode)
    elif selected_value == "Setup position":
        currentMode = OpMode.SETUP_POS
        print("--mode ", currentMode)

    elif selected_value == "Setup advance":
        currentMode = OpMode.SETUP_ADV
        print("--mode ", currentMode)

    elif selected_value == "Engraving":
        currentMode = OpMode.ENGRAVING
        print("--mode ", currentMode)


def changeSetupMode(selected_value):
    global setupMode

    if selected_value == "Linear":
        setupMode = Motion.LINEAR
    else:
        setupMode = Motion.ROTARY


def changeAdvanceMode(selected_value):
    global advanceMode

    if selected_value == "Linear":
        advanceMode = Motion.LINEAR
    else:
        advanceMode = Motion.ROTARY


def resetRotaryScale():
    print("resetting rotary")


def resetLinearScale():
    print("resetting linear")


def advanceForward():
    global currentMode

    print("advance forward")
    print("mode ", currentMode)


def advanceBackward():
    print("advance backward")


app = App(title="Rose Engine", width=700, height=300, layout="grid")

labelOpMode = Text(app, size=16, text="Operating Mode:", align="left", grid=[0, 0])
operatingMode = Combo(app, options=["Stopped", "Setup position", "Setup advance", "Engraving"], selected="Stopped",
                      grid=[0, 1], width=12, command=changeOpMode)

labelSetupMode = Text(app, size=16, text="Setup position", align="left", width=20, grid=[1, 0])
setupPositionMode = Combo(app, options=["Linear", "Rotary"], selected="Linear", grid=[1, 1], command=changeSetupMode)

labelRotary = Text(app, size=16, text="Rotary:", grid=[2, 0])
textRotary = Text(app, size=16, text="0.00", width=10, grid=[3, 0])

labelLinear = Text(app, size=16, text="Linear:", grid=[2, 1])
textLinear = Text(app, size=16, text="0.00", width=10, grid=[3, 1])

resetRotaryButton = PushButton(app, command=resetRotaryScale, text="Reset", grid=[4, 0])
resetLinearButton = PushButton(app, command=resetLinearScale, text="Reset", grid=[4, 1])

# Advance controls
labelSdvanceMode = Text(app, size=16, text="Setup advance", align="left", width=20, grid=[1, 3])
setupAdvanceMode = Combo(app, options=["Linear", "Rotary"], selected="Linear", grid=[1, 4], command=changeAdvanceMode)

labelAdvanceLinear = Text(app, size=16, text="Linear advance:", grid=[2, 3])
textAdvanceLinear = Text(app, size=16, text="2mm", grid=[3, 3])
labelAdvanceRotary = Text(app, size=16, text="Rotary advance", grid=[2, 4])
textAdvanceRotary = Text(app, size=16, text="5degrees", grid=[3, 4])

advanceForwardButton = PushButton(app, command=advanceForward, text="Forward", grid=[0, 5])
advanceBackwardButton = PushButton(app, command=advanceBackward, text="Back", grid=[1, 5])

app.display()

print("running here?")