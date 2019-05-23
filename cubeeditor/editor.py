import typing as t

import sys
import time
import os

from threading import Lock

from promise import Promise

from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QMainWindow, QAction, QDialog, QLabel

from mtgorp.models.serilization.strategies.strategy import SerializationException

from magiccube.collections.cube import Cube
from magiccube.laps.lap import Lap

from cubeeditor.context.context import Context
from cubeeditor import paths

from cubeeditor.cubeview.cubeview import CubeView
from cubeeditor.laprating.laprate import LapRater


class CubeTabs(QtWidgets.QTabWidget):
	DEFAULT_TEMPLATE = 'New Cube {}'

	def __init__(self, parent: QtWidgets.QWidget = None):
		super().__init__(parent)
		self._new_decks = 0
		self.setTabsClosable(True)

		self.tabCloseRequested.connect(self._tab_close_requested)
		# self.currentChanged.connect(self._current_changed)

	def add_cube(self, cube_view: CubeView) -> None:
		self.addTab(cube_view, cube_view.name)

	def new_cube(self) -> CubeView:
		deck_widget = CubeView(
			name = self.DEFAULT_TEMPLATE.format(self._new_decks),
		)
		self.add_cube(
			deck_widget
		)
		self._new_decks += 1

		return deck_widget

	def _tab_close_requested(self, index: int) -> None:
		if index == 0:
			self.new_deck()

		self.removeTab(index)

	@property
	def active_cube(self) -> Cube:
		active_tab = self.currentWidget() #type: CubeView
		return active_tab.cube

	# def _current_changed(self, index: int) -> None:
	# 	Context.deck_list_view.set_deck.emit(
	# 		self.currentWidget().maindeck.printings,
	# 		self.currentWidget().sideboard.printings,
	# 	)


class MainWindow(QMainWindow):

	def __init__(self, parent: QWidget = None, *args, **kwargs):
		super().__init__(parent, *args, **kwargs)

		self.setWindowTitle('Cube Editor')

		self._cube_tabs = CubeTabs(self)
		self.setCentralWidget(self._cube_tabs)

		menu_bar = self.menuBar()

		all_menus = {
			menu_bar.addMenu('File'): (
				('Exit', 'Ctrl+Q', QtWidgets.qApp.quit),
				('New Cube', 'Ctrl+N', lambda : None),
				('Open Cube', 'Ctrl+O', self._load_cube),
				('Save Cube', 'Ctrl+S', lambda : None),
				('Close Cube', 'Ctrl+W', lambda : None),
			),
			menu_bar.addMenu('tools'): (
				('Rate Traps', 'Ctrl+R', self._rate_traps),
			)
		}

		for menu in all_menus:
			for name, shortcut, action in all_menus[menu]:
				_action = QAction(name, self)

				if shortcut:
					_action.setShortcut(shortcut)

				_action.triggered.connect(action)
				menu.addAction(_action)

	def _rate_traps(self) -> None:

		dialog = LapRater(self)
		dialog.show()
		dialog.rate_laps(
			self._cube_tabs.active_cube.laps
		)

	def _load_cube(self) -> None:
		dialog = QtWidgets.QFileDialog(self)
		dialog.setFileMode(QtWidgets.QFileDialog.ExistingFile)
		dialog.setViewMode(QtWidgets.QFileDialog.List)
		dialog.setDirectory(paths.DEFAULT_CUBE_DIR)

		if not dialog.exec_():
			return

		file_names = dialog.selectedFiles()

		print(file_names)

		if not file_names:
			return

		file_name = file_names[0]

		with open(file_name, 'r') as f:
			try:
				cube = Context.serialization_strategy.deserialize(
					Cube,
					f.read(),
				)
			except SerializationException as e:
				print(e)
				return

		self._cube_tabs.add_cube(
			CubeView(cube=cube)
		)


def run():

	app = QtWidgets.QApplication(sys.argv)

	Context.init()


	with open(os.path.join(paths.RESOURCE_PATH, 'style.qss'), 'r') as f:

		app.setStyleSheet(
			f.read().replace(
				'url(',
				'url(' + os.path.join(
					paths.RESOURCE_PATH,
					'qss_icons',
					'rc',
					'',
				),
			)
		)

	app.setOrganizationName('EmbargoSoft')
	app.setOrganizationDomain('ce.lost-world.dk')
	app.setApplicationName('Cube Editor')


	w = MainWindow()

	w.showMaximized()

	sys.exit(app.exec_())


if __name__ == '__main__':
	run()