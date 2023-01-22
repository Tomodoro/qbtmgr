import qbittorrentapi as qbtapi
import logging, configparser, sys, os

def write_default_cfgfile(file):

    cfg = configparser.ConfigParser()
    cfg["Client"] = {"host": "localhost",
                     "port": "8080",
                     "bypass": "off",
                     "username": "admin",
                     "password": "adminadmin"}
    cfg["tier"] = {"bandwidth": "512000",
                    "throttle": "51200",
                    "stepstyle": "lineal",
                    "step": 5,
                    "seedtime": -2}

    with open(file, 'w') as cfgfile:
        cfg.write(cfgfile)
        logging.debug("New configuration file created")

def get_cfgfile() -> str:

    if sys.platform == "win32":
        logging.debug("Windows platform detected")
        dataenv = os.getenv("APPDATA")
        datadir = os.path.join(dataenv, "qbtmgr")
        os.makedirs(datadir,exist_ok=True)
        cfgpath = datadir

    elif sys.platform == "linux":
        logging.debug("Linux platform detected")
        logging.debug("Working on legacy mode")
        dataenv = os.getenv("HOME")
        datadir = os.path.join(dataenv, "qbtmgr")
        os.makedirs(datadir,exist_ok=True)
        cfgpath = datadir

    else:
        logging.critical("Platform not supported.")
        sys.exit()

    cfgfile = os.path.join(cfgpath, "qbtmgr.ini")
        
    if os.path.isfile(cfgfile):
        logging.debug("Using existing configuration file")
        pass

    else:
        logging.debug("Creating new configuration file")
        write_default_cfgfile(cfgfile)

    return cfgfile

def get_cfg():

    logging.debug("Reading configuration file")
    cfgfile = get_cfgfile()
    cfg = configparser.ConfigParser()
    cfg.read(cfgfile)

    return cfg

def init(args):
    status = check_cfgfile()

    if not status:
        cfgpath = get_cfgpath()
        cfgfile = os.path.join(cfgpath, "qbtmgr.ini")
        write_cfgfile(cfgfile)
