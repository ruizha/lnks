import argparse
from app import app

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Run lnks app")
    parser.add_argument("--host", type=str, default="127.0.0.1", help="host to listen to")
    args = parser.parse_args()
    app.router.run(host=args.host, debug=True)