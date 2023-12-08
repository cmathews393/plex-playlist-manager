from spotiplexfunctions import connection_handler, process_for_user
from config_handler import read_config, ensure_config_exists


def spotifyplaylistsync():
    global is_syncing
    plex, sp, lidarr_playlists = connection_handler()
    print(lidarr_playlists)
    workercount = int(config("WORKERS"))

    # Convert comma-separated users string to list of users
    userlist = config("USERS").split(",") if config("USERS") else []
    replace = bool(config("REPLACE"))
    # Process for the main user first

    process_for_user(None, plex, sp, lidarr_playlists, workercount, replace)

    # Then process for each user in the user list
    for user in userlist:
        process_for_user(user.strip(), plex, sp, lidarr_playlists, workercount, replace)
    is_syncing = False

    plex_config = read_config("plex")
    PLEX_SERVER_URL = plex_config.get("url")
    PLEX_SERVER_TOKEN = plex_config.get("apikey")


def testvars():
    config = ensure_config_exists()  # Ensure the config file exists

    count = 0
    for section in config:
        if config[section]:  # Checks if the section has one or more items
            count += 1

    return count


def syncall():
    global is_syncing

    ppm_config = read_config("PPM")
    workercount = int(ppm_config.get("workercount"))
    users = ppm_config.get("users").split(",") if ppm_config.get("users") else []

    testvars()

    is_syncing = False

    return


testvars()
