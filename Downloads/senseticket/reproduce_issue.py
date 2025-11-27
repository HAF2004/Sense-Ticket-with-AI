import sys
import os
import traceback

# Add current directory to path
sys.path.insert(0, os.getcwd())

try:
    from app import app, dashboard
    
    print("Attempting to execute dashboard function directly...")
    
    with open('traceback.txt', 'w') as f:
        with app.test_request_context():
            try:
                dashboard()
                print("Success! Dashboard executed without error.")
            except Exception:
                print("Caught exception during execution, writing to traceback.txt")
                traceback.print_exc(file=f)
            
except Exception as e:
    print("Caught exception during setup:")
    traceback.print_exc()
