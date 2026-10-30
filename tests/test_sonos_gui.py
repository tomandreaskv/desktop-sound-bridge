import unittest
import queue
from unittest.mock import MagicMock, patch

import sonos_gui


class SonosGuiTests(unittest.TestCase):
    def setUp(self):
        while True:
            try:
                sonos_gui.audio_errors.get_nowait()
            except queue.Empty:
                break

    def test_wav_header_contains_expected_pcm_format(self):
        header = sonos_gui.get_wav_header(44100, 2, 16)

        self.assertEqual(len(header), 44)
        self.assertEqual(header[:4], b"RIFF")
        self.assertEqual(header[8:12], b"WAVE")
        self.assertEqual(header[12:16], b"fmt ")
        self.assertEqual(int.from_bytes(header[22:24], "little"), 2)
        self.assertEqual(int.from_bytes(header[24:28], "little"), 44100)
        self.assertEqual(int.from_bytes(header[34:36], "little"), 16)

    def test_stream_requires_session_token(self):
        client = sonos_gui.app.test_client()

        with patch.object(sonos_gui, "generate_audio_stream") as generate_stream:
            response = client.get("/stream.wav")

        self.assertEqual(response.status_code, 401)
        generate_stream.assert_not_called()

    def test_stream_accepts_session_token(self):
        client = sonos_gui.app.test_client()

        with patch.object(sonos_gui, "generate_audio_stream", return_value=iter([b"pcm"])):
            response = client.get(f"/stream.wav?token={sonos_gui.STREAM_TOKEN}")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "audio/x-wav")
        self.assertEqual(response.data, b"pcm")

    def test_audio_device_error_is_reported(self):
        with patch.object(sonos_gui.sc, "default_speaker", side_effect=RuntimeError("device unavailable")):
            self.assertEqual(list(sonos_gui.generate_audio_stream()), [])

        self.assertIn("device unavailable", sonos_gui.audio_errors.get_nowait())

    def test_recording_error_is_reported_after_wav_header(self):
        recorder = MagicMock()
        recorder.record.side_effect = RuntimeError("recording failed")
        microphone = MagicMock()
        microphone.recorder.return_value = MagicMock()
        microphone.recorder.return_value.__enter__.return_value = recorder

        with patch.object(sonos_gui.sc, "default_speaker") as default_speaker, patch.object(
            sonos_gui.sc, "get_microphone", return_value=microphone
        ):
            default_speaker.return_value.name = "Default speaker"
            chunks = list(sonos_gui.generate_audio_stream())

        self.assertEqual(len(chunks), 1)
        self.assertTrue(chunks[0].startswith(b"RIFF"))
        self.assertIn("recording failed", sonos_gui.audio_errors.get_nowait())


if __name__ == "__main__":
    unittest.main()
