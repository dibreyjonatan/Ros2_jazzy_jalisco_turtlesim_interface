import sys
import random
import subprocess
import logging
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtCore import QTimer

from .utils import Ui_MainWindow
import rclpy
from rclpy.node import Node
from turtlesim.srv import TeleportRelative
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose

#logging configurations
logging.basicConfig(level=logging.NOTSET)
logger=logging.getLogger()
logger.setLevel(logging.DEBUG)

class TurtlePublisher(Node):
    def __init__(self,name_turtlesim):
        super().__init__(f'{name_turtlesim}_publisher')
        #so that the name of the node of every turtle added is unique
        self.publisher = self.create_publisher(Twist, f'/{name_turtlesim}/cmd_vel', 10)
        self.teleport_client = self.create_client(TeleportRelative, f'/{name_turtlesim}/teleport_relative')
       
        
    def publish_velocity(self, linear_x=0.0, angular_z=0.0):
        msg = Twist()
        msg.linear.x = linear_x
        msg.angular.z = angular_z
        self.publisher.publish(msg)

    def call_rotate(self, angular_z):
        # Prepare the service request to teleport (rotate) the turtle
        request = TeleportRelative.Request()
        request.linear = 0.0  # Linear movement is zero, just rotating
        request.angular = angular_z

        # Call the service in an asynchronous manner 
        self.teleport_client.call_async(request)

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.setWindowTitle("Turtlebot Control Interface")

        self.turtle_name="turtle1"
        self.turtle_pub = TurtlePublisher(self.turtle_name)
        self.id=1
        
        self.drive.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(0))
        self.config.clicked.connect(lambda: self.stackedWidget.setCurrentIndex(1))
      
        self.launch_turtlesim()

        self.right.clicked.connect(self.move_right)
        self.left.clicked.connect(self.move_left)

        # Add buttons to rotate
        self.up.clicked.connect(self.rotate_clockwise)
        self.down.clicked.connect(self.rotate_anticlockwise)
        #circle motion
        self.circle.clicked.connect(self.circle_motion)
        #connect kill,clear, and spawn 
        self.clear.clicked.connect(self.clear_simulation)
        self.add_turtle.clicked.connect(self.spawn_turtle)
        self.kill_turtle.clicked.connect(self.kill_turtlesim)
        #for selecting turtle
        self.comboBox.addItem("turtle1")
        self.comboBox.currentTextChanged.connect(self.combobox_changed)
        #connecting background buttons 
        self.r_button.clicked.connect(self.change_red)
        self.b_button.clicked.connect(self.change_blue)
        self.g_button.clicked.connect(self.change_green)

        #getting informations of speed of Turtlesim
        self.sub_node=Node("subscriber_node")
        self.subscriber=self.sub_node.create_subscription(Pose,f'/{self.turtle_name}/pose',self.pose_callbox,10)

        self.time=QTimer()
        self.time.timeout.connect(lambda : rclpy.spin_once(self.sub_node,timeout_sec=1))
        self.time.setInterval(10)
        self.time.start()

    def pose_callbox(self,msg):
        self.data.setText(f"[{self.turtle_name}] Linear Velocity: {msg.linear_velocity}, Angular Velocity: {msg.angular_velocity}")    

    def combobox_changed(self):
        self.turtle_name=self.comboBox.currentText()
        self.subscriber=self.sub_node.create_subscription(Pose,f'/{self.turtle_name}/pose',self.pose_callbox,10)

        self.turtle_pub=TurtlePublisher(self.turtle_name)
       
    def launch_turtlesim(self):
        cmd = "source /opt/ros/jazzy/setup.bash && ros2 run turtlesim turtlesim_node"
        subprocess.Popen(['gnome-terminal', '--', 'bash', '-c', cmd])

    def move_right(self):
        self.turtle_pub.publish_velocity(linear_x=2.0)

    def move_left(self):
        self.turtle_pub.publish_velocity(linear_x=-2.0)

    def circle_motion(self):
        self.turtle_pub.publish_velocity(linear_x=2.0,angular_z=2.0)  # 180 degrees rotation
    

    def rotate_clockwise(self):
        self.turtle_pub.call_rotate(1.5708)  # 90 degrees clockwise

    def rotate_anticlockwise(self):
        self.turtle_pub.call_rotate(-1.5708)  # 90 degrees counterclockwise

    def clear_simulation(self):
        cmd="ros2 service call /clear std_srvs/srv/Empty"
        subprocess.call(['bash', '-c', cmd], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def spawn_turtle(self):
        self.id += 1
        turtle_name = f"turtle{self.id}"
        x_pos = random.uniform(1.0, 10.0)
        y_pos = random.uniform(1.0, 10.0)

        self.comboBox.addItem(turtle_name)
        
        # Source ROS setup and call spawn service
        cmd = (
            f'ros2 service call /spawn turtlesim/srv/Spawn '
            f'"{{x: {x_pos:.2f}, y: {y_pos:.2f}, theta: 0.0, name: \\"{turtle_name}\\"}}"'
        )
        subprocess.call(['bash', '-c', cmd])


    def kill_turtlesim(self):
        # Get selected turtle name from comboBox
        turtle_name = self.comboBox.currentText()
        index=self.comboBox.currentIndex()
        self.comboBox.removeItem(index)  
        if not turtle_name:
            logger.warning("No turtle selected to kill.")
            return

        cmd = (
           
            f'ros2 service call /kill turtlesim/srv/Kill '
            f'"{{name: \\"{turtle_name}\\"}}"'
        )
        subprocess.call(['bash', '-c', cmd])
         
    def change_red(self):
        try:
            red_value=int(self.r_lineEdit.text())
            cmd=f'ros2 param set /turtlesim background_r {str(red_value)}'
            subprocess.call(['bash', '-c', cmd])
        except :
            logger.info("Enter integers not words")
    def change_blue(self):
        try:
            blue_value=int(self.b_lineEdit.text())
            cmd=f'ros2 param set /turtlesim background_b {str(blue_value)}'
            subprocess.call(['bash', '-c', cmd])
        except :
            logger.info("Enter integers not words")   
    def change_green(self):
        try:
            green_value=int(self.g_lineEdit.text())
            cmd=f'ros2 param set /turtlesim background_g {str(green_value)}'
            subprocess.call(['bash', '-c', cmd])     
        except :
            logger.info("Enter integers not words")      

def main():
    rclpy.init()
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.aboutToQuit.connect(lambda : rclpy.shutdown())
    app.exec_()

if __name__ == '__main__':
    main()
