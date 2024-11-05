import subprocess

from .base_service import BaseService

class SystemStatus(BaseService):
    def _capture_output(self, command: list[str]) -> str|None:
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            return result.stdout
        except (subprocess.CalledProcessError, FileNotFoundError):
            return None

    def php_version(self) -> str|None:
        output = self._capture_output(['php', '-v'])
        if output is None:
            return None
        version_line = output.splitlines()[0]
        version = version_line.split()[1]
        return version
    def composer_version(self) -> str|None:
        output = self._capture_output(['composer', '--version'])
        if output is None:
            return None

        version_line = output.splitlines()[0]
        version = version_line.split()[2]
        return version

    def castor_version(self) -> str|None:
        output = self._capture_output(['castor', '--version'])
        if output is None:
            return None

        version_line = output.splitlines()[0]
        version = version_line.split()[1]
        return version[1:]

    def symfony_version(self) -> str|None:
        output = self._capture_output(['symfony', 'version', '--no-ansi'])
        if output is None:
            return None

        version_line = output.splitlines()[0]
        version = version_line.split()[3]
        return version

    def docker_version(self) -> str|None:
        output = self._capture_output(['docker', '-v'])
        if output is None:
            return None

        version_line = output.splitlines()[0]
        version = version_line.split()[2]
        return version[:-1]

    def ansible_version(self) -> str|None:
        output = self._capture_output(['ansible', '--version'])
        if output is None:
            return None

        version_line = output.splitlines()[0]
        version = version_line.split()[2]
        return version[:-1]
