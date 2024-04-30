import unittest

from audio_utils.audio_processor import AudioProcessor


class TestStt(unittest.TestCase):
    def test_sil_audio(self):
        r = AudioProcessor.change_audio_vol(audio_path='data/audio/sil.ogg', vol_scale=1.5)
        print('Out file:', r)
        r = AudioProcessor.change_audio_vol(audio_path='data/audio/sil.wav', vol_scale=0.5)
        print('Out file:', r)
        r = AudioProcessor.change_audio_speed(audio_path='data/audio/sil.ogg', speed_scale=1.5)
        print('Out file:', r)
        r = AudioProcessor.change_audio_speed(audio_path='data/audio/sil.wav', speed_scale=0.5)
        print('Out file:', r)

    def test_non_sil_audios(self):
        r = AudioProcessor.change_audio_vol(
            audio_path='data/audio/ytmp3-convert.com_128kbps-prikol-po-telefonu-prodazha-avto.mp3',
            vol_scale=1.6
        )
        print('Out file:', r)
        r = AudioProcessor.change_audio_vol(
            audio_path='data/audio/test_audio.wav',
            vol_scale=0.3
        )
        print('Out file:', r)
        r = AudioProcessor.change_audio_speed(
            audio_path='data/audio/ytmp3-convert.com_128kbps-prikol-po-telefonu-prodazha-avto.mp3',
            speed_scale=1.2
        )
        print('Out file:', r)
        r = AudioProcessor.change_audio_speed(
            audio_path='data/audio/test_audio.wav',
            speed_scale=0.7
        )
        print('Out file:', r)


if __name__ == '__main__':
    unittest.main()
