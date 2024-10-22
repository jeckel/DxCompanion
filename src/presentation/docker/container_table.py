from textual.widgets import DataTable
from textual import work, on
import subprocess

from models import Project


class ContainerTable(DataTable):
    """
    DataTable for listing docker containers for a project.
    """
    def __init__(self, title: str, project: Project, **kwargs):
        super().__init__(**kwargs)
        self.border_title = title
        self.project = project
        self.add_columns(*("Name", "Command", "State", "Ports"))
        self.cursor_type = "row"

    async def on_mount(self):
        # self.loading = True
        self.refresh_containers()


    @work(exclusive=True, thread=True)
    async def refresh_containers(self):
        self.clear()
        # Run the docker compose ps command
        process = subprocess.run(
            ["docker", "compose", "ps"],
            cwd=self.project.path,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        # Check for errors
        if process.returncode != 0:
            error_message = process.stderr.strip() if process.stderr else "Unknown error occurred."
            self.add_row("Error", error_message, "", "")
            return

        # Process the output
        output_lines = process.stdout.strip().split('\n')

        # Skip the header line and empty lines
        for line in output_lines[2:]:
            parts = line.split()
            if len(parts) < 4:
                continue  # Skip if there are not enough parts

            # Extract relevant fields
            name = parts[0]
            command = " ".join(parts[1:-2])  # Command can have spaces
            state = parts[-2]
            ports = parts[-1]

            # Add a row to the DataTable
            self.add_row(*[name, command, state, ports], key=name)