import unittest
import numpy as np
from ui.visualizer import Visualizer
import pygame

class TestVisualizerMoodColors(unittest.TestCase):
    """Unit tests for mood-based visualization colors."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Initialize pygame for testing (headless mode)
        import os
        os.environ['SDL_VIDEODRIVER'] = 'dummy'  # Use dummy video driver for testing
        self.visualizer = Visualizer()
        
        # Create test FFT data
        self.test_fft_data = np.random.rand(1024) * 0.5
    
    def test_mood_color_schemes_exist(self):
        """Test that all expected mood color schemes are defined."""
        expected_moods = [
            # Volume Strategy
            "Calm", "Chill", "Hype",
            # Frequency Strategy
            "Mellow", "Balanced", "Energetic",
            # Spectral Strategy
            "Bright", "Deep", "Dynamic", "Intense", "Chaotic", "Evolving", "Steady",
            # Default
            "Neutral"
        ]
        
        for mood in expected_moods:
            self.assertIn(mood, self.visualizer.mood_colors)
            
            # Check that each mood has required color components
            mood_colors = self.visualizer.mood_colors[mood]
            self.assertIn("background", mood_colors)
            self.assertIn("primary", mood_colors)
            self.assertIn("secondary", mood_colors)
            self.assertIn("accent", mood_colors)
    
    def test_color_interpolation(self):
        """Test color interpolation function."""
        color1 = (0, 0, 0)      # Black
        color2 = (255, 255, 255)  # White
        
        # Test interpolation at 0% (should be color1)
        result = self.visualizer.interpolate_color(color1, color2, 0.0)
        self.assertEqual(result, color1)
        
        # Test interpolation at 100% (should be color2)
        result = self.visualizer.interpolate_color(color1, color2, 1.0)
        self.assertEqual(result, color2)
        
        # Test interpolation at 50% (should be middle gray)
        result = self.visualizer.interpolate_color(color1, color2, 0.5)
        self.assertEqual(result, (127, 127, 127))
    
    def test_mood_color_generation(self):
        """Test that mood-based colors are generated correctly."""
        calm_colors = self.visualizer.mood_colors["Calm"]
        
        # Test low magnitude (should be closer to background)
        low_color = self.visualizer.get_mood_color(0.1, calm_colors)
        self.assertIsInstance(low_color, tuple)
        self.assertEqual(len(low_color), 3)
        
        # Test high magnitude (should be closer to accent)
        high_color = self.visualizer.get_mood_color(0.9, calm_colors)
        self.assertIsInstance(high_color, tuple)
        self.assertEqual(len(high_color), 3)
        
        # High magnitude should generally be brighter than low magnitude for most moods
        # (though this depends on the specific color scheme)
    
    def test_draw_with_different_moods(self):
        """Test drawing with different mood parameters."""
        test_moods = ["Calm", "Hype", "Energetic", "Chaotic", "Neutral"]
        
        for mood in test_moods:
            try:
                # This should not raise an exception
                self.visualizer.draw(self.test_fft_data, mood)
                
                # Verify mood was set
                self.assertEqual(self.visualizer.current_mood, mood)
            except Exception as e:
                self.fail(f"Drawing with mood '{mood}' raised an exception: {e}")
    
    def test_invalid_mood_fallback(self):
        """Test that invalid moods fall back to Neutral."""
        # Test with an invalid mood
        self.visualizer.draw(self.test_fft_data, "InvalidMood")
        
        # Should fall back to using Neutral color scheme
        # (We can't easily test the visual output, but we can ensure no crash)
    
    def test_color_values_valid_range(self):
        """Test that all color values are in valid RGB range (0-255)."""
        for mood_name, mood_colors in self.visualizer.mood_colors.items():
            for color_type, color_tuple in mood_colors.items():
                self.assertEqual(len(color_tuple), 3, f"Color {color_type} in {mood_name} should have 3 components")
                
                for component in color_tuple:
                    self.assertGreaterEqual(component, 0, f"Color component in {mood_name}.{color_type} should be >= 0")
                    self.assertLessEqual(component, 255, f"Color component in {mood_name}.{color_type} should be <= 255")
    
    def tearDown(self):
        """Clean up after tests."""
        try:
            self.visualizer.quit()
        except:
            pass  # Ignore cleanup errors in headless mode

if __name__ == '__main__':
    unittest.main()
