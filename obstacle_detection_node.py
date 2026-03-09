import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import math


class ObstacleDetection(Node):

    def __init__(self):

        super().__init__('obstacle_detection_node')

        self.subscription = self.create_subscription(
            LaserScan,
            'scan',
            self.callback,
            10)

        self.publisher = self.create_publisher(
            Twist,
            'cmd_vel',
            10)

        self.get_logger().info("Obstacle Detection Node Started")

    def callback(self, msg):

        # กรองค่าที่เป็น inf หรือ nan ออกจาก LiDAR
        valid_ranges = [
            r for r in msg.ranges
            if not math.isinf(r) and not math.isnan(r) and r > 0
        ]

        # ถ้าไม่มีข้อมูลเลยให้ข้าม
        if len(valid_ranges) == 0:
            return

        min_distance = min(valid_ranges)

        # หา index ของระยะที่ใกล้ที่สุดในข้อมูลเดิม
        index = msg.ranges.index(min_distance)

        angle = msg.angle_min + index * msg.angle_increment

        distance_mm = min_distance * 1000

        if distance_mm < 150:

            self.get_logger().warn(
                f"Obstacle detected {distance_mm:.1f} mm at {math.degrees(angle):.1f} deg"
            )

        if distance_mm < 120:

            twist = Twist()
            twist.linear.x = -0.2
            twist.angular.z = 0.0

            self.publisher.publish(twist)

            self.get_logger().warn("Too close! Moving away")


def main(args=None):

    rclpy.init(args=args)

    node = ObstacleDetection()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()