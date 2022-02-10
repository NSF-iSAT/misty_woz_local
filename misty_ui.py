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
def speak(robot, ssml_string):
    print("Speak", ssml_string)
    pass

# # # # # 

def main(misty_ip):
    # robot = None
    # robot = Robot(misty_ip)
    robot = Robot('10.200.192.135')
    

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

    layout = [
        [sg.Column([[sg.Column(head_controls)],[sg.Column(speak_input)], [sg.Column(led_control)]])],
    ]

    window = sg.Window("Misty UI", layout)

    functions_mapping = {
        "TILT_LEFT": lambda: tilt(robot, "left"),
        "TILT_RIGHT": lambda: tilt(robot, "right"),
        "LOOK_UP": lambda: look(robot, "up"),
        "LOOK_DOWN": lambda: look(robot, "down"),
        "LOOK_LEFT": lambda: look(robot, "left"),
        "LOOK_RIGHT": lambda: look(robot, "right"),
        "LOOK_STRAIGHT": lambda: look(robot, "straight"),
        "LED_RED": lambda: led(robot, "red"),
        "LED_GREEN": lambda: led(robot, "green"),
        "LED_BLUE": lambda: led(robot, "blue"),
        "SPEAK": lambda: speak(robot, "placeholder for speak"),
        "CLEAR": lambda: speak(robot, "placeholder for clear")
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
            # TODO implement

        if event == "Clear":
            window["-TTS-"].update("")

    window.close()

if __name__ == "__main__":
    # misty_ip = misty_ip_scan()
    misty_ip = ""
    main(misty_ip)
