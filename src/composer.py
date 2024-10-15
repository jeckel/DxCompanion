import subprocess
from typing import Optional, List

from models import Project


def run_composer(command, project: Project, extra_args: Optional[List[str]] = None):
    composer_command = ["composer", command]
    if extra_args:
        composer_command.extend(extra_args)

    result = subprocess.run(composer_command, cwd=project.path, capture_output=True, text=True)
    print("stdout:", result.stdout)
    print("stderr:", result.stderr)

    #
    # with subprocess.Popen(
    #     composer_command,
    #     cwd=project.path,
    #     stdout=subprocess.PIPE,
    #     # stderr=subprocess.PIPE,
    #     # text=True
    # ) as process:
    #     print(f"Sortie: {process.stdout.read().strip()}")
    #
    # stderr = process.communicate()[1]
    # if stderr:
    #     print(f"Erreurs: {stderr}")

# Exemple d'utilisation
# output = run_composer("install", working_directory="/path/to/your/project")