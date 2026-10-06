
# go to the project folder
cd "$(dirname "$0")"

# create the virtual environment if it does not exist
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi

# install dependencies and start the app
.venv/bin/pip install -r requirements.txt
.venv/bin/python run.py
