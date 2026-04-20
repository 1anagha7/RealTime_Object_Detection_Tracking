import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import Twist
from cv_bridge import CvBridge
import cv2
import numpy as np
import time


class ObjectDetector(Node):

    def __init__(self):
        super().__init__('object_detector')

        self.subscription = self.create_subscription(
            Image,
            '/camera/image_raw',
            self.listener_callback,
            10
        )

        self.cmd_pub = self.create_publisher(Twist, '/cmd_vel', 10)

        self.bridge = CvBridge()

        self.prev_x = None
        self.prev_time = None

        cv2.namedWindow("Detection + Tracking", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Detection + Tracking", 1200, 900)


    def listener_callback(self, msg):
        frame = self.bridge.imgmsg_to_cv2(msg, 'bgr8')

        height, width, _ = frame.shape
        frame_center = width // 2

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        red_lower = np.array([0, 120, 70])
        red_upper = np.array([10, 255, 255])

        green_lower = np.array([40, 40, 40])
        green_upper = np.array([80, 255, 255])

        blue_lower = np.array([100, 150, 0])
        blue_upper = np.array([140, 255, 255])

        red_mask = cv2.inRange(hsv, red_lower, red_upper)
        green_mask = cv2.inRange(hsv, green_lower, green_upper)
        blue_mask = cv2.inRange(hsv, blue_lower, blue_upper)

        detections = [
            (red_mask, "Red Object"),
            (green_mask, "Green Object"),
            (blue_mask, "Blue Object")
        ]

        best_cx = None
        best_area = 0

        for mask, label in detections:
            contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            if contours:
                largest = max(contours, key=cv2.contourArea)
                area = cv2.contourArea(largest)

                if area > 500:
                    x, y, w, h = cv2.boundingRect(largest)

                    cx = x + w // 2
                    cy = y + h // 2

                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0,255,0), 2)
                    cv2.putText(frame, label, (x, y-10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0,255,0), 2)

                    cv2.circle(frame, (cx, cy), 5, (0,0,255), -1)

                  
                    cv2.line(frame, (cx, cy), (frame_center, cy), (0,255,255), 2)

                    current_time = time.time()
                    if self.prev_x is not None:
                        dx = cx - self.prev_x
                        dt = current_time - self.prev_time
                        if dt > 0:
                            speed = dx / dt
                            cv2.putText(frame,
                                f"Speed: {int(speed)} px/s",
                                (x, y-30),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                0.6,
                                (255,0,0), 2)

                    self.prev_x = cx
                    self.prev_time = current_time

                    if area > best_area:
                        best_area = area
                        best_cx = cx

        if best_cx is not None:
            error = best_cx - frame_center

            twist = Twist()
            twist.angular.z = -0.002 * error

            if abs(error) < 50:
                twist.linear.x = 0.15

            self.cmd_pub.publish(twist)
        else:
            self.cmd_pub.publish(Twist())

        cv2.line(frame, (frame_center, 0), (frame_center, height), (255,255,0), 2)

        cv2.imshow("Detection + Tracking", frame)
        cv2.waitKey(1)


def main():
    rclpy.init()
    node = ObjectDetector()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
