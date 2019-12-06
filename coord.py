from ev3dev2.motor import OUTPUT_A, OUTPUT_D, MoveDifferential, SpeedRPM
from ev3dev2.wheel import EV3Tire
from ev3dev2.motor import MoveTank
from ev3dev2.motor import MotorSet
from ev3dev2.motor import MoveDifferential

STUD_MM = 8
# test with a robot that:
# - uses the standard wheels known as EV3Tire
# - wheels are 16 studs apart
mdiff = MoveDifferential(OUTPUT_A, OUTPUT_D, EV3Tire, 16 * STUD_MM)

def move():
    '''
    tank_drive = MoveTank(OUTPUT_A, OUTPUT_D)
    tank_drive.on_for_rotations(50, 75, 10)
    # drive in a turn for 10 rotations of the outer motor
    '''

    # Rotate 90 degrees clockwise
    mdiff.turn_right(SpeedRPM(40), 90)

    # Drive forward 500 mm
    mdiff.on_for_distance(SpeedRPM(40), 500)

    # Drive in arc to the right along an imaginary circle of radius 150 mm.
    # Drive for 700 mm around this imaginary circle.
    mdiff.on_arc_right(SpeedRPM(80), 150, 700)

    # Enable odometry
    mdiff.odometry_start()

    # Use odometry to drive to specific coordinates
    mdiff.on_to_coordinates(SpeedRPM(40), 300, 300)

    # Use odometry to go back to where we started
    mdiff.on_to_coordinates(SpeedRPM(40), 0, 0)

    # Use odometry to rotate in place to 90 degrees
    mdiff.turn_to_angle(SpeedRPM(40), 90)

    # Disable odometry
    mdiff.odometry_stop()
    