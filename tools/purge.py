from ipodder import players
import os.path

player = players.get(players.player_types()[0])
bad = [t for t in player.iTunes.LibraryPlaylist.Tracks
       if not (hasattr(t, 'Location') and t.Location and os.path.isfile(t.Location))]
print len([t.Delete() for t in bad])
