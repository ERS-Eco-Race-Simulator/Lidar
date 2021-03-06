from rplidar import RPLidar
import pygame
import math
import time
import yaml
from sys import argv

surface = pygame.display.set_mode((1000, 1000))
config = yaml.load(open(argv[1]), Loader=yaml.FullLoader)

def draw(points):
    surface.fill((0, 0, 0))
    for (x, y) in points:
        surface.set_at((int(x) + 500, int(y) + 500), (255, 255, 255))
    pygame.display.update()

def run():

    lidar = RPLidar(config['lidar']['port'])
    pygame.init()

    points = [ (0, 0) for i in range(361) ]
    k = 0

    try:
        print('Initializing')
        time.sleep(5)
        print('Recording data')
        for new, quality, theta, r in lidar.iter_measurments(max_buf_meas = 800):
            x = (math.cos(math.radians(theta / math.pi) * math.pi) * r) / int(config['scale'])
            y = (math.sin(math.radians(theta / math.pi) * math.pi) * r) / int(config['scale'])
            points[int(theta * 1)] = (x, y)
            k += 1
            if k > 100:
                k = 0
                draw(points)

    except KeyboardInterrupt:
        print('Stopping')

    lidar.stop()
    lidar.stop_motor()
    lidar.disconnect()

if __name__ == "__main__":
    run()