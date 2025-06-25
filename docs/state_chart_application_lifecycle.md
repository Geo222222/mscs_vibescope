# UML State Chart Diagram: VibeScope Application States

This state chart diagram shows the overall application lifecycle and state transitions of the VibeScope system.

```mermaid
stateDiagram-v2
    [*] --> Starting
    
    Starting --> Initializing : main() called
    
    state Initializing {
        [*] --> PrintingWelcome
        PrintingWelcome --> CreatingComponents : print_welcome()
        
        state CreatingComponents {
            [*] --> InitAudio
            InitAudio --> InitFFT : AudioInput() success
            InitFFT --> InitUI : FFTProcessor() success
            InitUI --> [*] : Visualizer() success
        }
        
        CreatingComponents --> [*] : All components ready
    }
    
    Initializing --> Running : Initialization successful
    Initializing --> InitError : Component creation failed
    
    state Running {
        [*] --> ProcessingFrame
        
        state ProcessingFrame {
            [*] --> CapturingAudio
            CapturingAudio --> ProcessingFFT : Audio chunk received
            ProcessingFFT --> RenderingFrame : FFT data ready
            RenderingFrame --> CheckingEvents : Frame rendered
            CheckingEvents --> FrameRateControl : Events processed
            FrameRateControl --> [*] : FPS maintained
        }
        
        ProcessingFrame --> ProcessingFrame : Continue loop
        ProcessingFrame --> ShuttingDown : QUIT event received
        
        state "Error Recovery" as ErrorRecovery
        ProcessingFrame --> ErrorRecovery : Audio/Processing error
        ErrorRecovery --> ProcessingFrame : Error handled, continue
        ErrorRecovery --> ShuttingDown : Critical error, exit
    }
    
    state ShuttingDown {
        [*] --> ClosingAudio
        ClosingAudio --> CleaningUI : audio.close()
        CleaningUI --> [*] : ui.quit()
    }
    
    state InitError {
        [*] --> LoggingError
        LoggingError --> [*] : Error reported
    }
    
    Running --> ShuttingDown : User quit or error
    InitError --> ShuttingDown : Cleanup after init failure
    ShuttingDown --> Terminated
    Terminated --> [*]

    note right of ProcessingFrame
        Real-time processing loop
        Target: 30 FPS
        Critical timing requirements
    end note
    
    note right of CapturingAudio
        Must complete within
        46ms (2048 samples @ 44.1kHz)
        to avoid buffer underrun
    end note
    
    note right of ErrorRecovery
        Graceful handling of:
        - Audio device errors
        - Processing overflows
        - Rendering failures
    end note
```

## Application State Details:

### Initialization States:
- **Starting**: Application entry point
- **PrintingWelcome**: Display startup message
- **CreatingComponents**: Initialize core system components
- **InitError**: Handle initialization failures

### Runtime States:
- **ProcessingFrame**: Main processing cycle
- **CapturingAudio**: Real-time audio input
- **ProcessingFFT**: Frequency domain transformation
- **RenderingFrame**: Visual output generation
- **CheckingEvents**: User input handling
- **FrameRateControl**: Timing synchronization

### Termination States:
- **ShuttingDown**: Graceful cleanup
- **ClosingAudio**: Release audio resources
- **CleaningUI**: Cleanup display resources
- **Terminated**: Application ended

### Error Handling:
- **ErrorRecovery**: Non-fatal error handling
- **InitError**: Fatal initialization errors

## Critical Timing Constraints:

1. **Audio Buffer Timing**: 46ms window for processing 2048 samples
2. **Frame Rate Target**: 30 FPS (33ms per frame)
3. **Real-time Requirements**: Processing must keep up with audio input
4. **Error Recovery**: Must maintain real-time performance during error handling

## State Transition Triggers:

- **User Events**: Window close, keyboard input
- **System Events**: Audio device changes, errors
- **Timing Events**: Frame rate control, buffer timing
- **Error Conditions**: Hardware failures, processing overload
