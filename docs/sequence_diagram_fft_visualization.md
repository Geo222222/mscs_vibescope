# UML Sequence Diagram: FFT Processing and Visualization Pipeline

This sequence diagram focuses on the detailed FFT processing and visualization rendering pipeline.

```mermaid
sequenceDiagram
    participant Main as Main Loop
    participant FFT as FFTProcessor
    participant Numpy as NumPy FFT
    participant UI as Visualizer
    participant Math as Math Operations
    participant Pygame as Pygame Renderer

    Note over Main, Pygame: FFT Processing Phase
    Main->>FFT: process(audio_chunk[2048])
    
    FFT->>Numpy: np.fft.rfft(audio_data)
    Note right of Numpy: Real FFT converts 2048 time samples<br/>to 1025 frequency bins
    Numpy-->>FFT: complex_fft[1025]
    
    FFT->>FFT: np.abs(complex_fft)
    Note right of FFT: Extract magnitude from<br/>complex frequency data
    
    FFT->>FFT: Calculate max(fft)
    alt max(fft) != 0
        FFT->>FFT: fft / max(fft)
        Note right of FFT: Normalize to 0-1 range
    else max(fft) == 0
        FFT->>FFT: Return original fft
        Note right of FFT: Avoid division by zero
    end
    
    FFT-->>Main: normalized_fft[1025]

    Note over Main, Pygame: Visualization Phase
    Main->>UI: draw(fft_data)
    
    UI->>Pygame: screen.fill((0, 0, 20))
    Note right of Pygame: Clear to dark blue background
    
    UI->>Math: np.log10(np.clip(fft_data, 1e-10, None))
    Note right of Math: Logarithmic scaling for<br/>better frequency perception
    Math-->>UI: log_fft
    
    UI->>Math: (log_fft - min) / (max - min)
    Note right of Math: Normalize log data to 0-1 range
    Math-->>UI: scaled_fft
    
    loop For each frequency bin i (0 to FFT_BINS-1)
        UI->>UI: magnitude = scaled_fft[i]
        UI->>UI: bar_height = magnitude * height * 0.9
        UI->>UI: x = i * bar_width
        UI->>UI: y = height - bar_height
        
        UI->>UI: get_color(magnitude)
        Note right of UI: Calculate RGB gradient:<br/>R = 255 * magnitude<br/>G = 255 * (1 - abs(mag - 0.5))<br/>B = 255 * (1 - magnitude)
        
        UI->>Pygame: pygame.draw.rect(screen, color, (x, y, width-1, height))
        Note right of Pygame: Draw individual frequency bar<br/>with 1px spacing
    end
    
    UI->>Pygame: pygame.display.flip()
    Note right of Pygame: Present rendered frame to screen
    
    UI-->>Main: Visualization complete

    Note over Main, Pygame: Color Mapping Algorithm
    Note over UI: Color gradient creates visual frequency mapping:<br/>• Low frequencies: Blue dominant<br/>• Mid frequencies: Green peaks<br/>• High frequencies: Red dominant<br/>• Creates rainbow spectrum effect
```

## Key Processing Steps:

### FFT Algorithm Flow:
1. **Real FFT Transform**: Converts 2048 time-domain samples to 1025 frequency bins
2. **Magnitude Extraction**: Converts complex numbers to magnitude values
3. **Normalization**: Scales data to 0-1 range for consistent visualization

### Visualization Pipeline:
1. **Logarithmic Scaling**: Improves perception of frequency dynamics
2. **Screen Clearing**: Prepares canvas for new frame
3. **Bar Calculation**: Maps frequency magnitude to visual bar height
4. **Color Mapping**: Creates spectral color gradient
5. **Rendering**: Draws individual frequency bars
6. **Display Update**: Presents completed frame

### Mathematical Transformations:
- **Time to Frequency Domain**: `np.fft.rfft()` 
- **Logarithmic Perception**: `np.log10()` for human-like frequency hearing
- **Dynamic Range Compression**: Normalization for consistent display
- **Spatial Mapping**: Frequency bins to screen pixel coordinates
