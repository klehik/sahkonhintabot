import logging, logging.handlers


def init_logger():

    # get logger    
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    # formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    
    # handlers
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    
    file_handler = logging.FileHandler(f"sahkobot.log")
    file_handler.setFormatter(formatter)
    
    # add handlers to logger
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)