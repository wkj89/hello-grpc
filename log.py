import logging


def init_log():
    file_handler = logging.FileHandler("/tmp/grpc.log")
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('[%(asctime)s] - %(levelname)s -%(filename)s -%(lineno)d - %(message)s')

    file_handler.setFormatter(formatter)
    logging.getLogger().addHandler(file_handler)
    logging.getLogger().setLevel(logging.INFO)
