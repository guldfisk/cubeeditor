
from mtgorp.db.database import CardDatabase
from mtgorp.db.load import Loader, DBLoadException
from mtgorp.managejson.update import update
from mtgorp.models.serilization.strategies.strategy import Strategy
from mtgorp.models.serilization.strategies.jsonid import JsonId

from mtgqt.pixmapload.pixmaploader import PixmapLoader


class Context(object):
	
	db = None #type: CardDatabase
	pixmap_loader = None #type: PixmapLoader
	serialization_strategy = None #type: Strategy

	@classmethod
	def init(cls):
		cls.pixmap_loader = PixmapLoader(
			pixmap_executor = 30,
			printing_executor = 30,
			imageable_executor = 30,
		)

		try:
			cls.db = Loader.load()
		except DBLoadException:
			update()
			cls.db = Loader.load()

		cls.serialization_strategy = JsonId(cls.db)