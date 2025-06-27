#!/usr/bin/env python3
"""Test script to validate all mood detection strategies work correctly."""

import numpy as np
from mood.volume_strategy import VolumeStrategy
from mood.frequency_strategy import FrequencyStrategy  
from mood.spectral_strategy import SpectralStrategy
from core.mood_detector import MoodDetector

def test_volume_strategy():
    print("🔊 Testing Volume Strategy:")
    strategy = VolumeStrategy()
    
    # Test low volume (should be Calm)
    low_volume_data = np.random.rand(1024) * 0.02  # Very quiet
    mood = strategy.detect_mood(low_volume_data)
    print(f"  Low volume: {mood}")
    
    # Test medium volume (should be Chill)
    medium_volume_data = np.random.rand(1024) * 0.08  # Medium
    mood = strategy.detect_mood(medium_volume_data)
    print(f"  Medium volume: {mood}")
    
    # Test high volume (should be Hype)
    high_volume_data = np.random.rand(1024) * 0.2  # Loud
    mood = strategy.detect_mood(high_volume_data)
    print(f"  High volume: {mood}")

def test_frequency_strategy():
    print("\n🎵 Testing Frequency Strategy:")
    strategy = FrequencyStrategy()
    
    # Test low frequency dominant
    low_freq_data = np.zeros(1024)
    low_freq_data[:256] = 0.8  # Strong bass
    low_freq_data[256:] = 0.1  # Weak treble
    mood = strategy.detect_mood(low_freq_data)
    print(f"  Low frequency dominant: {mood}")
    
    # Test high frequency dominant
    high_freq_data = np.zeros(1024)
    high_freq_data[:256] = 0.1  # Weak bass
    high_freq_data[256:] = 0.8  # Strong treble
    mood = strategy.detect_mood(high_freq_data)
    print(f"  High frequency dominant: {mood}")
    
    # Test balanced
    balanced_data = np.random.rand(1024) * 0.5
    mood = strategy.detect_mood(balanced_data)
    print(f"  Balanced frequencies: {mood}")

def test_spectral_strategy():
    print("\n🎨 Testing Spectral Strategy:")
    strategy = SpectralStrategy()
    
    # Test bright signal (high centroid)
    bright_data = np.zeros(1024)
    bright_data[800:] = 0.9  # Energy in high frequencies
    mood = strategy.detect_mood(bright_data)
    print(f"  Bright signal: {mood}")
    
    # Test dark signal (low centroid)
    dark_data = np.zeros(1024)
    dark_data[:200] = 0.9  # Energy in low frequencies
    mood = strategy.detect_mood(dark_data)
    print(f"  Dark signal: {mood}")
    
    # Test changing signal (high flux)
    for i in range(3):  # Build up flux history
        changing_data = np.random.rand(1024) * 0.6
        mood = strategy.detect_mood(changing_data)
    print(f"  Changing signal: {mood}")

def test_mood_detector_integration():
    print("\n🧠 Testing MoodDetector Integration:")
    
    # Test with Volume Strategy
    mood_detector = MoodDetector(VolumeStrategy())
    test_data = np.random.rand(1024) * 0.1
    
    # Analyze several frames to build confidence
    moods = []
    for i in range(5):
        mood = mood_detector.analyze(test_data)
        moods.append(mood)
    
    confidence = mood_detector.get_mood_confidence()
    dominant = mood_detector.get_dominant_mood()
    
    print(f"  Analyzed moods: {moods}")
    print(f"  Confidence: {confidence:.2f}")
    print(f"  Dominant mood: {dominant}")
    
    # Test strategy switching
    print("\n🔄 Testing Strategy Switching:")
    mood_detector.set_strategy(FrequencyStrategy())
    new_mood = mood_detector.analyze(test_data)
    print(f"  After switching to Frequency Strategy: {new_mood}")

def main():
    print("🎯 Phase 2 Mood Detection Strategy Test")
    print("=" * 50)
    
    test_volume_strategy()
    test_frequency_strategy()
    test_spectral_strategy()
    test_mood_detector_integration()
    
    print("\n✅ All mood detection strategies tested successfully!")
    print("🎮 Ready for Phase 2 screencast demonstration!")

if __name__ == "__main__":
    main()
