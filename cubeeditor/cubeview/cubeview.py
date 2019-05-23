import typing as t

from PyQt5.QtWidgets import QWidget, QLabel, QHBoxLayout

from mtgorp.models.persistent.printing import Printing

from magiccube.collections.cube import Cube


class CubeView(QWidget):

	def __init__(self, parent: t.Optional[QWidget] = None, name: str = '', cube: t.Optional[Cube] = None):
		super().__init__(parent)

		self.name = name

		self._cube = None

		layout = QHBoxLayout()

		self._cube_list = QLabel()

		layout.addWidget(self._cube_list)

		self.setLayout(layout)

		if cube is not None:
			self.set_cube(cube)

	@property
	def cube(self) -> Cube:
		return self._cube

	def set_cube(self, cube: Cube):
		self._cube = cube
		self._cube_list.setText(
			self._cube_to_text(
				cube
			)
		)

	@classmethod
	def _cube_to_text(cls, cube: Cube) -> str:
		return '\n'.join(
			f'{multiplicity}x {item}'
			for item, multiplicity in
			sorted(
				cube.cubeables.items(),
				key=lambda item: item[0].cardboard.name if isinstance(item[0], Printing) else str(hash(item[0]))
			)
		)