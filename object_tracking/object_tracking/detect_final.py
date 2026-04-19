import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import numpy as np


class DetectionNode(Node):
    def __init__(self):
        super().__init__('detection_node')

        self.bridge = CvBridge()

        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.callback,
            10
        )

    def callback(self, msg):
        frame = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Define colors
        colors = {
            "RED": ([0, 120, 70], [10, 255, 255], (0, 0, 255)),
            "GREEN": ([40, 40, 40], [70, 255, 255], (0, 255, 0)),
            "BLUE": ([100, 150, 0], [140, 255, 255], (255, 0, 0))
        }

        obj_id = 0

        for name, (lower, upper, color) in colors.items():
            lower = np.array(lower)
            upper = np.array(upper)

            mask = cv2.inRange(hsv, lower, upper)
            contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            for cnt in contours:
                area = cv2.contourArea(cnt)

                if area > 500:
                    x, y, w, h = cv2.boundingRect(cnt)

                    obj_id += 1

                    # Draw bounding box
                    cv2.rectangle(frame, (x, y), (x + w, y + h), color, 2)

                    # Label with ID
                    cv2.putText(frame,
                                f"{name} ID:{obj_id}",
                                (x, y - 10),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.7,
                                color,
                                2)

        cv2.namedWindow("Detection", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Detection", 1000, 800)
        cv2.imshow("Detection", frame)
        cv2.waitKey(1)


def main(args=None):
    rclpy.init(args=args)
    node = DetectionNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
