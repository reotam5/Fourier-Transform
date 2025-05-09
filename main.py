import pygame
import sys
import math
import numpy as np
from typing import List, Tuple
from svg_to_fourier import parse_svg_to_coordinates, discrete_fourier_transform, image_to_svg

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
CENTER = (WIDTH // 2, HEIGHT // 2)
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

class Needle:
    def __init__(self, amplitude: float, frequency: float, phase: float):
        """
        Initialize a needle with Fourier parameters
        
        Args:
            amplitude: The length of the needle
            frequency: How fast it rotates (in radians per second)
            phase: Initial phase offset (in radians)
        """
        self.amplitude = amplitude
        self.frequency = frequency
        self.phase = phase
    
    def get_position(self, time: float, start_pos: Tuple[float, float]) -> Tuple[float, float]:
        """Calculate the end position of this needle at the given time"""
        angle = self.frequency * time + self.phase
        x = start_pos[0] + self.amplitude * math.cos(angle)
        y = start_pos[1] + self.amplitude * math.sin(angle)
        return (x, y)

class FourierVisualizer:
    def __init__(self):
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Fourier Series Visualization")
        self.clock = pygame.time.Clock()
        
        # List of needles with their Fourier parameters
        self.needles: List[Needle] = []
        
        # Trace of points drawn by the last needle
        self.trace = []
        self.time = 0
        
    def add_needle(self, amplitude: float, frequency: float, phase: float):
        """Add a new needle to the visualization"""
        self.needles.append(Needle(amplitude, frequency, phase))
    
    def clear_needles(self):
        """Remove all needles"""
        self.needles = []
        
    def run(self):
        """Main loop for the visualization"""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            

            # Update
            self.time += 1 / FPS
            
            # Calculate positions of all needles
            positions = [CENTER]
            for needle in self.needles:
                next_pos = needle.get_position(self.time, positions[-1])
                positions.append(next_pos)
            
            # Add the last position to the trace
            if len(positions) > 1:
                self.trace.append(positions[-1])
            
            # Drawing
            self.screen.fill(WHITE)
            
            # Draw needles
            for i in range(len(positions) - 1):
                pygame.draw.line(self.screen, BLACK, positions[i], positions[i+1], 2)
                pygame.draw.circle(self.screen, GRAY, (int(positions[i][0]), int(positions[i][1])), self.needles[i].amplitude, 1)
            
            # Draw the last circle
            if positions:
                pygame.draw.circle(self.screen, BLACK, (int(positions[-1][0]), int(positions[-1][1])), 2)
            

            # Draw trace
            if len(self.trace) > 1:
                pygame.draw.lines(self.screen, GREEN, False, self.trace, 2)
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()
        sys.exit()

def main():
    visualizer = FourierVisualizer()

    # image = "image.png"
    svg = "image.svg"
    # image_to_svg(image, svg)
    # coords = parse_svg_to_coordinates(svg, num_points=10000, max_x=WIDTH - 100, max_y=HEIGHT-100)

    visualizer.clear_needles()
    visualizer.add_needle(
        amplitude=100,
        frequency=2 * math.pi / 60,  # 1 rotation every 60 frames
        phase=0
    )
    visualizer.add_needle(
        amplitude=50,
        frequency=2 * math.pi / 30,  # 1 rotation every 30 frames
        phase=math.pi / 4
    )
    visualizer.add_needle(
        amplitude=25,
        frequency=2 * math.pi / 15,  # 1 rotation every 15 frames
        phase=math.pi / 2
    )
    # fourier_coeffs = discrete_fourier_transform(coords)
    # for i, (amplitude, frequency, phase) in enumerate(fourier_coeffs):
    #     visualizer.add_needle(amplitude, frequency, phase)

    visualizer.run()

if __name__ == "__main__":
    main()