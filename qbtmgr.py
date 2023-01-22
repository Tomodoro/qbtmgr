import argparse, logging, sys
from qbtauth import auth
from qbtinit import init
from qbttier import tier
from qbtrank import rank
from qbtseed import seed

if sys.argv[1] == "--debug":
    logging.basicConfig(level=logging.DEBUG,
        format="%(filename)s: %(levelname)s: %(message)s")
else:
    logging.basicConfig(level=logging.INFO,
        format="%(levelname)s: %(message)s")

# Top-level parser
parser = argparse.ArgumentParser(prog="qbtmgr",
                                 description="qBittorrent Management",
                                 epilog="Configurations must follow the API Reference from qittorrent-api")
subparsers = parser.add_subparsers(title="subcommands")
parser.add_argument("--debug",
                    action="store_true")

# Parset for auth subcommand
parser_auth = subparsers.add_parser("auth",
                                    help="manage qbittorrent login")
exclusive0_auth = parser_auth.add_mutually_exclusive_group(required=True)
exclusive0_auth.add_argument("--test",
                         action="store_true",
                         help="test connection with saved|given parameters")
exclusive0_auth.add_argument("--save",
                         action="store_true",
                         help="save new given parameters")
exclusive0_auth.add_argument("--display",
                        action="store_true",
                        help="display current saved|given settings")
parser_auth.add_argument("--host",
                         metavar="URL",
                         default=None,
                         type=str,
                         help="set the target host of the WebUI")
parser_auth.add_argument("--port",
                         metavar="PORT",
                         default=None,
                         type=int,
                         help="set the target port of the WebUI")
parser_auth.add_argument("--credentials",
                         nargs=2,
                         metavar=("USER", "PSWD"),
                         default=(None,None),
                         help="set the username and password of the WebUI")                         
parser_auth.add_argument("--bypass",
                         choices=["on","off"],
                         default=None,
                         help="bypass credentials")
parser_auth.set_defaults(func=auth)

# Parser for tier subcommand
parser_tier = subparsers.add_parser("tier",
                                    description="",
                                    help="manage bandwidth per ratio by setting tags")
exclusive0_tier = parser_tier.add_mutually_exclusive_group(required=True)
exclusive0_tier.add_argument("--set",
                         action="store_true",
                         help="add tier tags and start managing")
exclusive0_tier.add_argument("--unset",
                         action="store_true",
                         help="remove tier tags and set global values")
exclusive0_tier.add_argument("--save",
                         action="store_true",
                         help="save new given parameters")
exclusive0_tier.add_argument("--resume",
                         action="store_true",
                         help="resume paused tier-tagged torrents")
exclusive0_tier.add_argument("--automatize",
                         action="store_true",
                          help="runs both --set and --resume")
parser_tier.add_argument("--bandwidth",
                         metavar="BYTES",
                         default=None,
                         type=int,
                         help="maximum bandwidth dedicated to the tiers")
parser_tier.add_argument("--throttle",
                         metavar="BYTES",
                         default=None,
                         type=int,
                         help="number of steps the tier throttle increases")
parser_tier.add_argument("--stepstyle",
                         choices=["lineal","fibonacci","tribonacci"],
                         default=None,
                         help="set how the ratio increases between tiers")
parser_tier.add_argument("-r",
                         metavar="STEPS",
                         default=None,
                         type=int,
                         help="set ratio step or nth number of *ibonacci to start")
parser_tier.add_argument("--seedtime",
                         metavar="MINUTES",
                         default=None,
                         type=int,
                         help="number of minutes the tiers can seed before halting")
parser_tier.set_defaults(func=tier)

# Parser for rank subcommand
# parser_rank = subparsers.add_parser("rank",
#                                     help="manage bandwidth and timelimits by reading categories")
# exclusive_rank = parser_rank.add_mutually_exclusive_group(required=True)
# exclusive_rank.add_argument("--list",
#                          action="store_true",
#                          help="list all the saved ranks")
# exclusive_rank.add_argument("--new",
#                          action="store_true",
#                          help="create new rank, overwrite if name already exist")
# parser_rank.add_argument("--name",
#                         metavar="NAME",
#                         default="all",
#                         type=str,
#                         help="name of the rank to select")
# parser_rank.add_argument("--category",
#                          metavar="NAME",
#                          default="all",
#                          type=str,
#                          help="name of the category to select")
# parser_rank.add_argument("--tracker",
#                          metavar="NAME",
#                          default="all",
#                          type=str,
#                          help="name of the tracker to select")
# parser_rank.set_defaults(func=rank)

# Parser for seed subcommand
# parser_seed = subparsers.add_parser("seed",
#                                     help="manage seeding of all torrents")
# parser_seed.add_argument("--category",
#                          metavar="NAME",
#                          default="all",
#                          type=str,
#                          help="only seed torrents of the selected category")
# parser_seed.add_argument("--bandwidth",
#                          metavar="BYTES",
#                          default="-1",
#                          type=int,
#                          help="Maximum global bandwidth of qbittorrent")
# parser_seed.add_argument("--below",
#                          metavar="RATIO",
#                          default="-1",
#                          type=int,
#                          help="only seed torrents below the selected ratio threshold")
# parser_seed.add_argument("--rank",
#                          metavar="NAME",
#                          default="all",
#                          type=str,
#                          help="only seed torrents belonging to the selected rank")
# parser_seed.add_argument("--tier",
#                          metavar="NAME",
#                          default="tier",
#                          type=str,
#                          help="only seed torrents belonging to the selected tier")
# parser_seed.set_defaults(func=seed)

# Parse the args and react accordingly
args = parser.parse_args()

# Why catch error?
# https://bugs.python.org/issue16308
# https://stackoverflow.com/q/48648036
try:
    func = args.func    
except AttributeError:
    parser.error("too few arguments")

func(args)
