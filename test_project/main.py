
'''
This code didnot work as expected because it is too slow 
Problem:

Your UI responds slowly when pressing the move buttons because:

    You're using subprocess.call() to invoke ros2 topic pub, which is slow to start every time.

    You are sourcing the ROS setup file with every command.

    The command runs synchronously on the main GUI thread, blocking PyQt’s event loop briefly.

Solution :
 BUild the project in ros2 workspace     

import sys
import subprocess 
from utils import Ui_MainWindow    
from PyQt5.QtWidgets import QApplication,QMainWindow


class MainWindow(QMainWindow,Ui_MainWindow):
    def __init__(self):
        super(MainWindow,self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Turtlebot Control Interface")
        
        #connecting the menu buttons
        self.drive.clicked.connect(lambda : self.stackedWidget.setCurrentIndex(0))
        self.config.clicked.connect(lambda : self.stackedWidget.setCurrentIndex(1))

        #launching turtlesim
        self.launch_turtlesim()

        #move turtle right
        self.right.clicked.connect(self.move_right)
        self.left.clicked.connect(self.move_left)

        

    def launch_turtlesim(self):
        cmd = "export QT_QPA_PLATFORM=wayland; source /opt/ros/jazzy/setup.bash && ros2 run turtlesim turtlesim_node"
        subprocess.Popen([
        'gnome-terminal', '--', 'bash', '-c', f'{cmd}; exec bash'])
 
    
    def move_right(self):
        cmd = 'source /opt/ros/jazzy/setup.bash && timeout 1 ros2 topic pub -r 10 /turtle1/cmd_vel geometry_msgs/msg/Twist \
          "{linear: {x: 2.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}"'
    
        subprocess.call(['bash', '-c', cmd], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    def move_left(self):
        cmd = 'timeout 1 ros2 topic pub -r 10 /turtle1/cmd_vel geometry_msgs/msg/Twist \
              "{linear: {x: -1.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 0.0}}"'
        subprocess.call(['bash', '-c', cmd], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        

def main(args=None):
    
    app=QApplication(sys.argv)
    window=MainWindow()
    window.show()

    app.exec_()

if __name__== '__main__' :
    main()               

'''