import logging
from pythonjsonlogger import jsonlogger
from pathlib import Path
import os
from datetime import datetime
import json


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super(CustomJsonFormatter, self).add_fields(log_record, record, message_dict)
        if not log_record.get('timestamp'):
            # this doesn't use record.created, so it is slightly off
            now = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            log_record['timestamp'] = now
        if log_record.get('level'):
            log_record['level'] = log_record['level'].upper()
        else:
            log_record['level'] = record.levelname

class JsonLogger:
    @staticmethod
    def create_logger(log_file: str,
                      logger_name: str = __name__) -> logging.Logger:
        Path(os.path.dirname(log_file)).mkdir(parents=True, exist_ok=True)
        logger = logging.getLogger(logger_name)
        logHandler = logging.FileHandler(log_file)
        formatter = CustomJsonFormatter('%(timestamp)s %(level)s %(name)s',
            json_encoder=json.JSONEncoder,
                                        json_indent=4,
                                        json_ensure_ascii=False)

        logHandler.setFormatter(formatter)
        logger.addHandler(logHandler)
        logger.setLevel(logging.DEBUG)

        return logger