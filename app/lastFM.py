import requests

class Base:
    URL = "http://ws.audioscrobbler.com/2.0"

    @classmethod
    def send(cls, params):
        try:
            r = requests.get(cls.URL, params)
        except:
            print("Error with API")
            return None
        return r


class LastFMTracks(Base):
    def get_info(self, track=None, mbid=None, artist=None, autocorrect=1):
        return self.send(locals())

    def get_correction(self, artist, track):
        return self.send(locals())

    def get_similar(self, mbid=None, track=None, artist=None, limit=None, autocorrect=1):
        return self.send(locals())

    def get_top_tags(self, track=None, artist=None, mbid=None, autocorrect=1):
        return self.send(locals())

    def search(self, track, limit=None, page=None, artist=None):
        return self.send(locals())

class LastFMAlbums(Base):
    def get_info(self, artist, album, mbid, autocorrect=1):
        return self.send(locals())

    def get_top_tags(self, artist=None, album=None, mbid=None, autocorrect=1):
        return self.send(locals())

    def search(self, album, limit=None, page=None):
        return self.send(locals())

class LastFMArtists(Base):
    def get_correction(self, artist):
        return self.send(locals())

    def get_info(self, artist=None, mbid=None, lang=None, autocorrect=1):
        return self.send(locals())

    def get_similar(self, artist, limit=None, autocorrect=1, mbid=None):
        return self.send(locals())

    def get_top_albums(self, artist=None, autocorrect=1, mbid=None, page=None, limit=None):
        return self.send(locals())

    def get_top_tags(self, artist=None, mbid=None, autocorrect=1):
        return self.send(locals())

    def get_top_tracks(self, artist=None, mbid=None, autocorrect=1, page=None, limit=None):
        return self.send(locals())

    def search(self, limit, page, artist):
        return self.send(locals())

class LastFMTags(Base):
    def get_info(self, tag, lang=None):
        return self.send(locals())

    def get_similar(self, tag):
        return self.send(locals())

    def get_top_albums(self, tag, limit=None, page=None):
        return self.send(locals())

    def get_top_artists(self, tag, limit=None, page=None):
        return self.send(locals())

    def get_top_tags(self):
        return self.send(locals())

    def get_top_tracks(self, tag, limit=None, page=None):
        return self.send(locals())

class LastFMGeos(Base):
    def get_top_artists(self, country, limit=None, page=None):
        return self.send(locals())

    def get_top_tracks(self, country, location=None, limit=None, page=None):
        return self.send(locals())

class LastFMCharts(Base):
    def get_top_artists(self, page=None, limit=None):
       return self.send(locals())

    def get_top_tracks(self, page=None, limit=None):
        return self.send(locals())