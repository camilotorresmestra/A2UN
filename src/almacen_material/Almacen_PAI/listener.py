#!/usr/bin/env python
import rospy
import mysql.connector as mariadb
import datetime
from std_msgs.msg import Int16

result =Int16()
send = True
mariadb_connection = mariadb.connect(user='AlmacenUN', password='AlmacenUN', database = "Perfiles")
cursor = mariadb_connection.cursor()
def callback(msg):
    global send
    result.data = msg.data
    rospy.loginfo("msj recibido")
    rospy.loginfo(result)
    send=True

def main():
    global send
    rospy.init_node("nodeN")
    #rospy.loginfo("Inicio")
    pub = rospy.Publisher("chatter", Int16, queue_size=10)
    sub = rospy.Subscriber("response", Int16, callback)
    r = rospy.Rate(1)
    while not rospy.is_shutdown():
    	if send:
		solicitud()
		#send=False 

def solicitud():
	global cursor
	pub1 = rospy.Publisher("chatter", Int16, queue_size=10)
        r = rospy.Rate(1)
	#rospy.loginfo("Realizando conexion")
        #mariadb_connection = mariadb.connect(user='AlmacenUN', password='AlmacenUN', database = "Perfiles")
        #cursor = mariadb_connection.cursor()
        #rospy.loginfo("Conexion realizada")
	perfil = input("Caracteristica dimensional del perfil: ")
        tipo=input("Caracteristica geometrica del perfil: ")
        try:
            cursor.execute('SELECT ubicacion FROM tabla1 WHERE perfil=%s AND tipo=%s',(perfil,tipo))
            for ubicacion  in cursor:
		u=int(ubicacion[0])
		rospy.loginfo("buscando en db")
            	rospy.loginfo("numero enviado")   
	    	rospy.loginfo(u)
	    	pub1.publish(u)
                now = datetime.datetime.now()
                date_time = now.strftime("%m/%d/%Y, %H:%M:%S")
                rospy.loginfo(date_time)
                cursor.execute("INSERT INTO  op(perfil,tipo,fecha) VALUES(%s,%s,%s)",(perfil, tipo,date_time))
                mariadb_connection.commit()
                rospy.loginfo("busqueda finalizada")
        except mariadb.Error as error:
            print("Pieza no disponible, solicitud no realizable")
			


if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass
