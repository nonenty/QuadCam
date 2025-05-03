import logging

def create_log(name,level,filename,sh_level,fh_level):
    log = logging.getLogger(name)

    log.setLevel(level=level)

    sh = logging.StreamHandler()
    sh.setLevel(level=sh_level)
    log.addHandler(sh)
    fh = logging.FileHandler(filename=filename,encoding="utf-8")

    fh.setLevel(level=fh_level)
    log.addHandler(fh)

    formats = "%(asctime)s - [%(filename)s-->line:%(lineno)d] - %(levelname)s:%(message)s"
    log_format = logging.Formatter(fmt=formats)
    sh.setFormatter(log_format)
    fh.setFormatter(log_format)
    return log
 

log = create_log(name="rose_log",level=logging.DEBUG,filename="test_log.log",sh_level=logging.DEBUG,fh_level=logging.DEBUG)
