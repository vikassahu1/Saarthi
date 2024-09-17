log_level = logging.DEBUG
log_file = 'app.log'
log_file_mode = 'a'
log_format = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(level=log_level, filename=log_file, filemode=log_file_mode)
