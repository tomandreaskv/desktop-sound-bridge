import unittest
from unittest.mock import patch

import sonos_gui


class SonosGuiTests(unittest.TestCase):
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


if __name__ == "__main__":
    unittest.main()
