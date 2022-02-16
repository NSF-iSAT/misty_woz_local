from os import scandir
import PySimpleGUI as sg
from misty_scan import initial_ip_scan_window as misty_ip_scan
from kaleb_mistyPy import Robot

def tilt(robot, direction):
    print("TILT", direction)
    if direction == "left": # house left
        # parameter order: roll, pitch, yaw, velocity
        robot.moveHeadPosition(5, 0, 0, 10)
    elif direction == "right": # house right
        robot.moveHeadPosition(-5, 0, 0, 10)

def look(robot, direction):
    print("LOOK", direction)
    if direction == "up": # negative pitch
        # parameter order: roll, pitch, yaw, velocity
        robot.moveHeadPosition(0, -5, 0, 10)
    elif direction == "down":
        robot.moveHeadPosition(0, 5, 0, 10)
    elif direction == "left": # house left, negative yaw
        robot.moveHeadPosition(0, 0, -5, 10)
    elif direction == "right": # house right
        # doesn't go as far right as left
        # looks like 45 degree yaw, versus 90 degree yaw seen with "left"
        robot.moveHeadPosition(0, 0, 5, 10)
    elif direction == "straight":
        robot.moveHeadPosition(0, 0, 0, 10)

def led(robot, color):
    print("LED", color)
    if color == "red":
        robot.changeLED(255, 0, 0)
    elif color == "green":
        robot.changeLED(0, 255, 0)
    elif color == "blue":
        robot.changeLED(0, 0, 255)

#TODO implement
# TODO
def speak(robot, ssml_string):
    print("Speak", ssml_string)
    pass

# TODO
def move_arms(robot, arm, move):
    # NOTE: feel free to change the input vars -- just adjust the functions_mapping entry accordingly
    pass

# TODO
def set_expression(robot, expression):
    # NOTE: one nice feature for this function would be to add a "duration" parameter
    #      so that the expression can be set for a certain amount of time (or forever)
    #      and then revert to a "default" expression
    # used robot.printImageList() to get list of saved images
    # use a dictionary instead of if/elif statement
    # dictionary maps key word to full jpg file name of expression
    
    expr_dict = {"admiration": 'e_Admiration.jpg',
                 "aggressive": 'e_Aggressiveness.jpg',
                 "amazement": 'e_Amazement.jpg',
                 "anger": 'e_Anger.jpg',
                 "apprehension": 'e_ApprehensionConcerned.jpg',
                 "contempt": 'e_Contempt.jpg',
                 "contentLeft": 'e_ContentLeft.jpg',
                 "contentRight": 'e_ContentRight.jpg',
                 "default": 'e_DefaultContent.jpg',
                 "disgust": 'e_Disgust.jpg',
                 "disorientated": 'e_Disoriented.jpg',
                 "fear": 'e_Fear.jpg',
                 "grief": 'e_Grief.jpg',
                 "hilarious": 'e_EcstacyHilarious.jpg',
                 "joy1": 'e_Joy.jpg',
                 "joy2": 'e_Joy2.jpg',
                 "joyGoofy1": 'e_JoyGoofy.jpg',
                 "joyGoofy2": 'e_JoyGoofy2.jpg',
                 "joyGoofy3": 'e_JoyGoofy3.jpg',
                 "love": 'e_Love.jpg',
                 "rage1": 'e_Rage.jpg',
                 "rage2": 'e_Rage2.jpg',
                 "rage3": 'e_Rage3.jpg',
                 "rage4": 'e_Rage4.jpg',
                 "remorse": 'e_RemorseShame.jpg',
                 "sadness": 'e_Sadness.jpg',
                 "sleeping": 'e_Sleeping.jpg',
                 "sleepingZZZ": 'e_SleepingZZZ.jpg',
                 "sleepy1": 'e_Sleepy.jpg',
                 "sleepy2": 'e_Sleepy2.jpg',
                 "sleepy3": 'e_Sleepy3.jpg',
                 "sleepy4": 'e_Sleepy4.jpg',
                 "starryEyed": 'e_EcstacyStarryEyed.jpg',
                 "surprise": 'e_Surprise.jpg',
                 "blackScreen": 'e_SystemBlackScreen.jpg',
                 "blinkingLarge": 'e_SystemBlinkLarge.jpg',
                 "blinkingStandard": 'e_SystemBlinkStandard.jpg',
                 "camera": 'e_SystemCamera.jpg',
                 "flash": 'e_SystemFlash.jpg',
                 "gearPrompt": 'e_SystemGearPrompt.jpg',
                 "logoPrompt": 'e_SystemLogoPrompt.jpg',
                 "terror1": 'e_Terror.jpg',
                 "terror2": 'e_Terror2.jpg',
                 "terrorLeft": 'e_TerrorLeft.jpg',
                 "terrorRight": 'e_TerrorRight.jpg'
                }

    print("Show", expression, "expression")
    robot.changeImage(expr_dict.get(expression))

