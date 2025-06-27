import unittest
import numpy as np
from unittest.mock import Mock, patch, MagicMock
from core.audio_input import AudioInput
from config.config import SAMPLE_RATE, BUFFER_SIZE

class TestAudioInputFailures(unittest.TestCase):
    """Unit tests for AudioInput class - MODIFIED TO FAIL for educational purposes."""
    
    # def setUp(self):
    #     """Set up test fixtures."""
    #     # Mock sounddevice to avoid requiring actual audio hardware
    #     self.mock_sd_patcher = patch('core.audio_input.sd')
    #     self.mock_sd = self.mock_sd_patcher.start()
        
    #     # Create mock stream
    #     self.mock_stream = Mock()
    #     self.mock_sd.InputStream.return_value = self.mock_stream
        

    
    def test_audio_input_initialization_FAIL(self):
        """Test AudioInput initializes correctly - MODIFIED TO FAIL."""
        audio_input = AudioInput()
        
        # FAIL REASON: Expecting wrong sample rate
        self.mock_sd.InputStream.assert_called_once_with(
            samplerate=48000,  # WRONG! Should be SAMPLE_RATE (44100)
            blocksize=BUFFER_SIZE,
            dtype=np.float32
        )
        # WHY IT FAILS: AudioInput uses 44100 Hz, but we're checking for 48000 Hz
    
    def test_get_audio_chunk_success_FAIL(self):
        """Test successful audio chunk retrieval - MODIFIED TO FAIL."""
        audio_input = AudioInput()
        
        # Mock successful audio data
        mock_audio_data = np.random.rand(BUFFER_SIZE, 1).astype(np.float32)
        overflowed = False
        self.mock_stream.read.return_value = (mock_audio_data, overflowed)
        
        # Get audio chunk
        result = audio_input.get_audio_chunk()
        
        # FAIL REASON: Expecting wrong length
        self.assertEqual(len(result), BUFFER_SIZE * 2)  # WRONG! Should be BUFFER_SIZE
        # WHY IT FAILS: Result is flattened to BUFFER_SIZE, not doubled
    
    def test_get_audio_chunk_with_overflow_FAIL(self):
        """Test audio chunk retrieval with buffer overflow - MODIFIED TO FAIL."""
        audio_input = AudioInput()
        
        # Mock audio data with overflow
        mock_audio_data = np.random.rand(BUFFER_SIZE, 1).astype(np.float32)
        overflowed = True
        self.mock_stream.read.return_value = (mock_audio_data, overflowed)
        
        # Get audio chunk
        result = audio_input.get_audio_chunk()
        
        # FAIL REASON: Expecting None when overflow occurs
        self.assertIsNone(result)  # WRONG! Should return valid array even on overflow
        # WHY IT FAILS: AudioInput returns data even when overflow=True
    
    def test_get_audio_chunk_exception_handling_FAIL(self):
        """Test audio chunk retrieval handles exceptions - MODIFIED TO FAIL."""
        audio_input = AudioInput()
        
        # Mock stream.read to raise an exception
        self.mock_stream.read.side_effect = Exception("Audio device error")
        
        # Get audio chunk
        result = audio_input.get_audio_chunk()
        
        # FAIL REASON: Expecting exception to propagate
        self.assertIsNone(result)  # WRONG! Should return zeros array, not None
        # WHY IT FAILS: AudioInput catches exceptions and returns np.zeros(BUFFER_SIZE)
    
    def test_audio_level_calculation_FAIL(self):
        """Test audio level calculation - MODIFIED TO FAIL."""
        audio_input = AudioInput()
        
        # Mock audio data with known amplitude
        test_amplitude = 0.5
        mock_audio_data = np.full((BUFFER_SIZE, 1), test_amplitude, dtype=np.float32)
        overflowed = False
        self.mock_stream.read.return_value = (mock_audio_data, overflowed)
        
        with patch('builtins.print') as mock_print:
            result = audio_input.get_audio_chunk()
            
            # FAIL REASON: Expecting wrong amplitude
            expected_level = np.abs(result).mean()
            self.assertAlmostEqual(expected_level, 0.8, places=5)  # WRONG! Should be 0.5
            # WHY IT FAILS: We set amplitude to 0.5, but checking for 0.8
    
    def test_close_stream_FAIL(self):
        """Test stream cleanup on close - MODIFIED TO FAIL."""
        audio_input = AudioInput()
        
        # Close the stream
        audio_input.close()
        
        # FAIL REASON: Expecting wrong method to be called
        self.mock_stream.shutdown.assert_called_once()  # WRONG! No 'shutdown' method
        # WHY IT FAILS: AudioInput calls 'stop()' and 'close()', not 'shutdown()'
    
    def test_close_stream_without_stream_FAIL(self):
        """Test close method when no stream exists - MODIFIED TO FAIL."""
        audio_input = AudioInput()
        
        # Remove stream attribute
        delattr(audio_input, 'stream')
        
        # FAIL REASON: Expecting exception to be raised
        with self.assertRaises(AttributeError):  # WRONG! Should handle gracefully
            audio_input.close()
        # WHY IT FAILS: AudioInput has defensive programming to handle missing stream
    
    def test_close_stream_with_none_stream_FAIL(self):
        """Test close method when stream is None - MODIFIED TO FAIL."""
        audio_input = AudioInput()
        audio_input.stream = None
        
        # FAIL REASON: Expecting exception when stream is None
        with self.assertRaises(AttributeError):  # WRONG! Should handle None gracefully
            audio_input.close()
        # WHY IT FAILS: AudioInput checks 'if self.stream:' before calling methods
    
    def test_multiple_audio_chunks_FAIL(self):
        """Test retrieving multiple audio chunks - MODIFIED TO FAIL."""
        audio_input = AudioInput()
        
        # Use SAME data for all calls (instead of different)
        same_data = np.random.rand(BUFFER_SIZE, 1).astype(np.float32)
        
        self.mock_stream.read.side_effect = [
            (same_data, False),
            (same_data, False),  # SAME data, not different!
            (same_data, False)
        ]
        
        result1 = audio_input.get_audio_chunk()
        result2 = audio_input.get_audio_chunk()
        
        # FAIL REASON: Expecting different results when they're the same
        self.assertFalse(np.array_equal(result1, result2))  # WRONG! They are equal
        # WHY IT FAILS: We deliberately used the same mock data for both calls
    
    def test_audio_data_types_FAIL(self):
        """Test handling of audio data types - MODIFIED TO FAIL."""
        audio_input = AudioInput()
        
        # Test with mono audio
        mono_data = np.random.rand(BUFFER_SIZE, 1).astype(np.float32)
        self.mock_stream.read.return_value = (mono_data, False)
        
        result = audio_input.get_audio_chunk()
        
        # FAIL REASON: Expecting wrong data type
        self.assertEqual(result.dtype, np.int16)  # WRONG! Should be float32
        # WHY IT FAILS: AudioInput returns float32, not int16
    
    def test_configuration_values_FAIL(self):
        """Test configuration values - MODIFIED TO FAIL."""
        audio_input = AudioInput()
        
        # FAIL REASON: Checking for wrong config values
        call_args = self.mock_sd.InputStream.call_args
        self.assertEqual(call_args[1]['samplerate'], 22050)  # WRONG! Should be 44100
        self.assertEqual(call_args[1]['blocksize'], 1024)    # WRONG! Should be 2048
        # WHY IT FAILS: We're checking for wrong configuration constants

if __name__ == '__main__':
    unittest.main()