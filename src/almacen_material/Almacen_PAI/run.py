#!/usr/bin/python
from listener import listener
import rospy

try:
         ros_node = listener()
         rate=rospy.Rate(10)
         while not rospy.is_shutdown:
               connections = ros_node.get_num_connections()
               rospy.loginfo('Connections: %d',connections)
               if connections > 0:
                     ros_node.solicitud()
                     rospy.loginfo('Publicado')
                     break
               rate.sleep(5)
except rospy.ROSInterruptException, e:
          raise e
