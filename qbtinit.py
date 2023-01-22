import qbittorrentapi as qbtapi
import logging, configparser, sys, os

def write_default_cfgfile(file):

    cfg = configparser.ConfigParser()
    cfg["Client"] = {"host": "localhost",
                     "port": "8080",
                     "bypass": "off",
                     "username": "admin",
                     "password": "adminadmin"}

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

# Legacy section

def write_default_legacy_cfgfile(file):

    cfg = configparser.ConfigParser()
    cfg["Client"] = {"host": "localhost",
                     "port": "8080",
                     "credentials": "True",
                     "username": "admin",
                     "password": "adminadmin"}

    cfg["Not popular"] = {"max_num_seeds": "10",
                          "min_ratio": "2",
                          "tag_exception": "Software"}

    cfg["Tier free"] = { "ratio_limit": "-1",
                         "seeding_time_limit": "-1",
                         "upload_limit": "-1"}

    cfg["Tier 0"] = { "ratio_limit": "5",
                       "seeding_time_limit": "-2",
                       "upload_limit": "-1"}

    cfg["Tier 1"] = { "ratio_limit": "10",
                       "seeding_time_limit": "-2",
                       "upload_limit": "460800"}

    cfg["Tier 2"] = { "ratio_limit": "15",
                       "seeding_time_limit": "-2",
                       "upload_limit": "409600"}

    cfg["Tier 3"] = { "ratio_limit": "20",
                       "seeding_time_limit": "-2",
                       "upload_limit": "358400"}

    cfg["Tier 4"] = { "ratio_limit": "25",
                       "seeding_time_limit": "-2",
                       "upload_limit": "307200"}

    cfg["Tier 5"] = { "ratio_limit": "30",
                       "seeding_time_limit": "-2",
                       "upload_limit": "256000"}

    cfg["Tier 6"] = { "ratio_limit": "35",
                       "seeding_time_limit": "-2",
                       "upload_limit": "204800"}

    cfg["Tier 7"] = { "ratio_limit": "40",
                       "seeding_time_limit": "-2",
                       "upload_limit": "153600"}

    cfg["Tier 8"] = { "ratio_limit": "45",
                       "seeding_time_limit": "-2",
                       "upload_limit": "102400"}

    cfg["Tier 9"] = { "ratio_limit": "50",
                       "seeding_time_limit": "-2",
                       "upload_limit": "51200"}

    with open(file, 'w') as cfgfile:
        cfg.write(cfgfile)
        logging.debug("New legacy configuration file created")

def get_legacy_cfgfile() -> str:

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

    cfgfile = os.path.join(cfgpath, "qbitseedmgr.ini")
        
    if os.path.isfile(cfgfile):
        logging.debug("Using existing legacy configuration file")
        pass

    else:
        logging.debug("Creating new legacy configuration file")
        write_default_legacy_cfgfile(cfgfile)

    return cfgfile

def get_legacy_cfg():

    logging.debug("Reading legacy configuration file")
    cfgfile = get_legacy_cfgfile()
    cfg = configparser.ConfigParser()
    cfg.read(cfgfile)

    return cfg


def init(args):
    status = check_cfgfile()

    if not status:
        cfgpath = get_cfgpath()
        cfgfile = os.path.join(cfgpath, "qbtmgr.ini")
        write_cfgfile(cfgfile)
