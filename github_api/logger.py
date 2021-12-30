import logging


def setup_logger(name, logfile="LOGFILENAME.txt"):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler(logfile)
    fh.setLevel(logging.DEBUG)
    fh_formatter = logging.Formatter("%(asctime)s - %(levelname)8s - %(message)s")
    fh.setFormatter(fh_formatter)

    logger.addHandler(fh)
    return logger
