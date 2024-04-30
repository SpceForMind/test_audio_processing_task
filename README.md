# test_audio_processing_task
test_audio_processing_task

### Requirements:
+ Python 3.10.12
+ pip 23.2.1
+ ffmpeg version 4.4.2-0ubuntu0.22.04.1

```
sudo apt-get install ffmpeg
pip install -r requirements.txt
```

### Enviroment

+ Настройте опции модели распознавания
```
# medium / large-v2 / base
model_size=base

# int8 / float32
compute_type=int8

# размер батча, устанавливается по требованиям системы
batch_size=8

# если есть гпу, установлена куда, выбрать cuda
device=cpu

# Путь к лог файлу для процесса расшифровки
log='data/logs/stt.log'
```
+ *Path*: `.env`

### Run Scripts
+ Распознавание аудио

`python -m stt.whisperx_stt --audio_path data/audio/test_audio.wav --transcript_dir data/transcripts`

Здесь `audio_path` - путь к аудио, `transcript_dir` путь к директории с транскриптами. Имя файла транскрипта 
будет повторять имя аудиофайла. Настроена обработка ошибок на случай сломанного аудио(т.к. нужен транскрипт, пусть даже пустой)

Посмотреть логи можно в `data/logs/stt.log`(по умолчанию)

+ Преобразование аудио

Запуск

`
python -m audio_utils.audio_processor --audio_path data/audio/test_audio.wav --speed_scale 1.2 --vol_scale 1.2
`

Здесь `audio_path` - путь к аудио, `speed_scale` - скорость воспроизведения(1.5 - в полтора раза), `vol_scale` - 
громкость воспроизведения (1.5 - в полтора раза). Так как выходной результат аудиозапись, если передать что-то некорректное(типо текстового файла),
то будет выброшена ошибка, выходной файл получен не будет

Результат работы(файл сохраняется в директорию с исходной аудиозаписью, выходной файл в имени содержит апгрейды по скорости и громкости + имя файла из команды):

`ut file path: data/audio/1.2_vol_1.2_speed_test_audio.wav`

### Testing
`python -m tests`

