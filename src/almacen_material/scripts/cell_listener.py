#! /usr/bin/python

import rospy
import math 
from std_msgs.msg import Float64
from std_msgs.msg import Int32
from std_msgs.msg import Bool
from std_msgs.msg import String
from control_msgs.msg import JointControllerState

#        z   x    y
A2UN = [[ 0,  0,  0],
        [15, 33, -28],
        [15, 33,  28],
        [15, 0,   28],
        [30, 33, -28],
        [30, 33,  28],
        [30, 0,  -28],
        [30, 0,   28],
        [45, 33, -28],
        [45, 33,  28],
        [45, 0,  -28],
        [45, 0,   28],
        [90, 0,  -28]]
        
home_cell_id = 0 #Id de la posicion HOME
deliver_cell_index=12 #Id de la 'celda' de entrega
cell_id = home_cell_id #Inicializacion de la variable

treshold= 2.5 #Tolerancia de posicion (REFINAR)

z_pos = 0.0
x_pos = 0.0
y_pos = 0.0

z_error = 0.0
x_error = 0.0
y_error = 0.0

pub1= rospy.Publisher('/vmd_model/joint1_position_controller/command',Float64,queue_size=1)
pub2= rospy.Publisher('/vmd_model/joint2_position_controller/command',Float64,queue_size=1)
pub3= rospy.Publisher('/vmd_model/joint3_position_controller/command',Float64,queue_size=1)
pub_gate = rospy.Publisher('/vmd_model/gate/state',String,queue_size=1)
pub_status = rospy.Publisher('/vmd_model/status',String,latch=True) #latch=Treu garantiz aque el mensaje se mantenga hasta que se cambie

def z_callback(msg):
    global z_pos
    global z_error
    z_pos = msg.process_value
    z_error=msg.error
    
def x_callback(msg):
    global x_pos
    global x_error
    x_pos = msg.process_value
    x_error=msg.error

def y_callback(msg):
    global y_pos
    global y_error
    y_pos = msg.process_value
    y_error=msg.error

#Logica para la compuerta
cell_cmd = False
sdv_pos = False
gate_state = 'closed'
def cell_listener_callback(msg):
    global cell_id
    global cell_cmd
    cell_id= msg.data
    
    cell_cmd=True

def sdv_listener_callback(msg):
    global sdv_pos
    global gate_state
    sdv_pos=msg.data

sub1 = rospy.Subscriber('/vmd_model/joint1_position_controller/state',JointControllerState,z_callback)
sub2 = rospy.Subscriber('/vmd_model/joint2_position_controller/state',JointControllerState,x_callback)
sub3 = rospy.Subscriber('/vmd_model/joint3_position_controller/state',JointControllerState,y_callback)

sub_cell_listener = rospy.Subscriber('/vmd_model/cell_command',Int32,cell_listener_callback)
sub_sdv_listener = rospy.Subscriber('/vmd_model/sdv_pos',Bool,sdv_listener_callback)

def reach(cell_id):

    global A2UN
    global x_error
    global y_error
    global z_error
    global treshold

    z_goal = A2UN[cell_id][0]
    x_goal = A2UN[cell_id][1]
    y_goal = A2UN[cell_id][2] 

    
    pub_status.publish('Cell selected: {0} in Position= x:{1}, y:{2}, z:{3}'.format(cell_id,x_goal,y_goal,z_goal))
    rate=rospy.Rate(10); #10Hz
    
    pub1.publish(Float64(z_goal))
    pub_status.publish('Moving shelf in z axis. ')
    rospy.sleep(1)
    while(abs(z_error)>treshold):
        pub1.publish(Float64(z_goal))
        rate.sleep()
    
    pub2.publish(Float64(x_goal))
    pub_status.publish('Moving shelf in x axis. ')
    rospy.sleep(1)
    while(abs(x_error)>treshold):
        pub2.publish(Float64(x_goal))
        rate.sleep()

    pub3.publish(Float64(y_goal))
    pub_status.publish('Moving shelf in y axis.')
    rospy.sleep(1)    
    while(abs(y_error)>treshold):    
        pub3.publish(Float64(y_goal))
        rate.sleep()

    # move_in_axis(0,cell_id,pub1)
    # move_in_axis(1,cell_id,pub2)
    # move_in_axis(2,cell_id,pub3)

    pub_status.publish('Shelf {0} Reached!'.format(cell_id))

