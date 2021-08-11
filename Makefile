default:help
py := python

help:
	@echo "USAGE"
	@echo "  make <commands>"
	@echo ""
	@echo "AVAILABLE COMMANDS"
	@echo "  run		Start a CI server"
	@echo "  run-reload	Start a CI server with statreload"


# ========
# Commands
# ========

run:
	$(py) -m uvicorn server:app --port 1337

run-reload:
	$(py) -m uvicorn server:app --port 1337 --reload

