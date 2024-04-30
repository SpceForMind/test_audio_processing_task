import os.path
import typing

import whisperx
import argparse
import traceback

from stt.config.whisperx_config import WhisperxConfig

from loggers.json_logger import JsonLogger

from audio_utils.wav_utils import WavUtils

class WhisperxStt:
    def __init__(self,
                 path_to_env: str):
        self.__config = WhisperxConfig(path_to_env=path_to_env)
        self.__logger = JsonLogger.create_logger(
            logger_name='stt-logger',
            log_file=self.__config.get_log_file_path()
        )
        self._setup_model()

    def _setup_model(self):
        print(f'Load model: {self.__config.get_model_size()}')
        self.__model = whisperx.load_model(
            self.__config.get_model_size(),
            device=self.__config.get_device(),
            compute_type=self.__config.get_compute_type()
        )
        print(f'Model loaded!')

    def _transcribe_wav(self,
                        wav_path: str):
        audio = whisperx.load_audio(wav_path)
        try:
            result = self.__model.transcribe(
                audio=audio,
                batch_size=self.__config.get_batch_size(),
            )
        except Exception as err:
            self.__logger.error({"error": repr(err),
                                 "traceback": traceback.format_tb(err.__traceback__)})
            result = {
                "segments": []
            }

        return result

    def _write_transcript(self,
                          path: str,
                          result: typing.List[dict]):
        with open(path, 'w') as f:
            f.write(' '.join([_['text'] for _ in result]))

        print('Transcript file:', path)

    def process_audio(self,
                      audio_path: str,
                      transcript_dir: str):
        transcript_path = os.path.join(transcript_dir, f"{os.path.basename(audio_path).split('.')[0]}.txt")
        try:
            converted_to_wav_tfile = WavUtils.convert_to_wav(filepath=audio_path)
        except Exception as err:
            self.__logger.error({"error": repr(err),
                                 "traceback": traceback.format_tb(err.__traceback__)})
            self.__logger.debug(f'Cannot convert file: {audio_path} to wav')
            self._write_transcript(path=transcript_path, result=[])

            return []

        cutted_tfiles_list = WavUtils.cut_wav_file(filepath=converted_to_wav_tfile, chunk_seconds=30)
        converted_to_wav_tfile.close()
        results = []

        for tfile in cutted_tfiles_list:
            result = self._transcribe_wav(tfile.name)
            results.append(result)
            tfile.close()

        out_result = []

        offset = 0

        for transcript in results:
            for seg in transcript["segments"]:
                out_result.append({
                    "text": seg["text"],
                    "start": seg["start"] + offset,
                    "end": seg["end"] + offset
                })

            if transcript["segments"]:
                offset += transcript["segments"][-1]["end"]

        self.__logger.debug({"transcript": out_result})
        print(out_result)
        self._write_transcript(path=transcript_path, result=out_result)

        return out_result


def parse_args():
    parser = argparse.ArgumentParser(description='tts')
    parser.add_argument('--audio_path',
                        action="store",
                        type=str,
                        dest="audio_path",
                        required=True)
    parser.add_argument('--transcript_dir',
                        action="store",
                        type=str,
                        dest="transcript_dir",
                        required=True)

    return parser.parse_args()

        
if __name__ == '__main__':
    args = parse_args()
    model = WhisperxStt(path_to_env='.env')
    model.process_audio(audio_path=args.audio_path,
                        transcript_dir=args.transcript_dir)