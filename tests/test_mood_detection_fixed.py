import unittest
import numpy as np
from mood.volume_strategy import VolumeStrategy
from mood.frequency_strategy import FrequencyStrategy
from core.mood_detector import MoodDetector

class TestMoodDetection(unittest.TestCase):
    """Unit tests for mood detection strategies and mood detector."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.volume_strategy = VolumeStrategy()
        self.frequency_strategy = FrequencyStrategy()
        self.detector = MoodDetector(self.volume_strategy)
        
        # Create test FFT data patterns with specific volume levels optimized for new thresholds
        self.low_volume_data = np.random.rand(1024) * 0.02  # Low amplitude (avg ~0.01, below 0.05)
        self.medium_volume_data = np.random.rand(1024) * 0.2  # Medium amplitude (avg ~0.1, between 0.05-0.15)
        self.high_volume_data = np.random.rand(1024) * 0.6  # High amplitude (avg ~0.3, above 0.15)

        # Gets rid of noise for real world testing - commented out old values
        # self.low_volume_data = np.random.rand(1024) * 0.1  # Low amplitude (avg ~0.1)
        # self.medium_volume_data = np.random.rand(1024) * 0.5  # Medium amplitude (avg ~0.5)
        # self.high_volume_data = np.random.rand(1024) * 0.9  # High amplitude (avg ~0.9)

        # Create frequency-biased test data
        self.bass_heavy_data = np.zeros(1024)
        self.bass_heavy_data[:256] = np.random.rand(256) * 0.8  # Strong low frequencies
        self.bass_heavy_data[256:] = np.random.rand(768) * 0.2  # Weak high frequencies
        
        self.treble_heavy_data = np.zeros(1024)
        self.treble_heavy_data[:256] = np.random.rand(256) * 0.2  # Weak low frequencies
        self.treble_heavy_data[256:] = np.random.rand(768) * 0.8  # Strong high frequencies
    
    def test_volume_strategy_calm(self):
        """Test volume strategy detects calm mood for low volume."""
        mood = self.volume_strategy.detect_mood(self.low_volume_data)
        self.assertEqual(mood, "Calm")
    
    def test_volume_strategy_chill(self):
        """Test volume strategy detects chill mood for medium volume."""
        mood = self.volume_strategy.detect_mood(self.medium_volume_data)
        self.assertEqual(mood, "Chill")
    
    def test_volume_strategy_hype(self):
        """Test volume strategy detects hype mood for high volume."""
        mood = self.volume_strategy.detect_mood(self.high_volume_data)
        self.assertEqual(mood, "Hype")
    
    def test_frequency_strategy_mellow(self):
        """Test frequency strategy detects mellow mood for bass-heavy audio."""
        mood = self.frequency_strategy.detect_mood(self.bass_heavy_data)
        self.assertEqual(mood, "Mellow")
    
    def test_frequency_strategy_energetic(self):
        """Test frequency strategy detects energetic mood for treble-heavy audio."""
        mood = self.frequency_strategy.detect_mood(self.treble_heavy_data)
        self.assertEqual(mood, "Energetic")
    
    def test_mood_detector_strategy_switching(self):
        """Test mood detector can switch between strategies."""
        # Start with volume strategy
        mood1 = self.detector.analyze(self.high_volume_data)
        self.assertEqual(mood1, "Hype")
        
        # Switch to frequency strategy
        self.detector.set_strategy(self.frequency_strategy)
        mood2 = self.detector.analyze(self.treble_heavy_data)
        self.assertEqual(mood2, "Energetic")
    
    def test_mood_detector_history(self):
        """Test mood detector maintains history correctly."""
        # Analyze several frames
        for _ in range(5):
            self.detector.analyze(self.high_volume_data)
        
        # Check history is maintained
        self.assertEqual(len(self.detector.mood_history), 5)
        self.assertEqual(self.detector.get_dominant_mood(), "Hype")
    
    def test_mood_detector_confidence(self):
        """Test mood detector calculates confidence correctly."""
        # Analyze consistent data
        for _ in range(5):
            self.detector.analyze(self.high_volume_data)
        
        # Should have high confidence for consistent moods
        confidence = self.detector.get_mood_confidence()
        self.assertGreater(confidence, 0.8)
    
    def test_custom_thresholds(self):
        """Test volume strategy with custom thresholds."""
        custom_strategy = VolumeStrategy(hype_threshold=0.08, chill_threshold=0.03)
        
        # Create specific test data for custom thresholds
        high_medium_data = np.random.rand(1024) * 0.25  # Should average ~0.125, above 0.08 threshold
        mood = custom_strategy.detect_mood(high_medium_data)
        # With these thresholds, this volume should be "Hype"
        self.assertEqual(mood, "Hype")

if __name__ == '__main__':
    unittest.main()
