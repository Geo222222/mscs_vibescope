# VibeScope - Real-Time Audio Visualization

## Overview
VibeScope is a real-time audio visualization tool developed as part of the Full Sail University Master of Science in Computer Science program. This application captures audio input and creates dynamic visual representations of frequency spectrums using Fast Fourier Transform (FFT) analysis.

## Features
- Real-time audio capture using sounddevice
- FFT-based frequency analysis
- Dynamic visualization using pygame
- Color-gradient spectrum display
- Logarithmic scaling for better frequency visualization
- Configurable sample rate and buffer size

## Technical Specifications
- **Sample Rate:** 44.1kHz (CD Quality)
- **Buffer Size:** 2048 samples
- **FFT Bins:** 1024 frequency bands
- **Frame Rate:** 30 FPS
- **Window Size:** 1024x600 pixels

## Dependencies
- Python 3.x
- numpy
- pygame
- sounddevice
- PyInstaller (for executable build)

## Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/vibescope.git
cd vibescope

# Install dependencies
pip install -r requirements.txt

# Run the application
python -m app.main
```

## Project Structure
```
vibescope/
├── app/               # Application entry point and config
├── core/             # Core audio processing
├── ui/               # Visualization components
├── tests/            # Unit tests
└── docs/             # Documentation
```

## Key Components
1. **Audio Input** (core/audio_input.py)
   - Handles microphone input
   - Manages audio buffer
   - Provides real-time audio chunks

2. **FFT Processor** (core/fft_processor.py)
   - Performs Fast Fourier Transform
   - Normalizes frequency data
   - Processes audio for visualization

3. **Visualizer** (ui/visualizer.py)
   - Creates visualization window
   - Renders frequency bars
   - Implements color gradients
   - Manages display updates

## Building the Executable
```bash
python build_exe.py
```
The executable will be created in the `dist` directory.

## Testing
```bash
python -m unittest discover tests
```

## Course Context
This project was developed as part of the Full Sail University Master of Science in Computer Science program, demonstrating:
- Real-time signal processing
- Audio analysis
- Data visualization
- Object-oriented design
- Test-driven development

## Author
[Your Name]
Full Sail University
Master of Science in Computer Science

## License
[Your chosen license]
