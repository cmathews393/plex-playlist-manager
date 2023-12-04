from .spotiplexfunctions import connection_handler, process_for_user



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