.PHONY: console console-quiet .uv

.uv:
	@if ! which uv > /dev/null 2>&1; then \
		echo "uv n'est pas installé. Installation en cours..."; \
		curl -LsSf https://astral.sh/uv/install.sh | sh; \
	fi

default: .uv
	@uv run textual run --dev src/main.py

console: .uv
	@uv run textual console

console-quiet: .uv
	@uv run textual console -x EVENT
	#@uv run textual console -x SYSTEM -x EVENT -x DEBUG -x INFO

pre-commit: .uv
	@uv run pre-commit run --all-files
