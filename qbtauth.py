import qbittorrentapi as qbtapi
import os, sys, logging, configparser
from qbtinit import get_cfg, get_cfgfile

def auth(args): 

    cfg = get_cfg()
    var_host   = cfg["Client"]["host"]
    var_port   = cfg["Client"]["port"]
    var_bypass = cfg["Client"]["bypass"]
    var_user   = cfg["Client"]["username"]
    var_pswd   = cfg["Client"]["password"]

    logging.debug("Reading auth settings from flags")
    if args.host           is not None: var_host   = args.host
    if args.port           is not None: var_port   = args.port
    if args.bypass         is not None: var_bypass = args.bypass
    if args.credentials[0] is not None: var_user   = args.credentials[0]
    if args.credentials[1] is not None: var_pswd   = args.credentials[1]

    client = qbtapi.Client(host=var_host, port=var_port)

    if args.display == True:
        logging.debug("Printing to console current settings")
        print("HOST:   "+var_host)
        print("PORT:   "+var_port)
        print("USER:   "+var_user)
        print("PSWD:   "+var_pswd)
        print("BYPASS: "+var_bypass)

    if args.test == True:
        logging.debug("Performing test connection")
        if var_bypass == "on":
            logging.debug("Bypass is active")
            try:
                client.auth_log_in()
            except:
                logging.error("Failed login, bypass rejected")
                
        if var_bypass == "off":
            logging.debug("Bypass is inactive")
            try:
                client.auth_log_in(username=var_user, password=var_pswd)
            except:
                logging.error("Failed login, credentials rejected")

        if client.is_logged_in:
                logging.info("Connection stablished")
        else:
            logging.critical("Could not stablish a connection.")

    if args.save == True:
        upd_auth(args)

def upd_auth(args):
    
    cfgfile = get_cfgfile()
    cfg = configparser.ConfigParser()
    cfg.read(cfgfile)

    if args.host           is not None: cfg["Client"]["host"]     = str(args.host)
    if args.port           is not None: cfg["Client"]["port"]     = str(args.port)
    if args.bypass         is not None: cfg["Client"]["bypass"]   = str(args.bypass)
    if args.credentials[0] is not None: cfg["Client"]["username"] = str(args.credentials[0])
    if args.credentials[1] is not None: cfg["Client"]["password"] = str(args.credentials[1])

    with open(cfgfile, "w") as f:
        cfg.write(f)
    
    logging.debug("Configuration file updated")

def get_auth():

    logging.debug("Reading auth settings from configuration file")
    cfgfile = get_cfgfile()
    cfg = configparser.ConfigParser()
    cfg.read(cfgfile)
    var_host   = cfg["Client"]["host"]
    var_port   = cfg["Client"]["port"]
    var_bypass = cfg["Client"]["bypass"]
    var_user   = cfg["Client"]["username"]
    var_pswd   = cfg["Client"]["password"]   

    client = qbtapi.Client(host=var_host, port=var_port)

    if var_bypass == "on":
        try:
            client.auth_log_in()
        except:
            logging.error("Failed login, bypass rejected")
            sys.exit()
                
    if var_bypass == "off":
        try:
            client.auth_log_in(username=var_user, password=var_pswd)
        except:
            logging.error("Failed login, credentials rejected")
            sys.exit()

    return client

