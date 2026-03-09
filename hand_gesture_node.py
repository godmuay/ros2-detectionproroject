import rclpy
from rclpy.node import Node

class HandGestureNode(Node):

    def __init__(self):
        super().__init__('hand_gesture_node')
        self.get_logger().info("Hand Gesture Node Started")

def main(args=None):
    rclpy.init(args=args)
    node = HandGestureNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()