def deliver():
    global A2UN
    global x_error
    global y_error
    global z_error
    global treshold
    global deliver_cell_index

    z_goal = A2UN[deliver_cell_index][0]
    x_goal = A2UN[deliver_cell_index][1]
    y_goal = A2UN[deliver_cell_index][2]

    pub_status.publish('Delivery started')

    rate=rospy.Rate(10); #10Hz
    
    y_neutral=0.0
    pub3.publish(Float64(y_neutral))
    pub_status.publish('Moving shelf in y axis.')
    rospy.sleep(1)    
    while(abs(y_error)>treshold):    
        pub3.publish(Float64(y_neutral))
        rate.sleep()
    
    pub2.publish(Float64(x_goal))
    pub_status.publish('Moving shelf in x axis.')
    rospy.sleep(1)
    while(abs(x_error)>treshold):
        pub2.publish(Float64(x_goal))
        rate.sleep()

    pub1.publish(Float64(z_goal))
    pub_status.publish('Moving shelf in z axis.')
    rospy.sleep(1)
    while(abs(z_error)>treshold):
        pub1.publish(Float64(z_goal))
        rate.sleep()

    pub3.publish(Float64(y_goal))
    pub_status.publish('Moving shelf in y axis.')
    rospy.sleep(1)    
    while(abs(y_error)>treshold):    
        pub3.publish(Float64(y_goal))
        rate.sleep()
    
    pub_status.publish('Delivery Position Reached!')

def home():
    global A2UN
    global x_error
    global y_error
    global z_error
    global treshold
    global home_cell_id
    z_goal = A2UN[home_cell_id][0]
    x_goal = A2UN[home_cell_id][1]
    y_goal = A2UN[home_cell_id][2]

    pub_status.publish('Return to Home started')

    rate=rospy.Rate(10); #10Hz
    
    pub3.publish(Float64(y_goal))
    pub_status.publish('Moving shelf in y axis.')
    rospy.sleep(1)    
    while(abs(y_error)>treshold):    
        pub3.publish(Float64(y_goal))
        rate.sleep()
    
    pub2.publish(Float64(x_goal))
    pub_status.publish('Moving shelf in x axis.')
    rospy.sleep(1)
    while(abs(x_error)>treshold):
        pub2.publish(Float64(x_goal))
        rate.sleep()

    pub1.publish(Float64(z_goal))
    pub_status.publish('Moving shelf in z axis.')
    rospy.sleep(1)
    while(abs(z_error)>treshold):
        pub1.publish(Float64(z_goal))
        rate.sleep()
    
    pub_status.publish('Home Position Reached!')

def open_gate():
    global gate_cmd
    #publish a command to open the gate and then wait for comand to close the gate
def main():
    pub_status.publish('Waiting for command')
    while not rospy.is_shutdown():
        global cell_id
        global cell_cmd
        global sdv_pos
        
        if(cell_cmd):
            reach(cell_id)
            rospy.sleep(1)
            deliver()
            rospy.sleep(1)
            cell_cmd=False
            pub_status.publish('Waiting for SDV...')

        if (sdv_pos and (not cell_cmd)):    
            pub_gate.publish('Open')
            pub_status.publish('Opening gate...')
            #Se esperan 10 segundos simulando la entrega
            rospy.sleep(10)
            pub_gate.publish('Close')
            pub_status.publish('Closing gate...')
            sdv_pos=False
            rospy.sleep(10)
            #vuelta a Home
            home()
            pub_status.publish('Waiting for command')

# def move_in_axis(axis, cell_id, pub):
#     global A2UN
#     global x_error
#     global y_error
#     global z_error
#     global treshold

#     if(axis==0):
#         axis_name = 'z'
#         error= z_error
#     elif(axis==1):
#         axis_name = 'x'
#         error= x_error
#     elif(axis==2):
#         axis_name = 'y'
#         error= y_error    

#     goal = A2UN[cell_id][axis]
    
#     rate=rospy.Rate(10); #10Hz
#     pub.publish(Float64(goal))
#     rospy.sleep(1)
#     pub_status.publish('Moving shelf in {0} axis.'.format(axis_name))
    
#     while(abs(error)>treshold):
#         pub.publish(Float64(goal))
#         rate.sleep()

if __name__ == '__main__':
    try:
        rospy.init_node('cell_listener', anonymous=False)
        main()
    except rospy.ROSInterruptException:
        pass