import unittest
import numpy as np
from unittest.mock import Mock, patch, MagicMock
from core.audio_input import AudioInput
from config.config import SAMPLE_RATE, BUFFER_SIZE

class TestAudioInput(unittest.TestCase):
    """Unit tests for AudioInput class."""
    
    def setUp(self):
        """Set up test fixtures."""
        # Mock sounddevice to avoid requiring actual audio hardware
        self.mock_sd_patcher = patch('core.audio_input.sd')
        self.mock_sd = self.mock_sd_patcher.start()
        
        # Create mock stream
        self.mock_stream = Mock()
        self.mock_sd.InputStream.return_value = self.mock_stream
        
    def test_audio_input_initialization(self):
        """Test AudioInput initializes correctly."""
        audio_input = AudioInput()
        
        # Verify InputStream was called with correct parameters
        self.mock_sd.InputStream.assert_called_once_with(
            samplerate=SAMPLE_RATE,
            blocksize=BUFFER_SIZE,
            dtype=np.float32
        )
        
        # Verify stream was started
        self.mock_stream.start.assert_called_once()
        
        # Verify audio_input has stream attribute
        self.assertEqual(audio_input.stream, self.mock_stream)
    
    def test_get_audio_chunk_success(self):
        """Test successful audio chunk retrieval."""
        audio_input = AudioInput()
        
        # Mock successful audio data
        mock_audio_data = np.random.rand(BUFFER_SIZE, 1).astype(np.float32)
        overflowed = False
        self.mock_stream.read.return_value = (mock_audio_data, overflowed)
        
        # Get audio chunk
        result = audio_input.get_audio_chunk()
        
        # Verify stream.read was called with correct buffer size
        self.mock_stream.read.assert_called_once_with(BUFFER_SIZE)
        
        # Verify result is flattened numpy array
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(len(result), BUFFER_SIZE)
        self.assertEqual(result.dtype, np.float32)
        
        # Verify data was flattened correctly
        expected_result = mock_audio_data.flatten()
        np.testing.assert_array_equal(result, expected_result)
    
    def test_get_audio_chunk_with_overflow(self):
        """Test audio chunk retrieval with buffer overflow."""
        audio_input = AudioInput()
        
        # Mock audio data with overflow
        mock_audio_data = np.random.rand(BUFFER_SIZE, 1).astype(np.float32)
        overflowed = True
        self.mock_stream.read.return_value = (mock_audio_data, overflowed)
        
        # Get audio chunk (should still work despite overflow)
        result = audio_input.get_audio_chunk()
        
        # Verify result is still valid
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(len(result), BUFFER_SIZE)
    
    def test_get_audio_chunk_exception_handling(self):
        """Test audio chunk retrieval handles exceptions gracefully."""
        audio_input = AudioInput()
        
        # Mock stream.read to raise an exception
        self.mock_stream.read.side_effect = Exception("Audio device error")
        
        # Get audio chunk should return zeros array on exception
        result = audio_input.get_audio_chunk()
        
        # Verify result is zeros array with correct size
        self.assertIsInstance(result, np.ndarray)
        self.assertEqual(len(result), BUFFER_SIZE)
        np.testing.assert_array_equal(result, np.zeros(BUFFER_SIZE))
    
    def test_audio_level_calculation(self):
        """Test audio level calculation and visualization."""
        audio_input = AudioInput()
        
        # Mock audio data with known amplitude
        test_amplitude = 0.5
        mock_audio_data = np.full((BUFFER_SIZE, 1), test_amplitude, dtype=np.float32)
        overflowed = False
        self.mock_stream.read.return_value = (mock_audio_data, overflowed)
        
        # Capture print output to verify debug visualization
        with patch('builtins.print') as mock_print:
            result = audio_input.get_audio_chunk()
            
            # Verify level calculation
            expected_level = np.abs(result).mean()
            self.assertAlmostEqual(expected_level, test_amplitude, places=5)
            
            # Verify print was called (debug visualization)
            mock_print.assert_called()
            
            # Check that the print call contains level information
            print_args = mock_print.call_args[0][0]
            self.assertIn("Input Level:", print_args)
    
    def test_close_stream(self):
        """Test stream cleanup on close."""
        audio_input = AudioInput()
        
        # Close the stream
        audio_input.close()
        
        # Verify stream was stopped and closed
        self.mock_stream.stop.assert_called_once()
        self.mock_stream.close.assert_called_once()
    
    def test_close_stream_without_stream(self):
        """Test close method when no stream exists."""
        audio_input = AudioInput()
        
        # Remove stream attribute to simulate edge case
        delattr(audio_input, 'stream')
        
        # Close should not raise an exception
        try:
            audio_input.close()
        except Exception as e:
            self.fail(f"close() raised an exception when no stream exists: {e}")
    
    def test_close_stream_with_none_stream(self):
        """Test close method when stream is None."""
        audio_input = AudioInput()
        audio_input.stream = None
        
        # Close should not raise an exception
        try:
            audio_input.close()
        except Exception as e:
            self.fail(f"close() raised an exception when stream is None: {e}")
    
    def test_multiple_audio_chunks(self):
        """Test retrieving multiple audio chunks in sequence."""
        audio_input = AudioInput()
        
        # Mock different audio data for each call
        chunk1_data = np.random.rand(BUFFER_SIZE, 1).astype(np.float32)
        chunk2_data = np.random.rand(BUFFER_SIZE, 1).astype(np.float32)
        chunk3_data = np.random.rand(BUFFER_SIZE, 1).astype(np.float32)
        
        self.mock_stream.read.side_effect = [
            (chunk1_data, False),
            (chunk2_data, False),
            (chunk3_data, False)
        ]
        
        # Get multiple chunks
        result1 = audio_input.get_audio_chunk()
        result2 = audio_input.get_audio_chunk()
        result3 = audio_input.get_audio_chunk()
        
        # Verify each result is different and correct
        self.assertFalse(np.array_equal(result1, result2))
        self.assertFalse(np.array_equal(result2, result3))
        
        np.testing.assert_array_equal(result1, chunk1_data.flatten())
        np.testing.assert_array_equal(result2, chunk2_data.flatten())
        np.testing.assert_array_equal(result3, chunk3_data.flatten())
        
        # Verify stream.read was called three times
        self.assertEqual(self.mock_stream.read.call_count, 3)
    
    def test_audio_data_types(self):
        """Test handling of different audio data shapes and types."""
        audio_input = AudioInput()
        
        # Test with mono audio (already correct shape)
        mono_data = np.random.rand(BUFFER_SIZE, 1).astype(np.float32)
        self.mock_stream.read.return_value = (mono_data, False)
        
        result = audio_input.get_audio_chunk()
        self.assertEqual(len(result), BUFFER_SIZE)
        self.assertEqual(result.dtype, np.float32)
    
    def test_configuration_values(self):
        """Test that configuration values are used correctly."""
        # Test that AudioInput uses the correct config values
        audio_input = AudioInput()
        
        # Verify InputStream was called with config values
        call_args = self.mock_sd.InputStream.call_args
        self.assertEqual(call_args[1]['samplerate'], SAMPLE_RATE)
        self.assertEqual(call_args[1]['blocksize'], BUFFER_SIZE)
        self.assertEqual(call_args[1]['dtype'], np.float32)

if __name__ == '__main__':
    unittest.main()
