import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install("aniso8601")
install("click")
install("Flask")
install("Flask-RESTful")
install("Flask-SQLAlchemy")
install("itsdangerous")
install("Jinja2")
install("MarkupSafe")
install("pytz")
install("six")
install("SQLAlchemy")
install("Werkzeug")
install("pyjwt")