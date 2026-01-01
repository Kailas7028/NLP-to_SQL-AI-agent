import logging
from datetime import datetime
import json


class JsonFormater(logging.Formatter):


    def format(self,record):

        log={
            "timestamp":datetime.now().isoformat(),
            "level":record.levelname,
            "message":record.getMessage(),
            "module":record.module
        }

        if hasattr(record,"extra"):
            log.update(record.extra)
            
        return json.dumps(log)
    
    

def get_logger(name:str):
    logger=logging.getLogger(name)
    logger.setLevel(logging.INFO)

    handler=logging.StreamHandler()
    handler.setFormatter(JsonFormater())

    if not logger.handlers:
        logger.addHandler(handler)
    return logger
