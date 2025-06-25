import numpy as np
from .strategy_base import MoodStrategy

class VolumeStrategy(MoodStrategy):
    """Mood detection strategy based on overall audio volume/amplitude.
    
    This strategy analyzes the mean amplitude of the frequency spectrum
    to determine mood based on overall energy levels:
    - High volume: Hype/Excited
    - Medium volume: Chill/Relaxed  
    - Low volume: Calm/Quiet    """
    
    def __init__(self, hype_threshold: float = 0.15, chill_threshold: float = 0.05):
        """Initialize volume-based mood detection.
        
        Args:
            hype_threshold: Volume level above which mood is "Hype" (default: 0.15)
            chill_threshold: Volume level above which mood is "Chill" (default: 0.05)
            
        Note: Thresholds are optimized for FFT data normalized by max value.
        Typical average values range from 0.01 (quiet) to 0.25 (very loud).
        """
        self.hype_threshold = hype_threshold
        self.chill_threshold = chill_threshold
    
    def detect_mood(self, fft_data: np.ndarray) -> str:
        """Detect mood based on average volume level.
        
        Args:
            fft_data: Normalized FFT magnitude data
            
        Returns:
            "Hype" for high volume, "Chill" for medium, "Calm" for low
        """
        # Calculate average volume across all frequency bins
        avg_volume = np.mean(fft_data)
        
        # Debug: Print actual volume values occasionally
        if hasattr(self, '_debug_counter'):
            self._debug_counter += 1
        else:
            self._debug_counter = 0
            
        if self._debug_counter % 30 == 0:  # Print every 30 frames (1 second)
            max_vol = np.max(fft_data)
            print(f"Debug - Avg: {avg_volume:.4f}, Max: {max_vol:.4f}, Thresholds: {self.chill_threshold:.2f}/{self.hype_threshold:.2f}")
        
        if avg_volume > self.hype_threshold:
            return "Hype"
        elif avg_volume > self.chill_threshold:
            return "Chill"
        else:
            return "Calm"
