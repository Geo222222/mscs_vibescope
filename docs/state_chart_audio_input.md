# UML State Chart Diagram: AudioInput Component States

This state chart diagram shows the various states and transitions of the AudioInput component during its lifecycle.

```mermaid
stateDiagram-v2
    [*] --> Uninitialized
    
    Uninitialized --> Initializing : AudioInput.__init__()
    
    state Initializing {
        [*] --> CreatingStream
        CreatingStream --> ConfiguringParams : Set sample rate, buffer size, dtype
        ConfiguringParams --> StartingStream : stream.start()
        StartingStream --> [*]
    }
    
    Initializing --> Active : Initialization successful
    Initializing --> Error : Initialization failed
    
    state Active {
        [*] --> Idle
        
        Idle --> Capturing : get_audio_chunk() called
        
        state Capturing {
            [*] --> Reading
            Reading --> Processing : stream.read() returns data
            Reading --> ReadError : stream.read() throws exception
            
            state Processing {
                [*] --> Flattening
                Flattening --> CalculatingLevel : audio_data.flatten()
                CalculatingLevel --> DebuggingOutput : Calculate mean amplitude
                DebuggingOutput --> [*] : Print level visualization
            }
            
            Processing --> [*] : Return audio_chunk
            ReadError --> [*] : Return zeros array
        }
        
        Capturing --> Idle : Audio chunk returned
        
        state "Overflow Detected" as Overflow
        Capturing --> Overflow : overflowed flag = True
        Overflow --> Idle : Handle overflow (continue processing)
    }
    
    Active --> Closing : close() called
    Error --> Closing : Cleanup after error
    
    state Closing {
        [*] --> Stopping
        Stopping --> StreamStopped : stream.stop()
        StreamStopped --> StreamClosed : stream.close()
        StreamClosed --> [*]
    }
    
    Closing --> Terminated
    Terminated --> [*]
    
    state Error {
        [*] --> ErrorState
        ErrorState --> LoggingError : Print error message
        LoggingError --> [*]
    }

    note right of Active
        Main operational state
        Continuously processes
        audio capture requests
    end note
    
    note right of Capturing
        Critical real-time section
        Must complete within
        buffer time constraints
    end note
    
    note right of Overflow
        Buffer overflow indicates
        system cannot keep up
        with real-time requirements
    end note
```

## State Descriptions:

### Primary States:
- **Uninitialized**: Component not yet created
- **Initializing**: Setting up audio stream with hardware
- **Active**: Normal operation, ready to capture audio
- **Closing**: Cleaning up resources
- **Terminated**: Component fully shut down
- **Error**: Error condition requiring cleanup

### Active Sub-states:
- **Idle**: Waiting for audio capture request
- **Capturing**: Actively reading from audio stream
- **Processing**: Converting and preparing audio data
- **Overflow**: Handling buffer overflow conditions

### Critical Transitions:
1. **Initialization Success/Failure**: Determines if component can operate
2. **Capture Request**: Triggers real-time audio reading
3. **Overflow Detection**: Indicates performance issues
4. **Error Handling**: Ensures graceful degradation
5. **Cleanup**: Proper resource management on shutdown
