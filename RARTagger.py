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
    qb = qbittorrentapi.Client("http://192.168.1.114:8080", username=username, password=password, REQUESTS_ARGS={'timeout': (300, 300)})
    # Login to the qBittorrent web UI
    qb.auth_log_in()

    logging.info("Logged in to qbit.")
    logging.info("Getting list of categories...")
    categories = qb.torrent_categories.categories.keys()
    foundTorrents = []
    for category in categories:
        attempts = 0
        readSuccess = False
        torrents = None
        logging.info("Reading category: " + category)

        # Get a list of all the torrents
        # torrents = qb.torrents_info(category='tv-sonarr')
        torrents = qb.torrents_info(category=category)
        blurayStrings = ["BR", "BluRay", "BD", "Blu-Ray", "Blu-ray"]
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
                if torrentDict["name"].endswith(".bdmv") or (any(x in torrentDict["name"] for x in blurayStrings) and torrentDict["name"].endswith(".iso")):
                    logging.info("Bluray Disc torrent found with name: " + torrent["name"])
                    # If the torrent has ".bdmv" files, add the "BDRaw" tag to it
                    torrent.add_tags(tags="BDRaw")
                    # sys.exit()
                    break

    # Log out of the qBittorrent web UI
    qb.auth_log_out()


if __name__ == "__main__":
    main()
