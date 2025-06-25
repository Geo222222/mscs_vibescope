import pygame
import numpy as np
from config.config import FFT_BINS

class Visualizer:
    def __init__(self):
        pygame.init()
        self.width = 1024  # Wider window for better resolution
        self.height = 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("VibeScope FFT Analyzer - Mood Visualization")
        self.clock = pygame.time.Clock()
        self.bar_width = max(2, self.width // FFT_BINS)  # Minimum 2px width
        self.current_mood = "Neutral"
        
        # Define mood color schemes
        self.mood_colors = {
            # Volume Strategy Moods
            "Calm": {
                "background": (5, 10, 30),      # Deep blue background
                "primary": (100, 150, 255),     # Soft blue
                "secondary": (150, 200, 255),   # Light blue
                "accent": (200, 220, 255)       # Very light blue
            },
            "Chill": {
                "background": (10, 20, 15),     # Dark green background
                "primary": (100, 255, 150),     # Green
                "secondary": (150, 255, 200),   # Light green
                "accent": (200, 255, 220)       # Very light green
            },
            "Hype": {
                "background": (30, 5, 5),       # Dark red background
                "primary": (255, 100, 100),     # Red
                "secondary": (255, 150, 100),   # Orange-red
                "accent": (255, 200, 100)       # Yellow-orange
            },
            
            # Frequency Strategy Moods
            "Mellow": {
                "background": (20, 10, 30),     # Purple background
                "primary": (180, 100, 255),     # Purple
                "secondary": (200, 150, 255),   # Light purple
                "accent": (220, 200, 255)       # Very light purple
            },
            "Balanced": {
                "background": (15, 15, 15),     # Neutral gray background
                "primary": (200, 200, 200),     # Gray
                "secondary": (220, 220, 220),   # Light gray
                "accent": (240, 240, 240)       # Very light gray
            },
            "Energetic": {
                "background": (30, 25, 5),      # Golden background
                "primary": (255, 200, 50),      # Gold
                "secondary": (255, 220, 100),   # Light gold
                "accent": (255, 240, 150)       # Very light gold
            },
            
            # Spectral Strategy Moods
            "Bright": {
                "background": (25, 25, 5),      # Bright yellow background
                "primary": (255, 255, 100),     # Bright yellow
                "secondary": (255, 255, 150),   # Light yellow
                "accent": (255, 255, 200)       # Very light yellow
            },
            "Deep": {
                "background": (5, 5, 25),       # Deep blue background
                "primary": (50, 50, 200),       # Deep blue
                "secondary": (100, 100, 220),   # Medium blue
                "accent": (150, 150, 240)       # Light blue
            },
            "Dynamic": {
                "background": (25, 5, 25),      # Magenta background
                "primary": (255, 50, 255),      # Magenta
                "secondary": (255, 100, 255),   # Light magenta
                "accent": (255, 150, 255)       # Very light magenta
            },
            "Intense": {
                "background": (25, 0, 0),       # Dark red background
                "primary": (200, 0, 0),         # Dark red
                "secondary": (255, 50, 50),     # Red
                "accent": (255, 100, 100)       # Light red
            },
            "Chaotic": {
                "background": (20, 20, 20),     # Dark background
                "primary": (255, 0, 128),       # Hot pink
                "secondary": (255, 128, 0),     # Orange
                "accent": (128, 255, 0)         # Lime green
            },
            "Evolving": {
                "background": (15, 25, 20),     # Teal background
                "primary": (0, 255, 200),       # Cyan
                "secondary": (100, 255, 220),   # Light cyan
                "accent": (150, 255, 235)       # Very light cyan
            },
            "Steady": {
                "background": (20, 15, 10),     # Brown background
                "primary": (200, 150, 100),     # Brown
                "secondary": (220, 180, 140),   # Light brown
                "accent": (240, 210, 180)       # Very light brown
            },
            "Neutral": {
                "background": (0, 0, 20),       # Default background
                "primary": (100, 100, 255),     # Default blue
                "secondary": (150, 150, 255),   # Light blue
                "accent": (200, 200, 255)       # Very light blue
            }
        }

    def draw(self, fft_data, mood="Neutral"):
        """Draw the frequency spectrum with mood-based coloring.
        
        Args:
            fft_data: FFT magnitude data to visualize
            mood: Current detected mood for color scheme selection
        """
        # Update current mood
        self.current_mood = mood
        
        # Get color scheme for current mood
        colors = self.mood_colors.get(mood, self.mood_colors["Neutral"])
        
        # Clear screen with mood-appropriate background
        self.screen.fill(colors["background"])

        # Apply logarithmic scaling for better visualization
        fft_data = np.log10(np.clip(fft_data, 1e-10, None))
        if np.max(fft_data) != np.min(fft_data):  # Avoid division by zero
            fft_data = (fft_data - np.min(fft_data)) / (np.max(fft_data) - np.min(fft_data))
        
        # Draw mood indicator text
        self.draw_mood_indicator(mood)

        # Draw frequency bars with mood-based colors
        for i, magnitude in enumerate(fft_data[:FFT_BINS]):
            # Calculate dimensions
            bar_height = int(magnitude * self.height * 0.85)  # Leave space for mood text
            x = i * self.bar_width
            y = self.height - bar_height

            # Get mood-appropriate color for this magnitude
            color = self.get_mood_color(magnitude, colors)
            
            # Draw bar with 1px spacing
            pygame.draw.rect(
                self.screen,
                color,
                (x, y, self.bar_width - 1, bar_height)
            )

        pygame.display.flip()
    
    def draw_mood_indicator(self, mood):
        """Draw mood indicator text on screen."""
        font = pygame.font.Font(None, 36)
        text_color = (255, 255, 255)  # White text
        
        # Main mood text
        mood_text = font.render(f"Mood: {mood}", True, text_color)
        self.screen.blit(mood_text, (10, 10))
        
        # Strategy indicator (smaller font)
        small_font = pygame.font.Font(None, 24)
        strategy_text = small_font.render("Press V/F/S to change strategy", True, (200, 200, 200))
        self.screen.blit(strategy_text, (10, 50))

    def get_mood_color(self, magnitude, color_scheme):
        """Generate color based on magnitude and current mood scheme.
        
        Args:
            magnitude: Frequency magnitude (0.0 to 1.0)
            color_scheme: Color scheme dictionary for current mood
            
        Returns:
            RGB color tuple based on magnitude and mood
        """
        # Interpolate between colors based on magnitude
        if magnitude < 0.33:
            # Low magnitude: blend background and primary
            factor = magnitude * 3  # Scale 0-0.33 to 0-1
            return self.interpolate_color(color_scheme["background"], color_scheme["primary"], factor)
        elif magnitude < 0.66:
            # Medium magnitude: blend primary and secondary
            factor = (magnitude - 0.33) * 3  # Scale 0.33-0.66 to 0-1
            return self.interpolate_color(color_scheme["primary"], color_scheme["secondary"], factor)
        else:
            # High magnitude: blend secondary and accent
            factor = (magnitude - 0.66) * 3  # Scale 0.66-1.0 to 0-1
            return self.interpolate_color(color_scheme["secondary"], color_scheme["accent"], factor)
    
    def interpolate_color(self, color1, color2, factor):
        """Interpolate between two RGB colors.
        
        Args:
            color1: Starting RGB color tuple
            color2: Ending RGB color tuple
            factor: Interpolation factor (0.0 to 1.0)
            
        Returns:
            Interpolated RGB color tuple
        """
        factor = max(0.0, min(1.0, factor))  # Clamp factor to [0, 1]
        
        r = int(color1[0] + (color2[0] - color1[0]) * factor)
        g = int(color1[1] + (color2[1] - color1[1]) * factor)
        b = int(color1[2] + (color2[2] - color1[2]) * factor)
        
        return (r, g, b)

    def quit(self):
        """Clean up and quit pygame"""
        pygame.quit()
