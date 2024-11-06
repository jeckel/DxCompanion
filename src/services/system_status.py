import subprocess

from .base_service import BaseService

class SystemStatus(BaseService):
    @staticmethod
    def _capture_output(command: list[str]) -> str | None:
        try:
            result = subprocess.run(command, capture_output=True, text=True, check=True)
            return result.stdout
        except (subprocess.CalledProcessError, FileNotFoundError):
            return None

    @staticmethod
    def _capture_version(output: str, line_number: int = 0, position: int = 1) -> str:
        version_line = output.splitlines()[line_number]
        version = version_line.split()[position]
        return version

    def php_version(self) -> str|None:
        output = self._capture_output(['php', '-v'])
        return None if output is None else self._capture_version(output)

    def composer_version(self) -> str|None:
        output = self._capture_output(['composer', '--version'])
        return None if output is None else self._capture_version(output, position=2)

    def castor_version(self) -> str|None:
        output = self._capture_output(['castor', '--version'])
        return None if output is None else self._capture_version(output)[1:]

    def symfony_version(self) -> str|None:
        output = self._capture_output(['symfony', 'version', '--no-ansi'])
        return None if output is None else self._capture_version(output, position=3)

    def docker_version(self) -> str|None:
        output = self._capture_output(['docker', '-v'])
        return None if output is None else self._capture_version(output, position=2)[:-1]

    def ansible_version(self) -> str|None:
        output = self._capture_output(['ansible', '--version'])
        return None if output is None else self._capture_version(output, position=2)[:-1]

    def git_version(self) -> str|None:
        output = self._capture_output(['git', '--version'])
        return None if output is None else self._capture_version(output, position=2)
