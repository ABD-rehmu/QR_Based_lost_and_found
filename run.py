import sys
import os

# Ensure UTF-8 stdout encoding on Windows
if sys.platform == "win32":
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

import uvicorn

if __name__ == "__main__":
    print("\n" + "="*70)
    print(" [*] CampusTag - Smart QR Lost & Found Platform with Instant Match")
    print("="*70)
    print(" >>> ACCESS ALL FEATURES AT THIS SINGLE LINK:")
    print("     http://localhost:8000")
    print("="*70 + "\n")
    
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
