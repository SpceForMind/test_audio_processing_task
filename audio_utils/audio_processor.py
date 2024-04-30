import librosa
import os
import soundfile
from pydub import AudioSegment
import argparse


class AudioProcessor:
    @staticmethod
    def change_audio_speed(audio_path: str,
                           speed_scale: float) -> str:
        audio, sr = librosa.load(audio_path)
        changed_audio = librosa.effects.time_stretch(y=audio, rate=speed_scale)
        out_path = os.path.join(os.path.dirname(audio_path),
                                f"{speed_scale}_speed_{os.path.basename(audio_path)}")
        soundfile.write(out_path, changed_audio, sr)

        return out_path

    @staticmethod
    def change_audio_vol(audio_path: str,
                         vol_scale: float) -> str:
        audio = AudioSegment.from_file(file=audio_path)
        target_dBFS = audio.dBFS * vol_scale
        normalized_audio = audio.apply_gain(audio.dBFS - target_dBFS)
        out_path = os.path.join(os.path.dirname(audio_path),
                                f"{vol_scale}_vol_{os.path.basename(audio_path)}")
        normalized_audio.export(out_path, format="wav")
        return out_path


def parse_args():
    parser = argparse.ArgumentParser(description='audio processing utils')
    parser.add_argument('--audio_path',
                        action="store",
                        type=str,
                        dest="audio_path",
                        required=True)
    parser.add_argument('--vol_scale',
                        action="store",
                        type=float,
                        dest="vol_scale",
                        required=False,
                        default=1.0)
    parser.add_argument('--speed_scale',
                        action="store",
                        type=float,
                        dest='speed_scale',
                        required=False,
                        default=1.0)

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    audio_path = args.audio_path
    speed_scale = args.speed_scale
    vol_scale = args.vol_scale

    speed_scaled_path = AudioProcessor.change_audio_speed(
        audio_path=audio_path,
        speed_scale=speed_scale
    )
    vol_and_speed_scaled_path = AudioProcessor.change_audio_vol(
        audio_path=speed_scaled_path,
        vol_scale=vol_scale
    )
    os.remove(speed_scaled_path)

    print('Out file path:', vol_and_speed_scaled_path)

        
