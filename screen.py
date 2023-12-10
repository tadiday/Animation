import pygame
import numpy as np
from pygame import surfarray
from PIL import Image
pygame.init()

class Screen:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
    
    def ratio(self) -> float:
        return self.width / self.height

    def draw(self, buffer):
        if buffer.shape != (self.width, self.height, 3):
            raise ValueError("Wrong Shape")
        else:
            #flip the buffer up side down
            buffer = np.flipud(buffer)
            #create a new py game display and display the buffer
            screen = pygame.display.set_mode([self.width, self.height])
            pygame.pixelcopy.array_to_surface(screen, buffer)
            pygame.display.flip()

    def show(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

    def device_to_screen(self,point):
        # Assuming p where x and y are in device space [0, 1]
        x = int((point[0] + 1) * 0.5 * self.width)
        # since why start from the top in pygame, we do 1 - point[1] to get the normal coordinates
        y = int((1 - point[1]) * 0.5 * self.height)
        return x, y, point[2]

