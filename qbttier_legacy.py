import qbittorrentapi as qbtapi
import re, sys, logging, configparser
from qbtinit import get_legacy_cfg

def log_in(config, cl):

    if (str(config["Client"]["credentials"]) == "True"):
        try:
            cl.auth_log_in(username=config["Client"]["username"],password=config["Client"]["password"])
            print ("INFO: Sucessful login with credentials")
        except:
            print ("INFO: Credentials activated in config file")
            print ("Could not login with provided credentials")
            sys.exit()

    if (str(config["Client"]["credentials"]) == "False"):
        try:
            cl.auth_log_in()
            print ("INFO: Succesful login with authentication bypass")
        except:
            print ("INFO: Credentials deactivated in config file")
            print ("Could not login, are you sure you have authentication bypass?")
            sys.exit()

def help():
	print ("")
	print ("qBittorrent Seeding Manager")
	print ("    Program to manage seeding options of multiple completed torrents at once")
	print ("    To see this help run the program without arguments\n")
	print ("Arguments available:")
	print ("    set-tiers:   Adds tags to torrents and applies upload speed limits according to their ratio")
	print ("                 You can exclude torrents from this limits adding the tag \"@tier free\" manually")
	print ("    not-popular: Pauses torrents if there is more than X seeders currently present")
	print ("                 Resumes torrents if there is less than X seeders currently present\n")
	print ("    tier-active: Resumes paused torrents, only affects tier-tagged torrents")
	print ("                 Overrides \"not-popular\" if used after that argument")
	print ("Configurations are read from the file \"qbitseedmgr.ini\" and must follow the API Reference from qittorrent-api ")
	print ("")

def tier_active(config, client):
	for torrent in client.torrents_info():
		tags = torrent.tags
		ratio = torrent.ratio
		ratio_limit = torrent.ratio_limit
		state = torrent.state
		tier = re.search("@tier [1-9]",tags)

		if tier is None:
			continue

		if (state != "pausedUP"):
			continue

		tier_num = int(tier.group(0)[-1])
		prev_tier_num = tier_num-1
		prev_tier = "Tier "+str(prev_tier_num)

		if (ratio >= int(config[prev_tier]["ratio_limit"])):
			client.torrents_resume(torrent.hash)

def not_popular(config, client):
	for torrent in client.torrents_info():
		ratio = torrent.ratio
		seeds = torrent.num_complete
		tags = torrent.tags
		is_exception = re.search(config["Not popular"]["tag_exception"],tags)

		if torrent.progress != 1:
			continue

		elif is_exception:
			continue

		elif (seeds > int(config["Not popular"]["max_num_seeds"])) and (ratio > int(config["Not popular"]["min_ratio"])):
			client.torrents_pause(torrent.hash)

		else:
			client.torrents_resume(torrent.hash)

