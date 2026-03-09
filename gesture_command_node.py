import rclpy
from rclpy.node import Node
from std_msgs.msg import String

class GestureCommand(Node):

    def __init__(self):
        super().__init__('gesture_command_node')

        self.publisher = self.create_publisher(String,'gesture_cmd',10)

        self.get_logger().info("Gesture Command Node Started")

        self.timer = self.create_timer(0.5,self.loop)

    def loop(self):

        cmd = input("Command (w/s/a/d/q/e): ")

        msg = String()

        if cmd == 'w':
            msg.data = "forward"

        elif cmd == 's':
            msg.data = "backward"

        elif cmd == 'a':
            msg.data = "left"

        elif cmd == 'd':
            msg.data = "right"

        elif cmd == 'q':
            msg.data = "rotate_left"

        elif cmd == 'e':
            msg.data = "rotate_right"

        else:
            msg.data = "stop"

        self.publisher.publish(msg)

        self.get_logger().info("Send: %s" % msg.data)

def main(args=None):

    rclpy.init(args=args)

    node = GestureCommand()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()

if __name__ == '__main__':
    main()