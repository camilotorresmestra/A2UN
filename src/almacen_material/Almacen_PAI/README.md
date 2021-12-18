# Package ROS para el funcionamiento del almacen automatizado LabFabEx 2018-III

Los archivos presentes hacen parte de un paquete nombrado Own_nodes en ROS Kinetic


A continuación podrán encontrar las instrucciones para instalar las
dependencias necesarias para el funcionamiento del almacen. Recordar que debe ser instalado
sobre Raspbian Stretch 9.

1. Habilitar interfas ssh

2. Instalar ROS kinetic 
      de acuerto a las instrucciones brindadas en http://wiki.ros.org/ROSberryPi/Installing%20ROS%20Kinetic%20on%20the%20Raspberry%20Pi
      
3. Instalar rosserial-arduino
    sudo apt-get install ros-kinetic-rosserial-arduino 
    siguiendo las instrucciones de http://wiki.ros.org/rosserial_arduino/Tutorials/Arduino%20IDE%20Setup
    
4. Instalar gestor de bases de datos
     sudo apt install mariadb-server
     https://linuxize.com/post/how-to-install-mariadb-on-ubuntu-18-04/
     
     
     
