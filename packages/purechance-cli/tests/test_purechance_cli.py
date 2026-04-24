from importlib import metadata
from types import ModuleType

import purechance


def test_project_name(project_name: str, project_pkg: ModuleType):
    assert project_pkg.__name__ == project_name


def test_project_version(project_name: str, project_pkg: ModuleType):
    assert project_pkg.__version__ == metadata.version(project_name)


def test_lib_name():
    assert purechance.__name__ == "purechance"
