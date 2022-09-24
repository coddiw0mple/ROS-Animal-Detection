#!/usr/bin/env python3
import airsim
import sys
import rospy

args = sys.argv
client = airsim.MultirotorClient(ip = args[1])
x, y, z, vel = 0, 0, 0, 5

def mover(l):
    global x, y, z, vel, client
    if l[0] == "down":
        z = z + int(l[1])
        client.moveToPositionAsync(x, y, z, vel).join()
    elif l[0] == "up":
        z = z - int(l[1])
        client.moveToPositionAsync(x, y, z, vel).join()
    elif l[0] == "forward":
        x = x + int(l[1])
        client.moveToPositionAsync(x, y, z, vel).join()
    elif l[0] == "back":
        x = x - int(l[1])
        client.moveToPositionAsync(x, y, z, vel).join()
    elif l[0] == "right":
        y = y + int(l[1])
        client.moveToPositionAsync(x, y, z, vel).join()
    elif l[0] == "left":
        y = y - int(l[1])
        client.moveToPositionAsync(x, y, z, vel).join()
    else:
        print("\n\nWrong format! Please retry\n\n")

def pos():
    global x, y, z, vel, client
    client.moveToPositionAsync(x, y, z, vel).join()

def stop():
    global x, y, z, vel, client
    print("Quitting....")
    x, y, z = 0, 0, 0
    client.goHomeAsync().join()
    client.landAsync().join()
    client.armDisarm(False)
    client.enableApiControl(False)
    print("\nLanded and disconnected successfully!\n")

def main(args):
    global x, y, z, vel, client
    # connect to the AirSim simulator
    client.confirmConnection()
    client.enableApiControl(True)
    client.armDisarm(True)

    # Async methods returns Future. Call join() to wait for task to complete.
    print("TakeOff!")
    rospy.loginfo("takeoff!")
    client.takeoffAsync().join()

    client.moveToPositionAsync(x, y, z, vel).join()

    while True:
        try:
            commands = input("Enter command: ").split(" ")
            if commands[0] == "move":
                mover(commands[1:])
            elif commands[0] == "pos":
                x, y, z = int(commands[1]), int(commands[2]), int(commands[3])
                pos()
            elif commands[0] == "vel":
                vel = commands[1]
            elif commands[0] =="stop":
                stop()
                break
            else:
                print("\n\nWrong command format! Please retry\n\n")
        except:
            print("\n\nWrong command format! Please retry\n\n")


if __name__ == '__main__':
    try:
        main(sys.argv)
    except rospy.ROSInterruptException:
        pass