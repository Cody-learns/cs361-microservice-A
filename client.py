import zmq
import os

# Set port below
port = 5555

# Set ZMQ context and socket connection
context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect(f"tcp://localhost:{port}")

# Sample payload
payload = {
    "data": [3, 1, 1, 2, 3, 2, 2, 3, 4, 5, 2, 1, 3, 4, 5, 3, 1, 2, 4, 3, 2, 1, 3, 3],
    "title": "Very Awesome Histogram",
    "xlabel": "X Values",
    "ylabel": "Y Frequency",
    "bins": 5
}

# Send example request
input = input("Press enter to send the test payload...")
socket.send_json(payload)

# Receive request
response = socket.recv()

# Check for errors
if response.startswith(b"Error"):
    print(response.decode())

# Save and open image   
else:
    with open("example.png", "wb") as f:
        f.write(response)
        print("Histogram received! Opening now...")

        # Change below if you're not running windows
        os.startfile("example.png")