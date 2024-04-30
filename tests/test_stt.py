import unittest

from stt.whisperx_stt import WhisperxStt


model = WhisperxStt(path_to_env='.env')


class TestStt(unittest.TestCase):
    def test_sil_audio(self):
        result = model.process_audio('data/audio/sil.ogg', transcript_dir='data/transcripts')
        result = model.process_audio('data/audio/sil.wav', transcript_dir='data/transcripts')

    def test_non_sil_audios(self):
        result = model.process_audio('data/audio/ytmp3-convert.com_128kbps-prikol-po-telefonu-prodazha-avto.mp3',
                                     transcript_dir='data/transcripts')
        result = model.process_audio('data/audio/test_audio.wav', transcript_dir='data/transcripts')

    def test_broken_audio(self):
        result = model.process_audio('data/audio/broken_audio.wav', transcript_dir='data/transcripts')


if __name__ == '__main__':
    unittest.main()
