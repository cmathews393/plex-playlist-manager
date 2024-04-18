# Plex Playlist Manager
 An easy way to sync playlists across multiple services, and manage playlists for plex more intuitively than the default Plex experience.


## Features

- Automatically sync users requests to a Plex Playlist called "My Requests" for each user (i.e. via Ombi, using Radarr/Sonarr tags)

## [Roadmap]()

- Sync Import lists to Plex from
  - Radarr
  - Sonarr
  - Lidarr

- Manual/Custom playlist creation via web interface

- Spotify direct sync (No Lidarr)

- Trakt direct sync

- TMDB direct sync

- IMDB direct sync

## Details

Plex Playlist manager was inspired by my frustration at trying to add a trakt list to Radarr, only to have no easy way to categorize movies from that list via Plex. I'd done some work on [Spotiplex](https://github.com/cmathews393/spotify-to-plex) and thought this would be a nice upgrade to that and a way to incorporate Movies and TV as well.

### Bugs

- See the Issues tab for details about known bugs and their status

### Tools/Packages

- Flask
- Spotipy
- PlexAPI
- rtoml
- Bootstrap-Flask