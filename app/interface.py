from .lastFM import LastFMTracks, LastFMAlbums, LastFMArtists, LastFMCharts, LastFMGeos, LastFMTags

class Instance:

    def __init__(self, API=None):
        self.API = API
        self.track = self.Track(self)
        self.album = self.Album(self)
        self.artist = self.Artist(self)
        self.genre = self.Genre(self)
        self.charts = self.Charts(self)

    class Base:
        APIs = {
            "lastFM": {
                "track" : LastFMTracks,
                "album": LastFMAlbums,
                "artist": LastFMArtists,
                "tag": LastFMTags,
                "geo": LastFMGeos,
                "chart": LastFMCharts
            }
        }

        endpoints = {

            "track": {

                "info": {
                    "lastFM": LastFMTracks.get_info
                },
                "similar": {
                    "lastFM": LastFMTracks.get_similar
                },
                "search": {
                    "lastFM": LastFMTracks.search
                }
            },

            "album": {

                "info": {
                    "lastFM": LastFMAlbums.get_info
                },
                "similar": {

                },
                "search": {
                    "lastFM": LastFMAlbums.search
                }
            },

            "artist": {

                "info": {
                    "lastFM": LastFMArtists.get_info
                },
                "track": {
                    "lastFM": LastFMArtists.get_top_tracks
                },
                "album": {
                    "lastFM": LastFMArtists.get_top_albums
                },
                "search": {
                    "lastFM":  LastFMArtists.search
                },
                "similar": {
                    "lastFM": LastFMArtists.get_similar
                },
                "genres": {
                    "lastFM": LastFMArtists.get_top_tags
                }
            },

            "genre": {

                "info": {
                    "lastFM": LastFMTags.get_info
                },
                "similar": {
                    "lastFM": LastFMTags.get_similar
                },
                "tracks": {
                    "lastFM": LastFMTags.get_top_tracks
                },
                "albums": {
                    "lastFM": LastFMTags.get_top_albums
                }, 
                "artists": {
                    "lastFM": LastFMTags.get_top_artists
                }
            },

            "charts": {

                "top_track": {
                    "lastFM": LastFMCharts.get_top_tracks
                },
                "top_albums": {
                    "lastFM": LastFMCharts.get_top_artists
                }
            }
        }

        def __init__(self, parent):
            self.API = parent.API

        def fetch(self, endpoint, **kwargs):
            
            if self.API in self.APIs:
                API = self.endpoints[self.method][endpoint].get(self.API)
                if API:
                    data = API(**kwargs)
                    return data
            
            return self.fetchAny(endpoint, **kwargs)


        def fetchAny(self, endpoint, **kwargs):
            for API in self.APIs:
                data = self.endpoints[self.method][endpoint][API](**kwargs)

                if data is not None:
                    return data

            return None
            

        def endpoint(self, endpoint, locals):
            vals = {a:b for a,b in locals.items() if b is not None}

            if self.API:
                data = self.fetch(endpoint, vals)
                if data:
                    return data

                return self.fetchAny(endpoint, vals)


    class Track(Base):
        method = "track"

        def info(self, track=None, artist=None):
            return self.endpoint("info", locals())

        def similar(self, track=None, artist=None, limit=None):
            return self.endpoint("similar", locals())

        def search(self, track, artist=None, limit=None, page=None):
            return self.endpoint("search", locals())

    class Album(Base):
        method = "album"

        def info(self, album=None, artist=None):
            return self.endpoint("info", locals())

        #def similar(self, album=None, artist=None, limit=None):
        #    return self.endpoint("similar", locals())

        def search(self, album, limit=None, page=None):
            return self.endpoin("search", locals())

    class Artist(Base):
        method = "artist"

        def info(self, artist=None):
            return self.endpoint("info", locals())

        def albums(self, artist=None, page=None, limit=None):
            return self.endpoint("albums", locals())

        def tracks(self, artist=None, page=None, limit=None):
            return self.endpoint("artists", locals())

        def search(self, artist, limit=None, page=None):
            return self.endpoint("search", locals())

        def similar(self, artist, limit=None):
            return self.endpoint("similar", locals())

        def genre(self, artist):
            return self.endpoint("genre", locals())

    class Genre(Base):
        method = "genre"

        def info(self, genre, lang=None):
            return self.endpoint("info", locals())

        def similar(self, genre):
            return self.endpoint("similar". locals())

        def tracks(self, genre, limit=None, page=None):
            return self.endpoint("tracks", locals())

        def albums(self, genre, limit=None, page=None):
            return self.endpoint("albums", locals())

        def artists(self, genre, limit=None, page=None):
            return self.endpoint("artists", locals())

    class Charts(Base):
        method = "charts"

        def top_tracks(self, page=None, limit=None):
            return self.endpoint("top_tracks", locals())

        def top_artists(self, page=None, limit=None):
            return self.endpoint("top_artists", locals())
                
        