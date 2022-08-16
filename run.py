from waitress import serve
from scope2screen import app
import multiprocessing
import sys

if __name__ == '__main__':
    multiprocessing.freeze_support()
    port = 8000 if len(sys.argv) < 2 or not str.isdigit(sys.argv[1]) else sys.argv[1]
    print('Serving on 0.0.0.0:' + str(port) + ' or http://localhost:' + str(port))
    serve(app, host='0.0.0.0', port=port, max_request_body_size=107374182400, max_request_header_size=8589934592)