# # # # # 

def main(misty_ip):
    # robot = None
    # robot = Robot(misty_ip)
    robot = Robot('10.200.195.151')
    

    head_controls = [
        [sg.Text("Look")],
        [sg.Button("TILT LEFT", key = "TILT_LEFT"), sg.Button("UP", key = "LOOK_UP"), sg.Button("TILT RIGHT", key = "TILT_RIGHT")],
        [sg.Button("LEFT", key = "LOOK_LEFT"), sg.Button("STRAIGHT", key = "LOOK_STRAIGHT"), sg.Button("RIGHT", key = "LOOK_RIGHT")],
        [sg.Button("             "), sg.Button("DOWN", key = "LOOK_DOWN"), sg.Button("           ")]
    ]

    speak_input = [
        [sg.Text("Text to Speech")],
        [sg.Input(size=(50, 5), enable_events=True, key="-TTS-")],
        [sg.Button("Speak", key = "SPEAK"), sg.Button("Clear", key = "CLEAR")]
    ]

    led_control = [
        [sg.Text("LED Control")],
        [sg.Button("RED", key = "LED_RED"), sg.Button("GREEN", key = "LED_GREEN"), sg.Button("BLUE", key = "LED_BLUE")]
    ]

    # TODO add GUI for arms
    arm_control = [
        [sg.Text("Arms")],
        [sg.Button("Left Arm"), sg.Button("Right Arm")]
    ]

    # GUI drop down menu to change Misty face expression
    # enable_events=True means that when a drop down menu item
    # is selected, then the face changes automatically
    expression_list = [
        [sg.Text("Face Expression")],
        [sg.Combo(["admiration",
                   "aggressive",
                   "amazement",
                   "anger",
                   "apprehension",
                   "contempt",
                   "contentLeft",
                   "contentRight",
                   "default",
                   "disgust",
                   "disorientated",
                   "fear",
                   "grief",
                   "hilarious",
                   "joy1",
                   "joy2",
                   "joyGoofy1",
                   "joyGoofy2",
                   "joyGoofy3",
                   "love",
                   "rage1",
                   "rage2",
                   "rage3",
                   "rage4",
                   "remorse",
                   "sadness",
                   "sleeping",
                   "sleepingZZZ",
                   "sleepy1",
                   "sleepy2",
                   "sleepy3",
                   "sleepy4",
                   "starryEyed",
                   "surprise",
                   "blackScreen",
                   "blinkingLarge",
                   "blinkingStandard",
                   "camera",
                   "flash",
                   "gearPrompt",
                   "logoPrompt",
                   "terror1",
                   "terror2",
                   "terrorLeft",
                   "terrorRight"],
                  enable_events=True, key = "my_expression")]
    ]

    # TODO: add display window for robot camera
        # (this can be in the PySimpleGUI window, or in a separate window -- coder's choice :))
        # https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html

    layout = [
        [sg.Column([[sg.Column(head_controls)],[sg.Column(speak_input)],
        [sg.Column(led_control)],[sg.Column(arm_control)],
        [sg.Column(expression_list)]])],
    ]

    window = sg.Window("Misty UI", layout)

    functions_mapping = {
        # events and mapping for head
        "TILT_LEFT": lambda: tilt(robot, "left"),
        "TILT_RIGHT": lambda: tilt(robot, "right"),
        "LOOK_UP": lambda: look(robot, "up"),
        "LOOK_DOWN": lambda: look(robot, "down"),
        "LOOK_LEFT": lambda: look(robot, "left"),
        "LOOK_RIGHT": lambda: look(robot, "right"),
        "LOOK_STRAIGHT": lambda: look(robot, "straight"),
        # events and mapping for LED color
        "LED_RED": lambda: led(robot, "red"),
        "LED_GREEN": lambda: led(robot, "green"),
        "LED_BLUE": lambda: led(robot, "blue"),
        # TODO events and mapping for arms
    }

    while True:
        event, values = window.read(timeout=20)
        if event == "Exit" or event == sg.WIN_CLOSED:
            break

        if event in functions_mapping.keys():
            print("Actuation : ", event)
            functions_mapping[event]()
        
        if event == "Speak" and values["-TTS-".strip()]:
            print("TTS : ", values["-TTS-"])
            speak(robot, values["-TTS-"])

        if event == "Clear":
            window["-TTS-"].update("")

        # TODO add event names for arms

        # event names for expression
        if event == "my_expression":
            set_expression(robot, values["my_expression"])

    window.close()

if __name__ == "__main__":
    # misty_ip = misty_ip_scan()
    misty_ip = ""
    main(misty_ip)
