import time
import argparse

parser = argparse.ArgumentParser(description="This is a script tells Wall-E the robot to move and records his position")
parser.add_argument("-i", "--instructions", nargs="+", help="provide a list of instructions. example: begin up left down right stop", required=True)
args = parser.parse_args()

moves = args.instructions


def robot(move):
    command_count = len(move)

    instructions = ["begin", "right", "left", "up", "down", "stop"]

    posUp = 0
    posDown = 0
    posLeft = 0
    posRight = 0
    
    
    for i in range(0, command_count):
        if (move[i].lower() not in instructions):
                print(f"The robot is confused {move[i]} is not a valid command! please re-enter commands that look like this: {instructions}")
                break
        else:

            if (move[i].lower() == "begin"):
                posUp = posDown = posLeft = posRight = 0
                print(f"The robot is starting from the begining position {posRight-posLeft,posUp-posDown}")
            elif (move[i].lower() == "right"):
                posRight +=1
                print(f"The robot moved right one step, current positon is: {posRight-posLeft,posUp-posDown}")
                time.sleep(.5)
            elif (move[i].lower() == "left"):
                posLeft +=1
                print(f"The robot moved left one step current positon is: {posRight-posLeft,posUp-posDown}")
                time.sleep(.5)
            elif (move[i].lower() == "up"):
                posUp +=1
                print(f"The robot moved up one step, current positon is: {posRight-posLeft,posUp-posDown}")
                time.sleep(.5)
            elif (move[i].lower() == "down"):
                posDown +=1
                print(f"The robot moved down one step, current positon is: {posRight-posLeft,posUp-posDown}")
                time.sleep(.5)
            elif (move[i].lower()== "stop"):
                print(f"The robot has stopped! current positon is: {posRight-posLeft,posUp-posDown}")
                break


if __name__ == "__main__":
    robot(moves)