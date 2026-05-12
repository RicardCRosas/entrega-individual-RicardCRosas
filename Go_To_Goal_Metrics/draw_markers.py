import rclpy
from rclpy.node import Node
from turtlesim.srv import TeleportAbsolute, SetPen, Spawn, Kill
import time

class MarkerDrawer(Node):
    def __init__(self):
        super().__init__('marker_drawer')
        self.spawn_client = self.create_client(Spawn, '/spawn')
        self.kill_client = self.create_client(Kill, '/kill')
        
        while not self.spawn_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Spawn service not available...')
        while not self.kill_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Kill service not available...')

    def spawn_painter(self):
        req = Spawn.Request()
        req.x = 0.0
        req.y = 0.0
        req.theta = 0.0
        req.name = 'painter'
        future = self.spawn_client.call_async(req)
        rclpy.spin_until_future_complete(self, future)
        return future.result().name

    def kill_painter(self):
        req = Kill.Request()
        req.name = 'painter'
        future = self.kill_client.call_async(req)
        rclpy.spin_until_future_complete(self, future)

    def draw_all(self):
        # Create temporary painter turtle
        try:
            self.spawn_painter()
        except:
            pass # Already exists
            
        # Create clients for the painter's services
        teleport_client = self.create_client(TeleportAbsolute, '/painter/teleport_absolute')
        pen_client = self.create_client(SetPen, '/painter/set_pen')
        
        teleport_client.wait_for_service()
        pen_client.wait_for_service()

        def set_pen(r, g, b, width, off):
            req = SetPen.Request()
            req.r = r; req.g = g; req.b = b; req.width = width; req.off = off
            pen_client.call_async(req)
            time.sleep(0.05)

        def teleport(x, y):
            req = TeleportAbsolute.Request()
            req.x = x; req.y = y; req.theta = 0.0
            teleport_client.call_async(req)
            time.sleep(0.1)

        # Draw Goal X (Red)
        x_goal, y_goal = 8.0, 8.0
        set_pen(255, 0, 0, 5, 1) # Off
        teleport(x_goal - 0.2, y_goal - 0.2)
        set_pen(255, 0, 0, 5, 0) # On
        teleport(x_goal + 0.2, y_goal + 0.2)
        set_pen(255, 0, 0, 5, 1) # Off
        teleport(x_goal - 0.2, y_goal + 0.2)
        set_pen(255, 0, 0, 5, 0) # On
        teleport(x_goal + 0.2, y_goal - 0.2)
        
        # Draw Start Point (Green)
        x_start, y_start = 5.544445, 5.544445
        set_pen(0, 255, 0, 12, 1) # Off
        teleport(x_start, y_start)
        set_pen(0, 255, 0, 12, 0) # On
        teleport(x_start + 0.01, y_start)
        
        set_pen(0, 0, 0, 0, 1) # Off
        
        # Kill the painter so it disappears
        self.kill_painter()

def main():
    rclpy.init()
    node = MarkerDrawer()
    node.draw_all()
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
