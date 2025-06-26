import unittest
import numpy as np
from core.fft_processor import FFTProcessor
from config.config import BUFFER_SIZE

class TestFFTProcessor(unittest.TestCase):
    """Unit tests for FFTProcessor class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.fft_processor = FFTProcessor()
        
        # Create test audio signals
        self.sample_rate = 44100
        self.duration = BUFFER_SIZE / self.sample_rate  # Duration in seconds
        self.time = np.linspace(0, self.duration, BUFFER_SIZE, endpoint=False)
        
        # Generate test signals
        self.silence = np.zeros(BUFFER_SIZE)
        self.dc_signal = np.ones(BUFFER_SIZE) * 0.5  # DC component
        self.sine_wave_440hz = np.sin(2 * np.pi * 440 * self.time)  # A4 note
        self.sine_wave_880hz = np.sin(2 * np.pi * 880 * self.time)  # A5 note
        self.complex_signal = (self.sine_wave_440hz * 0.7 + 
                              self.sine_wave_880hz * 0.3 + 
                              np.random.normal(0, 0.1, BUFFER_SIZE))  # Mix with noise
        self.impulse = np.zeros(BUFFER_SIZE)
        self.impulse[0] = 1.0  # Unit impulse
        
    def test_fft_processor_initialization(self):
        """Test FFTProcessor initializes correctly."""
        processor = FFTProcessor()
        self.assertIsInstance(processor, FFTProcessor)
        
        # Verify it has the process method
        self.assertTrue(hasattr(processor, 'process'))
        self.assertTrue(callable(getattr(processor, 'process')))
    
    def test_process_silence(self):
        """Test FFT processing of silence."""
        result = self.fft_processor.process(self.silence)
        
        # Result should be all zeros (or very close due to floating point)
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(len(result), BUFFER_SIZE // 2 + 1)  # Real FFT output size
        
        # All values should be very close to zero
        np.testing.assert_allclose(result, 0, atol=1e-10)
    
    def test_process_dc_signal(self):
        """Test FFT processing of DC signal."""
        result = self.fft_processor.process(self.dc_signal)
        
        # DC signal should have peak at frequency bin 0
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(len(result), BUFFER_SIZE // 2 + 1)
        
        # After normalization, max should be 1.0
        self.assertAlmostEqual(np.max(result), 1.0, places=5)
        
        # Peak should be at DC (first bin)
        peak_index = np.argmax(result)
        self.assertEqual(peak_index, 0)
    
    def test_process_sine_wave(self):
        """Test FFT processing of pure sine wave."""
        result = self.fft_processor.process(self.sine_wave_440hz)
        
        # Result should be normalized
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(len(result), BUFFER_SIZE // 2 + 1)
        self.assertAlmostEqual(np.max(result), 1.0, places=5)
        
        # Find the peak frequency
        peak_index = np.argmax(result)
        peak_frequency = peak_index * self.sample_rate / BUFFER_SIZE
        
        # Peak should be close to 440 Hz (within one frequency bin)
        frequency_resolution = self.sample_rate / BUFFER_SIZE
        self.assertLess(abs(peak_frequency - 440), frequency_resolution)
    
    def test_process_multiple_frequencies(self):
        """Test FFT processing of signal with multiple frequency components."""
        result = self.fft_processor.process(self.complex_signal)
        
        # Result should be normalized
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(len(result), BUFFER_SIZE // 2 + 1)
        self.assertAlmostEqual(np.max(result), 1.0, places=5)
        
        # Should have peaks around 440 Hz and 880 Hz
        frequencies = np.fft.rfftfreq(BUFFER_SIZE, 1/self.sample_rate)
        
        # Find indices corresponding to our test frequencies
        freq_440_idx = np.argmin(np.abs(frequencies - 440))
        freq_880_idx = np.argmin(np.abs(frequencies - 880))
        
        # These should have relatively high values
        self.assertGreater(result[freq_440_idx], 0.1)
        self.assertGreater(result[freq_880_idx], 0.1)
    
    def test_process_impulse(self):
        """Test FFT processing of unit impulse."""
        result = self.fft_processor.process(self.impulse)
        
        # Impulse should have flat spectrum (all frequencies present equally)
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(len(result), BUFFER_SIZE // 2 + 1)
        self.assertAlmostEqual(np.max(result), 1.0, places=5)
        
        # All values should be equal (flat spectrum)
        # Due to normalization, all values should be 1.0
        np.testing.assert_allclose(result, 1.0, rtol=1e-10)
    
    def test_normalization_consistency(self):
        """Test that normalization works consistently across different signals."""
        # Test multiple signals of different amplitudes
        test_signals = [
            self.sine_wave_440hz * 0.1,   # Low amplitude
            self.sine_wave_440hz * 0.5,   # Medium amplitude
            self.sine_wave_440hz * 1.0,   # Full amplitude
            self.sine_wave_440hz * 2.0,   # Over-amplitude
        ]
        
        for signal in test_signals:
            result = self.fft_processor.process(signal)
            
            # Maximum should always be normalized to 1.0
            self.assertAlmostEqual(np.max(result), 1.0, places=5)
            
            # All values should be between 0 and 1
            self.assertTrue(np.all(result >= 0))
            self.assertTrue(np.all(result <= 1))
    
    def test_empty_input_handling(self):
        """Test handling of edge cases with empty or invalid input."""
        # Test with empty array
        empty_signal = np.array([])
        
        try:
            result = self.fft_processor.process(empty_signal)
            # If no exception, result should be empty
            self.assertEqual(len(result), 0)
        except Exception:
            # Exception is acceptable for empty input
            pass
    
    def test_zero_max_handling(self):
        """Test handling when FFT result has zero maximum."""
        # This tests the division by zero protection
        zero_signal = np.zeros(BUFFER_SIZE)
        result = self.fft_processor.process(zero_signal)
        
        # Should return the original FFT (all zeros) without division
        self.assertIsInstance(result, np.ndarray)
        np.testing.assert_allclose(result, 0, atol=1e-10)
    
    def test_fft_output_properties(self):
        """Test mathematical properties of FFT output."""
        result = self.fft_processor.process(self.sine_wave_440hz)
        
        # Real FFT should have specific length
        expected_length = BUFFER_SIZE // 2 + 1
        self.assertEqual(len(result), expected_length)
        
        # All values should be real and non-negative (magnitude)
        self.assertTrue(np.all(np.isreal(result)))
        self.assertTrue(np.all(result >= 0))
        
        # Should be finite values
        self.assertTrue(np.all(np.isfinite(result)))
    
    def test_frequency_resolution(self):
        """Test that frequency resolution is correct."""
        # Create a signal with known frequency content
        test_freq = 1000  # 1 kHz
        test_signal = np.sin(2 * np.pi * test_freq * self.time)
        
        result = self.fft_processor.process(test_signal)
        
        # Calculate frequency bins
        frequencies = np.fft.rfftfreq(BUFFER_SIZE, 1/self.sample_rate)
        
        # Find peak
        peak_index = np.argmax(result)
        detected_frequency = frequencies[peak_index]
        
        # Should be close to our test frequency
        frequency_resolution = self.sample_rate / BUFFER_SIZE
        self.assertLess(abs(detected_frequency - test_freq), frequency_resolution)
    
    def test_process_different_buffer_sizes(self):
        """Test processing with different input sizes."""
        # Test with smaller buffer
        small_signal = self.sine_wave_440hz[:512]  # Half size
        result_small = self.fft_processor.process(small_signal)
        
        # Should work and return appropriate size
        expected_small_length = 512 // 2 + 1
        self.assertEqual(len(result_small), expected_small_length)
        self.assertAlmostEqual(np.max(result_small), 1.0, places=5)
        
        # Test with larger buffer (if input is larger than BUFFER_SIZE)
        large_signal = np.tile(self.sine_wave_440hz, 2)  # Double size
        result_large = self.fft_processor.process(large_signal)
        
        # Should work and return appropriate size
        expected_large_length = len(large_signal) // 2 + 1
        self.assertEqual(len(result_large), expected_large_length)
        self.assertAlmostEqual(np.max(result_large), 1.0, places=5)
    
    def test_real_world_audio_characteristics(self):
        """Test with audio characteristics similar to real-world scenarios."""
        # Test with noise
        noise = np.random.normal(0, 0.1, BUFFER_SIZE)
        result_noise = self.fft_processor.process(noise)
        
        # Should be normalized and finite
        self.assertAlmostEqual(np.max(result_noise), 1.0, places=5)
        self.assertTrue(np.all(np.isfinite(result_noise)))
        
        # Test with music-like signal (multiple harmonics)
        fundamental = 220  # A3
        harmonics = np.sin(2 * np.pi * fundamental * self.time)
        harmonics += 0.5 * np.sin(2 * np.pi * 2 * fundamental * self.time)  # 2nd harmonic
        harmonics += 0.25 * np.sin(2 * np.pi * 3 * fundamental * self.time)  # 3rd harmonic
        
        result_harmonics = self.fft_processor.process(harmonics)
        
        # Should show peaks at harmonic frequencies
        frequencies = np.fft.rfftfreq(BUFFER_SIZE, 1/self.sample_rate)
        
        # Find peaks
        peaks = []
        for i in range(1, len(result_harmonics) - 1):
            if (result_harmonics[i] > result_harmonics[i-1] and 
                result_harmonics[i] > result_harmonics[i+1] and
                result_harmonics[i] > 0.1):
                peaks.append(frequencies[i])
        
        # Should have detected some harmonic content
        self.assertGreater(len(peaks), 0)

if __name__ == '__main__':
    unittest.main()
