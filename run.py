import argparse
import uvicorn

def main():
    parser = argparse.ArgumentParser(description="Ticket Management System Runner")
    
    parser.add_argument("--host", default="0.0.0.0", help="Host interface to bind (default: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=8000, help="Port to run the server on (default: 8000)")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload for development")
    parser.add_argument("--log-level", choices=["debug", "info", "warning", "error", "critical"], default="info", help="Set the logging level (default: info)")

    args = parser.parse_args()

    uvicorn_config = {
        "app": "app.main:app",
        "host": args.host,
        "port": args.port,
        "log_level": args.log_level
    }

    print(f"{' Starting Ticket Management System ':^50}")
    print(f"Host: {uvicorn_config['host']}")
    print(f"Port: {uvicorn_config['port']}")
    print(f"Log Level: {uvicorn_config['log_level']}")
    print('=' * 50)

    uvicorn.run(**uvicorn_config)

if __name__ == "__main__":
    main()
