from example_interfaces.srv import AddTwoInts
import sys
import rclpy
from rclpy.node import Node


class MinimalClientAsync(Node):
    def __init__(self):
        super().__init__('minimal_client_async')
        self.cli = self.create_client(AddTwoInts, 'add_two_ints')

    def send_request(self, a, b):
        while not self.cli.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Service not available, waiting again...')

        request = AddTwoInts.Request()
        request.a = a
        request.b = b
        self.future = self.cli.call_async(request)
        rclpy.spin_until_future_complete(self, self.future)
        return self.future.result()


def main(args=None):
    rclpy.init(args=args)

    minimal_client = MinimalClientAsync()
    future = minimal_client.send_request(int(sys.argv[1]), int(sys.argv[2]))
    response = future
    minimal_client.get_logger().info(f'Result of add_two_ints: {response.sum}')

    minimal_client.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()