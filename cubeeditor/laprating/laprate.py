import typing as t

from threading import Lock

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QDialog, QLabel

from magiccube.collections.cube import Cube
from magiccube.laps.lap import Lap

from cubeeditor.context.context import Context


class LapLabel(QLabel):
	clicked = QtCore.pyqtSignal(QLabel)

	def __init__(self, parent: t.Optional[QWidget] = None):
		super().__init__(parent)
		self._lap = None #type: Lap

	def set_lap(self, lap: Lap) -> None:
		self._lap = lap
		self.setPixmap(
			Context.pixmap_loader.get_pixmap(lap)
		)

	def mousePressEvent(self, mouse_event: QtGui.QMouseEvent):
		print('mouse press', self)
		super().mousePressEvent(mouse_event)
		self.clicked.emit(self)


class LapRater(QDialog):

	def __init__(self, parent: QWidget):
		super().__init__(parent=parent)

		self._layout = QtWidgets.QHBoxLayout()

		self._left_label = LapLabel()
		self._right_label = LapLabel()

		self._left_label.clicked.connect(self._label_clicked)
		self._right_label.clicked.connect(self._label_clicked)

		self._layout.addWidget(self._left_label)
		self._layout.addWidget(self._right_label)

		self.setLayout(self._layout)

		self._lock = Lock()
		self._picked_lap = None  # type: Lap

	def _label_clicked(self, lap: Lap) -> None:
		self._picked_lap = lap
		self._lock.release()

	def _pick_one(self, first: Lap, second: Lap) -> Lap:
		self._left_label.setPixmap(
			Context.pixmap_loader.get_pixmap(first).get()
		)
		self._right_label.setPixmap(
			Context.pixmap_loader.get_pixmap(second).get()
		)

		self._lock.acquire()
		return self._picked_lap

	def rate_laps(self, laps: t.Collection[Lap]) -> t.List[Lap]:

		list_laps = list(laps)

		first_lap, second_lap = list_laps[0], list_laps[1]

		print(self._pick_one(first_lap, second_lap))



		return list(laps)