def set_tiers(config, client):
	for torrent in client.torrents_info():
		ratio = torrent.ratio
		tags = torrent.tags
		hash = torrent.hash
		free = re.search("tier free",tags)
		progress = torrent.progress
		
		# Check if it has finished
		if progress != 1:
			continue

		# Mantain Tier free
		elif free:
			client.torrents_set_share_limits(config["Tier free"]["ratio_limit"],config["Tier free"]["seeding_time_limit"],hash)
			client.torrents_set_upload_limit(config["Tier free"]["upload_limit"],hash)	
	
		# Set Tier 0
		elif (ratio >= 0) and (ratio < int(config["Tier 0"]["ratio_limit"])):
			client.torrents_add_tags("@tier 0",hash)
			client.torrents_set_share_limits(config["Tier 0"]["ratio_limit"],config["Tier 0"]["seeding_time_limit"],hash)
			client.torrents_set_upload_limit(config["Tier 0"]["upload_limit"],hash)
	
		# Set Tier 1
		elif (ratio >= int(config["Tier 0"]["ratio_limit"])) and (ratio < int(config["Tier 1"]["ratio_limit"])):
			client.torrents_remove_tags("@tier 0",torrent.hash)
			client.torrents_add_tags("@tier 1",torrent.hash)
			client.torrents_set_share_limits(config["Tier 1"]["ratio_limit"],config["Tier 1"]["seeding_time_limit"],hash)
			client.torrents_set_upload_limit(config["Tier 1"]["upload_limit"],hash)
		
		# Set Tier 2
		elif (ratio >= int(config["Tier 1"]["ratio_limit"])) and (ratio < int(config["Tier 2"]["ratio_limit"])):
			client.torrents_remove_tags("@tier 1",torrent.hash)
			client.torrents_add_tags("@tier 2",torrent.hash)
			client.torrents_set_share_limits(config["Tier 2"]["ratio_limit"],config["Tier 2"]["seeding_time_limit"],hash)
			client.torrents_set_upload_limit(config["Tier 2"]["upload_limit"],hash)

		# Set Tier 3
		elif (ratio >= int(config["Tier 2"]["ratio_limit"])) and (ratio < int(config["Tier 3"]["ratio_limit"])):
			client.torrents_remove_tags("@tier 2",torrent.hash)
			client.torrents_add_tags("@tier 3",torrent.hash)
			client.torrents_set_share_limits(config["Tier 3"]["ratio_limit"],config["Tier 3"]["seeding_time_limit"],hash)
			client.torrents_set_upload_limit(config["Tier 3"]["upload_limit"],hash)

		# Set Tier 4
		elif (ratio >= int(config["Tier 3"]["ratio_limit"])) and (ratio < int(config["Tier 4"]["ratio_limit"])):
			client.torrents_remove_tags("@tier 3",torrent.hash)
			client.torrents_add_tags("@tier 4",torrent.hash)
			client.torrents_set_share_limits(config["Tier 4"]["ratio_limit"],config["Tier 4"]["seeding_time_limit"],hash)
			client.torrents_set_upload_limit(config["Tier 4"]["upload_limit"],hash)

		# Set Tier 5
		elif (ratio >= int(config["Tier 4"]["ratio_limit"])) and (ratio < int(config["Tier 5"]["ratio_limit"])):
			client.torrents_remove_tags("@tier 4",torrent.hash)
			client.torrents_add_tags("@tier 5",torrent.hash)
			client.torrents_set_share_limits(config["Tier 5"]["ratio_limit"],config["Tier 5"]["seeding_time_limit"],hash)
			client.torrents_set_upload_limit(config["Tier 5"]["upload_limit"],hash)

		# Set Tier 6
		elif (ratio >= int(config["Tier 5"]["ratio_limit"])) and (ratio < int(config["Tier 6"]["ratio_limit"])):
			client.torrents_remove_tags("@tier 5",torrent.hash)
			client.torrents_add_tags("@tier 6",torrent.hash)
			client.torrents_set_share_limits(config["Tier 6"]["ratio_limit"],config["Tier 6"]["seeding_time_limit"],hash)
			client.torrents_set_upload_limit(config["Tier 6"]["upload_limit"],hash)

		# Set Tier 7
		elif (ratio >= int(config["Tier 6"]["ratio_limit"])) and (ratio < int(config["Tier 7"]["ratio_limit"])):
			client.torrents_remove_tags("@tier 6",torrent.hash)
			client.torrents_add_tags("@tier 7",torrent.hash)
			client.torrents_set_share_limits(config["Tier 7"]["ratio_limit"],config["Tier 7"]["seeding_time_limit"],hash)
			client.torrents_set_upload_limit(config["Tier 7"]["upload_limit"],hash)

		# Set Tier 8
		elif (ratio >= int(config["Tier 7"]["ratio_limit"])) and (ratio < int(config["Tier 8"]["ratio_limit"])):
			client.torrents_remove_tags("@tier 7",torrent.hash)
			client.torrents_add_tags("@tier 8",torrent.hash)
			client.torrents_set_share_limits(config["Tier 8"]["ratio_limit"],config["Tier 8"]["seeding_time_limit"],hash)
			client.torrents_set_upload_limit(config["Tier 8"]["upload_limit"],hash)

		# Set Tier 9
		elif (ratio >= int(config["Tier 8"]["ratio_limit"])) and (ratio < int(config["Tier 9"]["ratio_limit"])):
			client.torrents_remove_tags("@tier 8",torrent.hash)
			client.torrents_add_tags("@tier 9",torrent.hash)
			client.torrents_set_share_limits(config["Tier 9"]["ratio_limit"],config["Tier 9"]["seeding_time_limit"],hash)
			client.torrents_set_upload_limit(config["Tier 9"]["upload_limit"],hash)

		else:
			print ("Ratio "+str(ratio)+" out of bounds for "+hash)