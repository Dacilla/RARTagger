import qbittorrentapi
import logging
import sys
import json
from pprint import pprint

__VERSION = "1.0.0"
LOG_FORMAT = "%(asctime)s.%(msecs)03d %(levelname)-8s P%(process)06d.%(module)-12s %(funcName)-16sL%(lineno)04d %(message)s"
LOG_DATE_FORMAT = "%Y-%m-%d %H:%M:%S"

def main():
    logging.basicConfig(datefmt=LOG_DATE_FORMAT, format=LOG_FORMAT, level=logging.INFO)
    logging.info(f"Version {__VERSION} starting...")
    with open("qbitDetails.txt", "r") as d:
        lines = d.readlines()
        username = lines[0].strip()
        password = lines[1].strip()
    logging.debug("Username: " + username)
    logging.debug("Password: " + password)
    logging.info("Logging in to qbit...")
    qb = qbittorrentapi.Client("http://192.168.1.114:8080", username=username, password=password)
    # Login to the qBittorrent web UI
    qb.auth_log_in()

    # Get a list of all the torrents
    torrents = qb.torrents_info()

    # Iterate through each torrent
    for torrent in torrents:
        torrent:qbittorrentapi.TorrentDictionary
        # print(torrent.files)
        for file in torrent.files:
            torrentDict = dict(file)
            logging.debug(torrentDict)
            if torrentDict["name"].endswith(".r01"):
                logging.info("RARed torrent found with name: " + torrent["name"])
                # If the torrent has ".r01" files, add the "RARed" tag to it
                torrent.add_tags(tags="RARed")
                # sys.exit()
                break

    # Log out of the qBittorrent web UI
    qb.auth_log_out()

if __name__ == "__main__":
    main()
