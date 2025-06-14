import pygame
import numpy as np
from app.config import FFT_BINS

class Visualizer:
    def __init__(self):
        pygame.init()
        self.width = 1024  # Wider window for better resolution
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("VibeScope FFT Analyzer")
        self.clock = pygame.time.Clock()
        self.bar_width = max(2, self.width // FFT_BINS)  # Minimum 2px width

    def draw(self, fft_data):
        # Clear screen
        self.screen.fill((0, 0, 20))

        # Apply logarithmic scaling for better visualization
        fft_data = np.log10(np.clip(fft_data, 1e-10, None))
        fft_data = (fft_data - np.min(fft_data)) / (np.max(fft_data) - np.min(fft_data))

        # Draw frequency bars
        for i, magnitude in enumerate(fft_data[:FFT_BINS]):
            # Calculate dimensions
            bar_height = int(magnitude * self.height * 0.9)
            x = i * self.bar_width
            y = self.height - bar_height

            # Color gradient: blue -> green -> red
            color = self.get_color(magnitude)
            
            # Draw bar with 1px spacing
            pygame.draw.rect(
                self.screen,
                color,
                (x, y, self.bar_width - 1, bar_height)
            )

        pygame.display.flip()

    def get_color(self, magnitude):
        """Generate color gradient based on magnitude"""
        return (
            int(255 * magnitude),  # Red
            int(255 * (1 - abs(magnitude - 0.5))),  # Green peaks at 0.5
            int(255 * (1 - magnitude))  # Blue
        )