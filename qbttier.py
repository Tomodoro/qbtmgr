import qbittorrentapi as qbtapi
import re, sys, logging, configparser
from qbtauth import get_auth
from qbtinit import get_cfg, get_legacy_cfg
import qbttier_legacy

def tier(args):

    if args.l is not None:
        logging.info("Working on legacy mode")
        tier_legacy(args)

    elif args.set:
        set_tiers(args)

    elif args.unset:
        unset_tiers(args)

    elif args.resume:
        resume_tiers(args)


def set_tiers(args):

    client = get_auth()

    logging.debug("Reading configurations from qBittorrent")
    var_bandwidth = client.transfer_upload_limit()

    logging.debug("Reading flags")
    var_stepstyle = args.stepstyle

    if var_bandwidth == 0:
        logging.info("Global Bandwidth is unlimited, locking at 500KiB/s")
        var_bandwidth = 512000

    else:
        logging.info("Setting bandwidth to half the Global bandwidth")
        var_bandwidth = var_bandwidth/2

    var_throttle = var_bandwidth/10

    logging.debug("Creating tier array")
    all_tiers = [None] * 10
    for i in range(0,10):

        tier_bandwidth = int(var_bandwidth) - int(var_throttle)*int(i)
        if tier_bandwidth < 51199:
            logging.warning("Bandwidth too low for Tier "+str(i)+", locking at 50KiB/s")
            tier_bandwidth = 51200

        logging.debug("Tier "+str(i)+" has bandwidth "+str(tier_bandwidth))

        if var_stepstyle == "lineal":
            var_ratio = 5
            if i != 0:
                tier_ratio  = var_ratio + var_ratio*i
            else:
                tier_ratio  = var_ratio

        elif var_stepstyle == "quadratic":
            var_ratio = 2
            if i != 0:
                tier_ratio  = var_ratio**i
            else:
                tier_ratio  = 1

        elif var_stepstyle == "fibonacci":
            var_ratio = 5
            tier_ratio = Fibonacci(var_ratio+i)

        elif var_stepstyle == "tribonacci":
            var_ratio = 8
            tier_ratio = Tribonacci(var_ratio+i)

        tier_tag = "@tier "+str(i)

        all_tiers[i] = { "tag": tier_tag,
                    "bandwidth": tier_bandwidth,
                    "ratio_limit": tier_ratio}
        
        logging.debug("NEW TIER: " +str(all_tiers[i]))

    logging.debug("Adding tiers")
    for torrent in client.torrents_info():
        category = torrent.category
        ratio    = torrent.ratio
        tags     = torrent.tags
        hash     = torrent.hash
        free     = re.search("tier free", tags)
        progress = torrent.progress

        # Check if torrent has finished
        if progress != 1:
            continue

        # Set apart Tier free
        elif free:
            client.torrents_set_share_limits(-1, -1, hash)
            client.torrents_set_upload_limit(-1, hash)
            continue

        # Above Tiers
        if (ratio > all_tiers[-1]["ratio_limit"]):
            logging.info("Ratio "+str(ratio)+" out of bounds for "+hash+", skipping.")
            continue

        # Set Tier 0
        if ratio < all_tiers[0]["ratio_limit"]:
            client.torrents_add_tags(all_tiers[0]["tag"], hash)
            client.torrents_set_share_limits(all_tiers[0]["ratio_limit"], -2, hash)
            client.torrents_set_upload_limit(all_tiers[0]["bandwidth"], hash)
            if args.resume: client.torrents_resume(hash)
            continue

        # Set Tier [1-9]
        for i in range(1,10):
            if (ratio >= all_tiers[i-1]["ratio_limit"]) \
            and (ratio < all_tiers[i]["ratio_limit"]):
                client.torrents_remove_tags(all_tiers[i-1]["tag"], hash)
                client.torrents_add_tags(all_tiers[i]["tag"], hash)
                client.torrents_set_share_limits(all_tiers[i]["ratio_limit"], -2, hash)
                client.torrents_set_upload_limit(all_tiers[i]["bandwidth"], hash)

        if args.resume: client.torrents_resume(hash)

def unset_tiers(args):
    logging.debug("Removing tiers")

    client = get_auth()
    for torrent in client.torrents_info():
        tags     = torrent.tags
        hash     = torrent.hash
        tier     = re.search(".tier [0-9]", tags)
        free     = re.search(".tier free", tags)

        if not free and (tier is not None):
            client.torrents_remove_tags(tier.group(0), hash)
            client.torrents_set_share_limits(-2, -2, hash)
            client.torrents_set_upload_limit(-1, hash)

    for i in range(0,10):
        prefix = "@"
        client.torrents_delete_tags(prefix+"tier "+str(i))

def resume_tiers(args):

    client = get_auth()
    for torrent in client.torrents_info():
        tags = torrent.tags
        hash = torrent.hash
        ratio = torrent.ratio
        ratio_limit = torrent.ratio_limit
        state = torrent.state
        tier = re.search(".tier [0-9]", tags)

        if tier is None:
            continue

        elif (state != "pausedUP"):
            continue

        else:
            client.torrents_resume(hash)

def tier_legacy(args):

    if len(args.l) == 0:
        qbttier_legacy.help()
        sys.exit()

    else:
        config = get_legacy_cfg()
        client = qbtapi.Client(host=config["Client"]["host"], port=int(config["Client"]["port"]))

    qbttier_legacy.log_in(config, client)

    for i in range(len(args.l)):
        
        if args.l[i] == "set-tiers":
            qbttier_legacy.set_tiers(config, client)

        if args.l[i] == "not-popular":
            qbttier_legacy.not_popular(config, client)

        if args.l[i] == "tier-active":
            qbttier_legacy.tier_active(config, client)

# https://www.geeksforgeeks.org/python-program-for-program-for-fibonacci-numbers-2/
# Function for nth Fibonacci number
def Fibonacci(n):

    # Check if input is 0 then it will
    # print incorrect input
    if n < 0:
        logging.error("Fibonacci has incorrect input")
        sys.exit()

    # Check if n is 0
    # then it will return 0
    elif n == 0:
        return 0

    # Check if n is 1,2
    # it will return 1
    elif n == 1 or n == 2:
        return 1

    else:
        return Fibonacci(n-1) + Fibonacci(n-2)

# Function for nth Tribonacci number
def Tribonacci(n):

    # Check if input is 0 then it will
    # print incorrect input
    if n < 0:
        logging.error("Tribonacci has incorrect input")
        sys.exit()

    # Check if n is 0
    # then it will return 0
    elif n == 0:
        return 0

    elif n == 1 or n == 2:
        return 0

    elif n == 3 or n == 4:
        return 1

    # Check if n is 1,2
    # it will return 1
    elif n == 3 or n == 4:
        return 1

    else:
        return Tribonacci(n-1) + Tribonacci(n-2) + Tribonacci(n-3)