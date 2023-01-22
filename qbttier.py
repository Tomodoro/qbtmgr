import qbittorrentapi as qbtapi
import re, sys, logging, configparser
from qbtauth import get_auth
from qbtinit import get_cfg

def tier(args):

    if args.automatize:
        set_tiers(args)
        resume_tiers(args)

    if args.resume:
        resume_tiers(args)

    if args.set:
        set_tiers(args)

    if args.unset:
        unset_tiers(args)


def set_tiers(args):

    client = get_auth()
    cfg    = get_cfg()
    var_stepstyle = cfg["tier"]["stepstyle"]
    var_ratio     = cfg["tier"]["step"]

    logging.debug("Reading configurations from qBittorrent")
    var_bandwidth = client.transfer_upload_limit()

    if var_bandwidth == 0:
        logging.info("Global Bandwidth is unlimited, locking at 500KiB/s")
        var_bandwidth = 512000

    else:
        logging.info("Setting bandwidth to half the Global bandwidth")
        var_bandwidth = var_bandwidth/2

    var_throttle = var_bandwidth/10

    logging.debug("Reading tier settings from flags")
    if args.stepstyle is not None: var_stepstyle = args.stepstyle
    if args.r         is not None: var_ratio     = args.r

    logging.debug("Creating tier array")
    all_tiers = [None] * 10
    for i in range(0,10):

        tier_bandwidth = int(var_bandwidth) - int(var_throttle)*int(i)
        if tier_bandwidth < 51199:
            logging.warning("Bandwidth too low for Tier "+str(i)+", locking at 50KiB/s")
            tier_bandwidth = 51200

        logging.debug("Tier "+str(i)+" has bandwidth "+str(tier_bandwidth))

        if var_stepstyle == "lineal":
            if i != 0:
                tier_ratio  = int(var_ratio) + int(var_ratio)*int(i)
            else:
                tier_ratio  = int(var_ratio)

        elif var_stepstyle == "fibonacci":
            tier_ratio = Fibonacci(int(var_ratio)+i)

        elif var_stepstyle == "tribonacci":
            tier_ratio = Tribonacci(int(var_ratio)+3+i)

        else:
            logging.debug("Unknown ratio, defaulting to lineal")
            tier_ratio  = int(var_ratio) + int(var_ratio)*int(i)

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
            client.torrents_set_share_limits(all_tiers[0]["ratio_limit"], var_-2, hash)
            client.torrents_set_upload_limit(all_tiers[0]["bandwidth"], hash)
            continue

        # Set Tier [1-9]
        for i in range(1,10):
            if (ratio >= all_tiers[i-1]["ratio_limit"]) \
            and (ratio < all_tiers[i]["ratio_limit"]):
                client.torrents_remove_tags(all_tiers[i-1]["tag"], hash)
                client.torrents_add_tags(all_tiers[i]["tag"], hash)
                client.torrents_set_share_limits(all_tiers[i]["ratio_limit"], -2, hash)
                client.torrents_set_upload_limit(all_tiers[i]["bandwidth"], hash)

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