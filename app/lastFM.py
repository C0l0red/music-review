import requests

class Base:
    URL = "http://ws.audioscrobbler.com/2.0"

    @classmethod
    def send(cls, params):
        r = requests.get(cls.URL, params)
        return r


class Track(Base):
    def get_info(self, track=None, mbid=None, artist=None, autocorrect=None):
        return self.send(locals())

    def get_correction(self, artist, track):
        return self.send(locals())

    def get_similar(self, mbid=None, track=None, artist=None, limit=None, autocorrect=None):
        return self.send(locals())

    def search(limit, track, page=None, artist=None):
        return self.send(locals())

class Album(Base):
    def get_info(self, artist, album, mbid, autocorrect):
        return self.send(locals())

    def search(self, album, limit=None, page=None):
        return self.send(locals())

class Artist(Base):
    def get_correction(self, artist):
        return self.send(locals())

    def get_info(self, artist=None, mbid=None, lang=None, autocorrect=None):
        return self.send(locals())

    def get_similar(self, artist, limit=None, autocorrect=None, mbid=None):
        return self.send(locals())

    def get_top_albums(self, artist=None, autocorrect=None, mbid=None, page=None, limit=None):
        return self.send(locals())

    def get_top_tracks(self, artist=None, mbid=None, autocorrect=None, page=None, limit=None):
        return self.send(locals())

    def search(self, limit, page, artist):
        return self.send(locals())

class Geo(Base):
    def get_top_artists(self, country, limit=None, page=None):
        return self.send(locals())

    def get_top_tracks(self, country, location=None, limit=None, page=None):
        return self.send(locals())

class Chart(Base):
    def get_top_artist(page=None, limit=None):
       return self.send(locals())

    def get_top_tracks(page=None, limit=None):
        return self.send(locals())