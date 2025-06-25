from typing import Optional
import numpy as np
from mood.strategy_base import MoodStrategy

class MoodDetector:
    """Pluggable mood detection system using strategy pattern.
    
    This class provides a flexible framework for real-time mood analysis
    by allowing different mood detection strategies to be plugged in and
    switched dynamically. The strategy pattern enables easy addition of
    new mood detection algorithms without modifying existing code.
    """
    
    def __init__(self, strategy: MoodStrategy):
        """Initialize mood detector with a specific strategy.
        
        Args:
            strategy: Initial mood detection strategy to use
        """
        self.strategy = strategy
        self.last_mood = "Unknown"
        self.mood_history = []
        self.max_history = 10  # Keep last 10 mood readings for smoothing
    
    def set_strategy(self, strategy: MoodStrategy):
        """Change the mood detection strategy.
        
        Args:
            strategy: New mood detection strategy to use
        """
        self.strategy = strategy
    
    def analyze(self, fft_data: np.ndarray) -> str:
        """Analyze FFT data and return detected mood.
        
        Args:
            fft_data: Normalized FFT magnitude data from audio processing
            
        Returns:
            String representing the detected mood
        """
        # Use current strategy to detect mood
        current_mood = self.strategy.detect_mood(fft_data)
        
        # Update mood history for potential smoothing
        self.mood_history.append(current_mood)
        if len(self.mood_history) > self.max_history:
            self.mood_history.pop(0)
        
        # Store and return current mood
        self.last_mood = current_mood
        return current_mood
    
    def get_mood_confidence(self) -> float:
        """Calculate confidence based on mood stability over recent history.
        
        Returns:
            Confidence value between 0.0 and 1.0
        """
        if len(self.mood_history) < 3:
            return 0.5  # Low confidence with insufficient data
        
        # Calculate how consistent the recent moods have been
        recent_moods = self.mood_history[-5:]  # Look at last 5 readings
        most_common_mood = max(set(recent_moods), key=recent_moods.count)
        consistency = recent_moods.count(most_common_mood) / len(recent_moods)
        
        return consistency
    
    def get_dominant_mood(self) -> str:
        """Get the most frequent mood from recent history.
        
        Returns:
            Most commonly detected mood from recent analysis
        """
        if not self.mood_history:
            return "Unknown"
        
        return max(set(self.mood_history), key=self.mood_history.count)
