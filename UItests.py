# Mock up of UI

from guizero import App, Text,TextBox, PushButton, Window, yesno, ButtonGroup, Combo


def resetRotaryScale():
    print("resetting rotary")

def resetLinearScale():
    print("resetting linear")

def advanceForward():
    print("advance forward")

def advanceBackward():
    print("advance backward")


app = App(title="Rose Engine", width=700, height=300, layout="grid")

labelOpMode = Text(app, size=16, text="Operating Mode:", align="left", grid=[0,0])
operatingMode = Combo(app, options=["Stopped", "Setup position", "Setup advance", "Engraving"], selected="Stopped", grid=[0,1], width=12)

labelSetupMode = Text(app, size=16, text="Setup position", align="left", width=20, grid=[1,0])
setupPositionMode = Combo(app, options=["Linear", "Rotary"], selected="Linear", grid=[1,1])


labelRotary = Text(app, size=16, text="Rotary:", grid=[2,0])
textRotary = Text(app, size=16, text="0.00", width=10, grid=[3,0])

labelLinear = Text(app, size=16, text="Linear:", grid=[2,1])
textLinear = Text(app, size=16, text="0.00", width=10, grid=[3,1])

resetRotaryButton = PushButton(app, command=resetRotaryScale, text="Reset", grid=[4,0])
resetLinearButton = PushButton(app, command=resetLinearScale, text="Reset", grid=[4,1])

#Advance controls
labelSdvanceMode = Text(app, size=16, text="Setup advance", align="left", width=20, grid=[1,3])
setupAdvanceMode = Combo(app, options=["Linear", "Rotary"], selected="Linear", grid=[1,4])

labelAdvanceLinear = Text(app, size=16, text="Linear advance:", grid=[2,3])
textAdvanceLinear = Text(app, size=16, text="2mm", grid=[3,3])
labelAdvanceRotary = Text(app, size=16, text="Rotary advance", grid=[2,4])
textAdvanceRotary = Text(app, size=16, text="5degrees", grid=[3,4])

advanceForwardButton = PushButton(app, command=advanceForward, text="Forward", grid=[0,5])
advanceBackwardButton = PushButton(app, command=advanceBackward, text="Back", grid=[1,5])




app.display()
