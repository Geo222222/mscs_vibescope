from core.audio_input import AudioInput
from core.fft_processor import FFTProcessor
from core.mood_detector import MoodDetector
from ui.visualizer import Visualizer
from mood.volume_strategy import VolumeStrategy
from mood.frequency_strategy import FrequencyStrategy
from mood.spectral_strategy import SpectralStrategy
from config.config import FPS
import pygame

def print_welcome():
    print("=" * 70)
    print("🎧  Welcome to VibeScope – Ambient Emotion Radar")
    print("📡  Listening for audio... analyzing frequency spectrum...")
    print("🧠  Phase 2: Real-time Mood Detection Engine Active")
    print("🎹  Controls: [V] Volume Strategy | [F] Frequency Strategy | [S] Spectral Strategy")
    print("=" * 70)


def main():
    print_welcome()
    audio = AudioInput()
    fft = FFTProcessor()
    ui = Visualizer()
    
    # Initialize mood detection system with volume strategy
    mood_detector = MoodDetector(VolumeStrategy())
    
    # Track mood detection statistics
    frame_count = 0
    mood_display_interval = 30  # Update mood display every 30 frames (1 second at 30 FPS)

    running = True
    while running:
        chunk = audio.get_audio_chunk()
        fft_data = fft.process(chunk)
        
        # Analyze mood from frequency data
        mood = mood_detector.analyze(fft_data)
        
        # Display mood information periodically
        frame_count += 1
        if frame_count % mood_display_interval == 0:
            confidence = mood_detector.get_mood_confidence()
            dominant_mood = mood_detector.get_dominant_mood()
            print(f"[Mood]: {mood} | Confidence: {confidence:.2f} | Dominant: {dominant_mood}")
        
        # Draw visualization with mood-based colors
        ui.draw(fft_data, mood)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                # Allow switching between mood detection strategies
                if event.key == pygame.K_v:
                    mood_detector.set_strategy(VolumeStrategy())
                    print("🔄 Switched to Volume-based mood detection")
                elif event.key == pygame.K_f:
                    mood_detector.set_strategy(FrequencyStrategy())
                    print("🔄 Switched to Frequency-based mood detection")
                elif event.key == pygame.K_s:
                    mood_detector.set_strategy(SpectralStrategy())
                    print("🔄 Switched to Spectral analysis mood detection")

        ui.clock.tick(FPS)

    audio.close()
    ui.quit()

if __name__ == "__main__":
    main()

