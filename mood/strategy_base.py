from abc import ABC, abstractmethod
import numpy as np

class MoodStrategy(ABC):
    """Base interface for mood detection strategies.
    
    This abstract class defines the contract that all mood detection
    strategies must implement. Different strategies can analyze audio
    frequency data using various approaches (volume, frequency distribution,
    spectral features, etc.) to determine the emotional mood of the audio.
    """
    
    @abstractmethod
    def detect_mood(self, fft_data: np.ndarray) -> str:
        """Analyze FFT data and return detected mood as a string.
        
        Args:
            fft_data: Normalized FFT magnitude data (frequency spectrum)
            
        Returns:
            String representing the detected mood (e.g., "Calm", "Energetic", "Hype")
        """
        pass
