#!/usr/bin/env python

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from nav_msgs.msg import Odometry


global x, y, w
x = 0
y = 0
w = 0

def callback(msg):
    print msg.pose.pose

def get_current_position(msg):
    global x, y, w
    x = msg.pose.pose.position.x
    y = msg.pose.pose.position.y
    w = msg.pose.pose.orientation.w
    # print("?")
    # print('in function' ,  x, y, w)
    return x, y, w



def movebase_client(x_goal, y_goal):
    global x, y, w
    # rospy.init_node('check_odometry')
    # odom_sub = rospy.Subscriber('/odom', Odometry, callback)
    # rospy.spin()
    
    # print( x, y, w)
    # print( x, y, w)
    # while not rospy.is_shutdown():
    #     print( x, y, w)

    x_move = x_goal - x
    y_move = y_goal - y

    print(x_move, y_move)


    client = actionlib.SimpleActionClient('move_base',MoveBaseAction)
    client.wait_for_server()

    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "odom"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = x_move
    goal.target_pose.pose.position.y = y_move
    goal.target_pose.pose.orientation.w = 1.0

    client.send_goal(goal)
    wait = client.wait_for_result()
    if not wait:
        rospy.logerr("Action server not available!")
        rospy.signal_shutdown("Action server not available!")
    else:
        return client.get_result()

if __name__ == '__main__':
    try:
        rospy.init_node('move_to_fixed_pose')
        odom_sub = rospy.Subscriber('/odom', Odometry, get_current_position)
        rospy.sleep(0.5)
        print(x, y,w)
        result = movebase_client(0, 0)
        if result:
            rospy.loginfo("Goal execution done!")
            odom_sub = rospy.Subscriber('/odom', Odometry, get_current_position)
            rospy.sleep(0.5)
            print(x, y,w)
    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation test finished.")