# DxCompanion, enhance your Developer eXperience

DxCompanion is a Terminal UI application used to provide usefull information about you're project status and easy access
to tools ot manage and monitor your project under development environment.

## Installation

- install uv
- git clone

## Run

```bash
uv run src/main.py <project-file.json>
```

## Your `<project-name>.json` file

You need one of this file per project configuration, it gives DxCompanion all the information to help you manage your project.

This is a json file which can look like this :
```json
{
    "path": "/path/to/project/directory",
    "project_name": "Name of your project",
    "package_managers": ["uv"]
}
```

Configuration options :

- `package_managers`: it's a list of packages manager to use with your project, actually supported are `composer` and `uv`
