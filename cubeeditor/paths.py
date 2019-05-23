

import os

from appdirs import AppDirs


RESOURCE_PATH = os.path.join(
	os.path.dirname(
		os.path.realpath(__file__)
	),
	'resources',
)

DEFAULT_CUBE_DIR = os.path.join(
	AppDirs('misccube', 'misccube').user_data_dir,
	'cubes',
)