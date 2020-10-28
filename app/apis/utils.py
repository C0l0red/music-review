from app import db

def clean_data(data):
    artist= data.get("artist")
    if artist:
        artist = Artist.query.filter(Artist.name.ilike(artist)).first_or_404(f"Artist '{artist}' not found")
        data['artist'] = artist

    album = data.get("album")
    if album:
        album = artist.albums.filter(Album.name.ilike(album)).first_or_404(f"Album '{album}' by '{artist}' not found")
        #print(album)
        data['album'] = album

    genre = data.get("genre")
    if genre:
        genre = Genre.query.filter(Genre.name.ilike(genre)).first_or_404(f"Genre '{genre}' not found")
        #print(genre)
        data['genre'] = genre

    featuring = data.get("featuring")
    if featuring:
        for i, artist in enumerate(featuring):
            result = Artist.query.filter(Artist.name.ilike(artist)).first_or_404(f"Artist '{artist}' not found")
            featuring[i] = result
        data["featuring"] = featuring

    genres = data.get("genres")        
    if genres:
        for i, genre in enumerate(genres):
            result = Genre.query.filter(Genre.name.ilike(genre)).first_or_404(f"Genre '{genre}' not found")
            genres[i] = result
        data["genres"] = genres
    
    return data

class SingleResource:

    def get(self, id):
        obj = self.Model.query.filter_by(public_id=id).first_or_404(f"{self.model} with ID '{id}' not found")
        return self.ns.marshal(obj, self.serializer, skip_none=True), 200

    def delete(self, id):
        obj = self.Model.query.filter_by(public_id=id).first_or_404(f"{self.model} with ID '{id}' not found.")

        db.session.delete(obj)
        db.session.commit()

        return {"success": f"{self.model} '{obj}' successfully deleted"}, 200

    def put(self, id):
        data = self.parser.parse_args()
        data = {key:val for key,val in data.items() if val is not None}
        data = clean_data(data)

        result = self.Model.query.filter_by(public_id=id)

        obj = result.first_or_404(f"{self.model} with ID '{id}' not found")

        for key,val in data.items():
            if isinstance(val, list):
                for item in val:
                    getattr(obj, key).append(item)
            else:
                setattr(obj, key, val)

        try:
            db.session.commit()
        except:
            self.ns.abort(409, f"New values already exist for another {self.model}")
            #return {"error": f"Updated values already exist for another {self.model}"}

        return self.ns.marshal(obj, self.serializer, skip_none=True), 200    