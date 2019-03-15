
import logging


def init_system_logger():

    formatter = logging.Formatter('[%(asctime)s] - %(levelname)s -%(filename)s -%(lineno)d - %(message)s')


    file_handler = logging.FileHandler('/tmp/grpc.log')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logging.getLogger().addHandler(file_handler)
    logging.getLogger().setLevel(logging.INFO)
