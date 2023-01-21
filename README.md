# qBittorrent Management

EARLY RELEASE
Program to manage multiple torrents at once in qBittorrent.

## Installation

(Optional) Start a python environment:
```
$ python -m venv qbtvenv
$ cd ./qbtvenv
$ source ./bin/activate
```

Install API library:
```
$ pip install qbittorrent-api
```

Clone the repo:
```
$ git clone https://github.com/Tomodoro/qbtmgr.git
```

Print help:
```
$ qbtmgr.py -h
```

Subcommands also contain help:
```
$ qbtmgr auth -h
```

## Authentification



## Seeding

It provides two methods of operation: tag-based management and category-based management.

The main goal is to make use of already existent methods of organization of torrents and only provide the automatization process to trigger changes.

### Tier

This is a tag-based management that classifies torrents on 10 fixed groups or tiers, each one having a defined ratio and bandwidth limit.

This type of management requires the program to be run on a periodic schedule, this way it can renew the torrent's group once it's ratio limit has been reached. A ratio limit is required for this type of approach since it strictly forbids any torrent to use more bandwidth than it's desired at the expense of pausing it.

This answers a specific use case, torrents that are desired to seed but that clog the available bandwidth. Presets or stepstyles have been made in order to ease the configuration:

**lineal** (Default)
Increases on a fixed step (default is 5). Throttles bandwidth on a steady pace.

**fibonacci**
As the title says (by default it starts at 5). Seeds for more time before start throttling too much the bandwidth.

**tribonacci**
This is an extension of Fibonacci's. Here tier 0 is ratio 13 and tier 9 is ratio 3136, it takes a lot heck of a time to throttle fully.

#### Usage examples

To start managing the torrents run:
```
$ qbtmgr tier --set
```

To stop managing the torrents run:
```
$ qbtmgr tier --unset
```

Managed torrents are paused once they reach their ratio limit, it requiers to steps to resume them:
```
# Update the tiers
$ qbtmgr tier --set

# Resume managed torrents
$ qbtmgr tier --resume
```

To run as a single command:
```
$ qbtmgr tier --automatize
```

### Rank

This is a category-based management that classifies all torrents inside a directory or folder, each one having its own ratio, bandwidth and seedtime limit.

It is intended to provide a more granular control over the seeding options, therefore a replacement for the tiers.

Keep in mind that for the qbittorrent api a subcategory is not considered part of its parent category, it just appends the name to the string. For example:

```
Category     : Music
API returns  : "Music"

Subcategory: : Chillstep
API returns  : "Music/Chillhop"
```

This program will consider `Music` and `Music/Chillhop` as two different categories.

Coming soon...