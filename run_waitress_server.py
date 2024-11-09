# run_waitress_server.py

from waitress import serve
from Videogames_project.wsgi import application

if __name__ == '__main__':
    serve(application, host='0.0.0.0', port=8000)