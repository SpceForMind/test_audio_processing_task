import wave
import numpy as np
import tempfile
import pydub
import librosa
import typing
from pydub import AudioSegment
from pydub.silence import detect_silence


class WavUtils:
    __silence_len_ms = 150
    __interval_duration_ms_th = 1000
    __drop_last_interval_ms_th = 500
    __get_audio_tail_th = 0.3
    __db_th_1 = -24
    __db_th_2 = -48
    __db_th_3 = -32

    @staticmethod
    def convert_to_wav(filepath: str) -> tempfile.NamedTemporaryFile:
        audio = AudioSegment.from_file(filepath)
        tfile = tempfile.NamedTemporaryFile(suffix='.wav')
        audio.export(tfile.name, format='wav')

        return tfile

    @staticmethod
    def find_sil_frames(audio: AudioSegment):
        sil_chunks = detect_silence(
            audio,
            min_silence_len=WavUtils.__silence_len_ms,
            silence_thresh=WavUtils.__db_th_2
        )

        if not sil_chunks:
            sil_chunks = detect_silence(
                audio,
                min_silence_len=WavUtils.__silence_len_ms,
                silence_thresh=WavUtils.__db_th_3
            )

        if not sil_chunks:
            sil_chunks = detect_silence(
                audio,
                min_silence_len=WavUtils.__silence_len_ms,
                silence_thresh=WavUtils.__db_th_1
            )

        return sil_chunks

    @staticmethod
    def cut_wav_file(filepath: str,
                     chunk_seconds: int) -> typing.List[tempfile.NamedTemporaryFile]:
        duration = librosa.get_duration(filename=filepath)
        # print(duration)
        count_chunks = int(duration / chunk_seconds) + 1
        count_chunks_float = duration / chunk_seconds
        # print(count_chunks_float)
        audio = pydub.AudioSegment.from_wav(file=filepath)
        last_sil_frame = 0
        cut_ended = False
        chunks = []

        if count_chunks > 1:
            while True:
                if last_sil_frame + chunk_seconds * 1000 >= count_chunks * chunk_seconds * 1000:
                    new_last_sil = count_chunks * chunk_seconds * 1000
                    cut_ended = True
                else:
                    sil_frames = WavUtils.find_sil_frames(audio[last_sil_frame: last_sil_frame + chunk_seconds * 1000])

                    if sil_frames:
                        new_last_sil = sil_frames[-1]
                        mediana = int((new_last_sil[0] + new_last_sil[1]) / 2)
                        new_last_sil = mediana
                    else:
                        new_last_sil = last_sil_frame + chunk_seconds * 1000

                    if abs(last_sil_frame + new_last_sil - int(count_chunks_float * chunk_seconds * 1000)) < \
                        WavUtils.__get_audio_tail_th * chunk_seconds * 1000:
                        new_last_sil += WavUtils.__get_audio_tail_th * chunk_seconds * 1000
                        new_last_sil = int(new_last_sil)
                        cut_ended = True

                # print(new_last_sil + last_sil_frame)

                chunk_audio = audio[last_sil_frame: last_sil_frame + new_last_sil]
                last_sil_frame += new_last_sil
                tfile = tempfile.NamedTemporaryFile(suffix='.wav')
                chunk_audio.export(out_f=tfile.name, format='wav')
                # chunk_audio.export(out_f=f'tests/data/{i}-chunk.wav', format='wav')
                # i += 1
                chunks.append(tfile)

                if cut_ended:
                    break
        else:
            tfile = tempfile.NamedTemporaryFile(suffix='.wav')
            audio.export(out_f=tfile.name, format='wav')
            chunks.append(tfile)

        return chunks


if __name__ == '__main__':
    print(WavUtils.cut_wav_file(
        filepath='data/call_19687.wav',
        chunk_seconds=20
    ))
