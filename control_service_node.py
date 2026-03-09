import rclpy
from rclpy.node import Node
from std_srvs.srv import SetBool

class ControlService(Node):

    def __init__(self):

        super().__init__('control_service_node')

        self.manual_enabled = True

        self.service = self.create_service(
            SetBool,
            'enable_manual_control',
            self.callback
        )

        self.get_logger().info("Control Service Ready")

    def callback(self, request, response):

        self.manual_enabled = request.data

        if self.manual_enabled:
            self.get_logger().info("Manual control ENABLED")
        else:
            self.get_logger().info("Manual control DISABLED")

        response.success = True
        response.message = "Manual control updated"

        return response


def main(args=None):

    rclpy.init(args=args)

    node = ControlService()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()