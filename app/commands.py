from flask.cli import with_appcontext
import click
from . import db
from .models import Song, Album, Artist, User, Genre

@click.command(name="createdb")
@with_appcontext
def create_db():
    db.create_all()

@click.command(name="dropdb")
@with_appcontext
def drop_db():
    db.drop_all()

@click.command(name="populatedb")
@with_appcontext
def populate_db():
    red = User(username="Red", email="blaizepaschal@gmail,com", password="password")
    kal = User("Kal.xv", "ucheoma.uwakwe@gmail.com")

    kendrick = Artist(name="Kendrick Lamar", url="kendrick.com")
    taylor = Artist(name="Taylor Swift", url="taylor.com")
    kanye = Artist(name="Kanye West", url="kanye.com")
    eminem = Artist(name="Eminem", url="eminem.com")
    drake = Artist(name="Drake", url="drizzy.com")
    u2 = Artist(name="U2", url="u2.com")

    hiphop = Genre("Hip-Hop/Rap")

    tpab = Album("To Pimp a Butterfly", "tpab.com", kendrick, 2015, hiphop)
    damn = Album("DAMN.", "damn.com", kendrick, 2017, hiphop)
    gkmc = Album("good kid m.A.A.d city", "gkmc.com", kendrick, 2012, hiphop)

    sherane = Song(name="Sherane", url="sherane.com", year=2012, artist=kendrick, album=gkmc, track_number=1)
    samidot = Song(name="Sing About Me, I'm Dying Of Thirst", url="samidot.com", year=2012, artist=kendrick, album=gkmc, track_number=2)
    taopp = Song(name="The Art of Peer Pressure", url="taopp.com", year=2012, artist=kendrick, album=gkmc, track_number=3)
    money_trees = Song(name="Money Trees", url="moneytrees.com", year=2012, artist=kendrick, album=gkmc, track_number=4)
    poetic_justice = Song(name="Poetic Jusitce", url="poeticjustice.com", year=2012, artist=kendrick, album=gkmc, featuring=[drake], track_number=5)

    pride = Song(name="PRIDE.", url="pride.com", year=2017, artist=kendrick, album=damn, track_number=1)
    humble = Song(name="HUMBLE.", url="humble.com", year=2017, artist=kendrick, album=damn, track_number=2)
    loyalty = Song(name="LOYALTY.", url="loyalty.com", year=2017, artist=kendrick, album=damn, track_number=3)
    lust = Song(name="LUST.", url="lust.com", year=2017, artist=kendrick, album=damn, track_number=4)
    ducky = Song(name="DUCKWORTH.", url="ducky.com", year=2017, artist=kendrick, album=damn, track_number=5)
    xxx = Song(name="XXX.", url="xxx.com", artist=kendrick, year=2017, featuring=[u2], album=damn, track_number=6)

    db.session.add(red)
    db.session.add(kal)
    db.session.add(kendrick)
    db.session.add(taylor)
    db.session.add(kanye)
    db.session.add(eminem)
    db.session.add(drake)
    db.session.commit()

