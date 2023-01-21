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

## Configuration

Configuration file `qbtmgr.ini` can be found at:

Windows:
```
$ Set-Location -Path $env:appdata/qbtmgr
```

Linux:
```
$ cd ${HOME}/.qbtmgr
```
XDG Base directory will be supported in the future.

Darwin:

I don't own an Apple device, I can't test it.

### Credentials

You can set them directly inside `qbtmgr.ini` or via command line:
```
$ qbtmgr.py auth -h
```

## Seeding

It provides two methods of operation:
* **Tier:** tag-based management
* **Rank:** category-based management

### Tier

Main features:
* Only uses tags, but requires to run the program periodically
* Torrents are classified on 10 fixed groups or tiers
* Ratio limit is mandatory to keep control of the bandwidth
* Torrents with ratio out of range are ignored
* Default bandwidth allowed per torrent is 500KiB/s

Presets are provided to ease management:

**lineal** (Deafault)
* Increases ratio limit by a fixed step (default is 5)
* Throttles bandwidth by a constant step (default is 50KiB/s)

**fibonacci**
* Increases ratio limit following fibonacci's sequence
* It can be set to which sequence's term to start (default is 5th)
* Throttles bandwidth by a constant step (default is 50KiB/s)

**tribonacci**
* Increases ratio limit following a faster fibonacci's sequence
* It can be set to which sequence's term to start (default is 8th)
* Throttles bandwidth by a constant step (default is 50KiB/s)
* It grows... fast

#### Usage examples

To start managing the torrents run:
```
$ qbtmgr tier --set
```

To stop managing the torrents run:
```
$ qbtmgr tier --unset
```

Managed torrents are paused once they reach their ratio limit, it requiers two steps to resume them:
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

Coming soon...

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