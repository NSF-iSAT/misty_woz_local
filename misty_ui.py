from os import scandir
import PySimpleGUI as sg
from misty_scan import initial_ip_scan_window as misty_ip_scan
from kaleb_mistyPy import Robot
import cv2
import time

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

def speak(robot, ssml_string):
    print("Speak:", ssml_string)
    robot.speak(ssml_string)

def move_arms(robot, arm, move):
    # NOTE: feel free to change the input vars -- just adjust the functions_mapping entry accordingly
    if arm == "both": # move both arms
        # parameters for moveArms(self, rightArmPosition, leftArmPosition, rightArmVelocity, leftArmVelocity, units)
        print("move", arm, "arm", move)
        if move == "up":
            robot.moveArms(10, 10, 10, 10, units = "position")
        elif move == "down":
            robot.moveArms(0, 0, 10, 10, units = "position")
        elif move == "straight":
            robot.moveArms(5, 5, 10, 10, units = "position")
    else: # move one arm
        # parameters for moveArm(self, arm, position, velocity, units)
        print("move", arm, "arm", move)
        if move == "up":
            robot.moveArm(arm, 10, 10, "position")
        elif move == "down":
            robot.moveArm(arm, 0, 10, "position")
        elif move == "straight":
            robot.moveArm(arm, 5, 10, "position")

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
                 "contentLeft": 'e_ContentLeft.jpg', #stage left
                 "contentRight": 'e_ContentRight.jpg', #stage right
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
                 "terrorLeft": 'e_TerrorLeft.jpg', #stage left
                 "terrorRight": 'e_TerrorRight.jpg' #stage right
                }

    print("Show", expression, "expression")
    robot.changeImage(expr_dict.get(expression))

def get_speech(robot):
    print("Misty is listening")
    robot.captureSpeech()
    print("Misty has stoped listening")


# # # # # 

def main(misty_ip):
    # robot = None
    # robot = Robot(misty_ip)
    misty_ip = '10.200.193.1'
    robot = Robot(misty_ip)
    
    # av streaming source: https://github.com/CPsridharCP/MistySkills/blob/master/Apps/Teleop/02_pythonTeleop/mistyTeleop.py
    robot.startAvStream(url='rtspd:1935', dimensions=(640, 480))
    print("Starting Misty's camera")
    time.sleep(2) #allows Misty to open up the stream before connecting to it
    cap = cv2.VideoCapture('rtsp://' + misty_ip + ':1935')
    if not(cap.isOpened()):
        print("cannot open rtsp")
        
    robot.setDefaultVolume(5)
    
    video_feed = [
        [sg.Text("Video Feed", size=(10, 1), justification="center")],
        [sg.Image(filename="", key="-IMAGE-")]
    ]

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

    arm_control = [
        [sg.Text("Arms")],
        [sg.Button("Arms Up", key = "ARMS_UP"),
            sg.Button("Arms Down", key = "ARMS_DOWN"),
            sg.Button("Arms Straight", key = "ARMS_STRAIGHT")],
        [sg.Button("Left Arm Up", key = "LEFT_ARM_UP"),
            sg.Button("Left Arm Down", key = "LEFT_ARM_DOWN"),
            sg.Button("Left Arm Straight", key = "LEFT_ARM_STRAIGHT")],
        [sg.Button("Right Arm Up", key = "RIGHT_ARM_UP"),
            sg.Button("Right Arm Down", key = "RIGHT_ARM_DOWN"),
            sg.Button("Right Arm Straight", key = "RIGHT_ARM_STRAIGHT")]
    ]

    # GUI drop down menu to change Misty face expression
    # resource: https://csveda.com/python-combo-and-listbox-with-pysimplegui/
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
    
    voice_controls = [
        [sg.Text("Speech to Text")],
        [sg.Button("Listen", key = "LISTEN", enable_events=True)]
    ]

    # TODO: add display window for robot camera
        # (this can be in the PySimpleGUI window, or in a separate window -- coder's choice :))
        # https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html

    layout = [
        [sg.Column(video_feed),sg.VSeperator(),
        sg.Column([[sg.Column(head_controls)],
                    [sg.Column(speak_input)],
                    [sg.Column(voice_controls)],
                    [sg.Column(led_control)],
                    [sg.Column(arm_control)],
                    [sg.Column(expression_list)]])]
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
        # both arms
        "ARMS_UP": lambda: move_arms(robot, "both", "up"),
        "ARMS_DOWN": lambda: move_arms(robot, "both", "down"),
        "ARMS_STRAIGHT": lambda: move_arms(robot, "both", "straight"),
        # left arm, stage left
        "LEFT_ARM_UP": lambda: move_arms(robot, 'left', "up"),
        "LEFT_ARM_DOWN": lambda: move_arms(robot, 'left', "down"),
        "LEFT_ARM_STRAIGHT": lambda: move_arms(robot, 'left', "straight"),
        # right arm, stage right
        "RIGHT_ARM_UP": lambda: move_arms(robot, 'right', "up"),
        "RIGHT_ARM_DOWN": lambda: move_arms(robot, 'right', "down"),
        "RIGHT_ARM_STRAIGHT": lambda: move_arms(robot, 'right', "straight"),
    }

    while True:
        event, values = window.read(timeout=20)
        if event == "Exit" or event == sg.WIN_CLOSED:
            break

        if event in functions_mapping.keys():
            print("Actuation : ", event)
            functions_mapping[event]()
        
        if event == "SPEAK" and values["-TTS-".strip()]:
            #print("TTS : ", values["-TTS-"])
            speak(robot, values["-TTS-"])

        if event == "CLEAR":
            window["-TTS-"].update("")

        # TODO add event names for arms

        # event names for expression
        if event == "my_expression":
            set_expression(robot, values["my_expression"])
            
        # event for speech to text
        if event == "LISTEN":
            get_speech(robot)
        
        # video functionality
        ret, frame = cap.read()
        if(ret == False):
            #print("frame is empty")
            pass
        else:
            #print("return is True")
            frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
            imgbytes = cv2.imencode(".png", frame)[1].tobytes()
            window["-IMAGE-"].update(data=imgbytes)
#            cv2.imshow("frame", frame)
#            cv2.waitKey(0)
        
    cap.release()
    cv2.destroyAllWindows()
    robot.stopAvStream()

    window.close()

if __name__ == "__main__":
    # misty_ip = misty_ip_scan()
    misty_ip = ""
    main(misty_ip)
