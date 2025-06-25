# VibeScope Phase 2: Mood Detection Engine

## Overview
Phase 2 introduces an intelligent mood detection system that analyzes audio frequency data in real-time to determine the emotional characteristics of the audio input. The system uses a flexible strategy pattern that allows for multiple mood detection algorithms.

## Architecture

### Strategy Pattern Implementation
The mood detection system is built using the Strategy design pattern, which provides:
- **Flexibility**: Easy switching between different mood detection algorithms
- **Extensibility**: Simple addition of new mood detection strategies
- **Separation of Concerns**: Each strategy focuses on a specific approach to mood analysis

### Core Components

#### 1. MoodStrategy (Abstract Base Class)
- **Location**: `mood/strategy_base.py`
- **Purpose**: Defines the interface that all mood detection strategies must implement
- **Key Method**: `detect_mood(fft_data) -> str`

#### 2. VolumeStrategy
- **Location**: `mood/volume_strategy.py`
- **Approach**: Analyzes overall audio amplitude/volume
- **Moods Detected**:
  - **"Calm"**: Low volume (< 0.3 threshold)
  - **"Chill"**: Medium volume (0.3 - 0.7 threshold)
  - **"Hype"**: High volume (> 0.7 threshold)
- **Use Case**: Simple, reliable mood detection based on energy levels

#### 3. FrequencyStrategy
- **Location**: `mood/frequency_strategy.py`
- **Approach**: Analyzes energy distribution between low and high frequencies
- **Moods Detected**:
  - **"Mellow"**: Low-frequency dominance (bass-heavy)
  - **"Energetic"**: High-frequency dominance (treble-heavy)
  - **"Balanced"**: Even frequency distribution
- **Use Case**: Genre-aware mood detection (e.g., bass-heavy vs bright music)

#### 4. SpectralStrategy (Advanced)
- **Location**: `mood/spectral_strategy.py`
- **Approach**: Advanced spectral feature analysis
- **Features Analyzed**:
  - Spectral centroid (brightness)
  - Spectral rolloff (energy distribution)
  - Spectral flux (rate of change)
- **Moods Detected**:
  - **"Bright"**: High centroid, stable
  - **"Dynamic"**: High centroid, changing
  - **"Deep"**: Low centroid, stable
  - **"Intense"**: Low centroid, changing
  - **"Chaotic"**: Rapidly changing
  - **"Evolving"**: Moderately changing
  - **"Steady"**: Stable and moderate
  - **"Neutral"**: Default state

#### 5. MoodDetector
- **Location**: `core/mood_detector.py`
- **Purpose**: Manages mood detection strategies and provides additional features
- **Features**:
  - Strategy switching at runtime
  - Mood history tracking (last 10 readings)
  - Confidence calculation based on consistency
  - Dominant mood analysis

## User Interface

### Real-Time Controls
- **V Key**: Switch to Volume-based strategy
- **F Key**: Switch to Frequency-based strategy  
- **S Key**: Switch to Spectral analysis strategy

### Console Output
```
[Mood]: Hype | Confidence: 0.85 | Dominant: Hype
🔄 Switched to Frequency-based mood detection
[Mood]: Energetic | Confidence: 0.92 | Dominant: Energetic
```

## Technical Implementation

### Integration with Main Loop
```python
# Initialize mood detection
mood_detector = MoodDetector(VolumeStrategy())

# In processing loop
mood = mood_detector.analyze(fft_data)
confidence = mood_detector.get_mood_confidence()
dominant_mood = mood_detector.get_dominant_mood()
```

### Data Flow
1. **Audio Capture**: Raw audio → `AudioInput`
2. **FFT Processing**: Time domain → Frequency domain → `FFTProcessor`
3. **Mood Analysis**: Frequency data → Mood classification → `MoodDetector`
4. **Visualization**: Combined frequency + mood display → `Visualizer`

### Performance Characteristics
- **Real-time Processing**: Maintains 30 FPS with mood analysis
- **Low Latency**: Mood detection adds < 1ms per frame
- **Memory Efficient**: Minimal additional memory footprint
- **Configurable**: Adjustable thresholds and parameters

## Testing

### Unit Tests
- **Location**: `tests/test_mood_detection.py`
- **Coverage**: All mood strategies and detector functionality
- **Test Cases**:
  - Strategy-specific mood detection
  - Strategy switching
  - History and confidence tracking
  - Custom threshold testing

### Running Tests
```bash
python -m pytest tests/test_mood_detection.py -v
```

## Future Enhancements

### Potential New Strategies
1. **TemporalStrategy**: Analyze rhythm and tempo patterns
2. **HarmonicStrategy**: Detect chord progressions and harmonic content
3. **MLStrategy**: Machine learning-based mood classification
4. **CombinedStrategy**: Weighted combination of multiple strategies

### Advanced Features
- Mood transition smoothing
- Personalized mood calibration
- Genre-specific mood models
- Export mood analysis data
- Visual mood indicators in the spectrum display

## Configuration

### Volume Strategy Parameters
```python
VolumeStrategy(
    hype_threshold=0.7,    # Volume level for "Hype" mood
    chill_threshold=0.3    # Volume level for "Chill" mood
)
```

### Frequency Strategy Parameters
```python
FrequencyStrategy(
    energy_ratio_threshold=1.5    # Ratio for frequency dominance
)
```

### Mood Detector Settings
```python
MoodDetector(
    strategy=initial_strategy,
    max_history=10    # Number of mood readings to keep
)
```

## Error Handling

The mood detection system includes robust error handling:
- Graceful fallback for invalid audio data
- Strategy switching without interrupting processing
- Confidence tracking to identify unreliable detections
- Automatic recovery from processing errors

## Performance Monitoring

Monitor mood detection performance through:
- Confidence values (0.0 - 1.0)
- Mood stability over time
- Strategy comparison
- Processing time metrics
