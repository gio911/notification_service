import logging


def setup_logging():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)  # Устанавливаем уровень логирования
    ch = logging.StreamHandler()  # Выводим логи в консоль
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    return logger
