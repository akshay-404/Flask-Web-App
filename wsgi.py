import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from app import app as application  # if your Flask instance is in app.py

if __name__ == "__main__":
    application.run()
