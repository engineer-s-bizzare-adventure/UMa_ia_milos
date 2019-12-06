from ev3dev2.motor import OUTPUT_A, OUTPUT_D, MoveDifferential, SpeedRPM
from ev3dev2.wheel import EV3Tire
from ev3dev2.motor import MoveTank
from ev3dev2.motor import MotorSet
from ev3dev2.motor import MoveDifferential

STUD_MM = 9.3
# test with a robot that:
# - uses the standard wheels known as EV3Tire
# - wheels are 16 studs apart
mdiff = MoveDifferential(OUTPUT_A, OUTPUT_D, EV3Tire, 14 * STUD_MM)

SPEEDRPM = 40

def move():
    '''
    tank_drive = MoveTank(OUTPUT_A, OUTPUT_D)
    tank_drive.on_for_rotations(50, 75, 10)
    # drive in a turn for 10 rotations of the outer motor
    '''
    # Enable odometry
    mdiff.odometry_start()

    mdiff.on_to_coordinates(SpeedRPM(SPEEDRPM), 250, 0)
    mdiff.on_to_coordinates(SpeedRPM(SPEEDRPM), 500, 0)
    mdiff.on_to_coordinates(SpeedRPM(SPEEDRPM), 500, 750)
    mdiff.on_to_coordinates(SpeedRPM(SPEEDRPM), 250, 750)
    mdiff.on_to_coordinates(SpeedRPM(SPEEDRPM), 750, 750)
    mdiff.on_to_coordinates(SpeedRPM(SPEEDRPM), 750, 250)

    # Rotate 90 degrees clockwise
    mdiff.turn_right(SpeedRPM(SPEEDRPM), 90)

    # Drive forward 500 mm
    mdiff.on_for_distance(SpeedRPM(SPEEDRPM), 500)

    mdiff.turn_left(SpeedRPM(SPEEDRPM), 90)

    mdiff.on_for_distance(SpeedRPM(SPEEDRPM), 500)

    mdiff.turn_left(SpeedRPM(SPEEDRPM), 90)

    mdiff.on_for_distance(SpeedRPM(SPEEDRPM), 1000)

    # Use odometry to go back to where we started
    mdiff.on_to_coordinates(SpeedRPM(SPEEDRPM), 0, 0)


    # Disable odometry
    mdiff.odometry_stop()
    