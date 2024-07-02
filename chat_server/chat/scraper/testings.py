import sys
import time

print("Press Control-C to stop the program")
i = 0
while i < 100:
    try:
        time.sleep(1)  # Simulate a long-running process
        i += 1
    except KeyboardInterrupt:
        print("\nProgram interrupted with Control-C")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {e}")
