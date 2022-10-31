import logging
import configparser

"""set configs"""
config = configparser.ConfigParser()
config.optionxform = str  # overrides configparsers conversion of all ini inputs to lowercase
config.read("configs/backfill_config.ini")
logfile = config.get("logs", "logfile")


"""Define logging"""
# Build logger
logger = logging.getLogger("dmp-cli")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
logger.handlers.clear()
logger.setLevel(logging.DEBUG)

# Build file handler
fh = logging.FileHandler(f"logs/dmp-{logfile}.log", mode='w')
fh.setLevel(logging.DEBUG)
fh.setFormatter(formatter)
logger.addHandler(fh)

# Build console handler
console = logging.StreamHandler()
console.setLevel(logging.INFO)
console.setFormatter(formatter)
logger.addHandler(console)
