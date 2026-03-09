import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from geometry_msgs.msg import Twist

class MotionControl(Node):

    def __init__(self):

        super().__init__('motion_control_node')

        self.subscription = self.create_subscription(
            String,
            'gesture_cmd',
            self.callback,
            10)

        self.publisher = self.create_publisher(
            Twist,
            'cmd_vel',
            10)

        self.get_logger().info("Motion Control Node Started")

    def callback(self,msg):

        twist = Twist()

        if msg.data == "forward":
            twist.linear.x = 0.3

        elif msg.data == "backward":
            twist.linear.x = -0.3

        elif msg.data == "left":
            twist.linear.y = 0.3

        elif msg.data == "right":
            twist.linear.y = -0.3

        elif msg.data == "rotate_left":
            twist.angular.z = 0.5

        elif msg.data == "rotate_right":
            twist.angular.z = -0.5

        else:
            twist.linear.x = 0.0
            twist.angular.z = 0.0

        self.publisher.publish(twist)

        self.get_logger().info("cmd_vel sent")


def main(args=None):

    rclpy.init(args=args)

    node = MotionControl()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()

if __name__ == '__main__':
    main()