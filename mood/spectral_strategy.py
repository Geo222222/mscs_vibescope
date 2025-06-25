import numpy as np
from .strategy_base import MoodStrategy

class SpectralStrategy(MoodStrategy):
    """Advanced mood detection strategy based on spectral features.
    
    This strategy analyzes multiple spectral characteristics:
    - Spectral centroid (brightness)
    - Spectral rolloff (energy distribution)
    - Spectral flux (change rate)
    - Zero crossing rate equivalent in frequency domain
    """
    
    def __init__(self):
        """Initialize spectral-based mood detection."""
        self.previous_spectrum = None
        self.flux_history = []
        self.max_flux_history = 5
    
    def detect_mood(self, fft_data: np.ndarray) -> str:
        """Detect mood based on advanced spectral features.
        
        Args:
            fft_data: Normalized FFT magnitude data
            
        Returns:
            Mood string based on spectral analysis
        """
        # Calculate spectral centroid (weighted average frequency)
        frequencies = np.arange(len(fft_data))
        spectral_centroid = np.sum(frequencies * fft_data) / (np.sum(fft_data) + 1e-10)
        centroid_ratio = spectral_centroid / len(fft_data)
        
        # Calculate spectral rolloff (frequency below which 85% of energy lies)
        cumulative_energy = np.cumsum(fft_data)
        total_energy = cumulative_energy[-1]
        rolloff_threshold = 0.85 * total_energy
        rolloff_point = np.argmax(cumulative_energy >= rolloff_threshold)
        rolloff_ratio = rolloff_point / len(fft_data)
        
        # Calculate spectral flux (change from previous frame)
        flux = 0.0
        if self.previous_spectrum is not None:
            flux = np.sum(np.abs(fft_data - self.previous_spectrum))
            self.flux_history.append(flux)
            if len(self.flux_history) > self.max_flux_history:
                self.flux_history.pop(0)
        
        self.previous_spectrum = fft_data.copy()
        
        # Calculate average flux for stability
        avg_flux = np.mean(self.flux_history) if self.flux_history else 0.0
        
        # Mood classification based on spectral features
        return self._classify_mood(centroid_ratio, rolloff_ratio, avg_flux)
    
    def _classify_mood(self, centroid_ratio: float, rolloff_ratio: float, flux: float) -> str:
        """Classify mood based on spectral feature combinations.
        
        Args:
            centroid_ratio: Normalized spectral centroid (0-1)
            rolloff_ratio: Normalized spectral rolloff point (0-1)  
            flux: Average spectral flux (rate of change)
            
        Returns:
            Classified mood string
        """
        # High brightness + high energy distribution = Bright/Energetic
        if centroid_ratio > 0.6 and rolloff_ratio > 0.7:
            if flux > 0.3:
                return "Dynamic"    # Changing and bright
            else:
                return "Bright"     # Stable and bright
        
        # Low brightness + low energy concentration = Dark/Deep
        elif centroid_ratio < 0.3 and rolloff_ratio < 0.4:
            if flux > 0.3:
                return "Intense"    # Changing and dark
            else:
                return "Deep"       # Stable and dark
        
        # High flux regardless of other features = Very dynamic
        elif flux > 0.5:
            return "Chaotic"        # Rapidly changing
        
        # Moderate characteristics
        elif 0.3 <= centroid_ratio <= 0.6:
            if flux > 0.2:
                return "Evolving"   # Moderately changing
            else:
                return "Steady"     # Stable and moderate
        
        # Default fallback
        else:
            return "Neutral"
