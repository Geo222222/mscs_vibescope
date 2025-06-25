import numpy as np
from .strategy_base import MoodStrategy

class FrequencyStrategy(MoodStrategy):
    """Mood detection strategy based on frequency distribution analysis.
    
    This strategy analyzes the energy distribution between low and high 
    frequencies to determine mood:
    - High-frequency dominant: Energetic/Bright
    - Low-frequency dominant: Mellow/Deep
    - Balanced: Balanced/Neutral
    """
    
    def __init__(self, energy_ratio_threshold: float = 1.5):
        """Initialize frequency-based mood detection.
        
        Args:
            energy_ratio_threshold: Ratio threshold for frequency dominance detection
        """
        self.energy_ratio_threshold = energy_ratio_threshold
    
    def detect_mood(self, fft_data: np.ndarray) -> str:
        """Detect mood based on low vs high frequency energy distribution.
        
        Args:
            fft_data: Normalized FFT magnitude data
            
        Returns:
            "Energetic" for high-freq dominance, "Mellow" for low-freq, "Balanced" otherwise
        """
        # Split frequency spectrum into low and high frequency regions
        midpoint = len(fft_data) // 2
        low_energy = np.sum(fft_data[:midpoint])    # Bass/low frequencies
        high_energy = np.sum(fft_data[midpoint:])   # Treble/high frequencies
        
        # Analyze energy distribution patterns
        if high_energy > low_energy * self.energy_ratio_threshold:
            return "Energetic"  # High frequencies dominate (bright, energetic sound)
        elif low_energy > high_energy * self.energy_ratio_threshold:
            return "Mellow"     # Low frequencies dominate (deep, mellow sound)
        else:
            return "Balanced"   # Relatively even distribution
