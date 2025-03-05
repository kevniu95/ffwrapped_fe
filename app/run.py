import os
from app.index import app  # Adjust this import if necessary

port = int(os.getenv("PORT", 8080))  # Default to 8080 if PORT is not set

if __name__ == "__main__":
    app.run_server(host="0.0.0.0", port=port, debug=True)
