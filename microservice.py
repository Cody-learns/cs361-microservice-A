import zmq
import json
import io
import matplotlib.pyplot as plt

# Set port below
port = 5555

# Set ZMQ context and bind socket to port
context = zmq.Context()
socket = context.socket(zmq.REP)
socket.bind(f"tcp://*:{port}")

# Listen for request from client
while True:
    print("Server is listening...")

    message = socket.recv().decode()

    # Print confirmation of receipt to console
    print("Request received!")

    # Parse payload
    try:
        payload = json.loads(message)
        data = payload.get("data", [])
        title = payload.get("title", "Histogram")
        xlabel = payload.get("xlabel", "Values")
        ylabel = payload.get("ylabel", "Frequency")
        bins = payload.get("bins", 10)

        # Validate payload data
        if not isinstance(data, list) or not all(isinstance(i, (int, float)) for i in data):
            socket.send_string("Error: Invalid request, 'data' must be a list of numbers")
            print("Response sent: Invalid data was received :(")
            continue

        # Create histogram
        else:
            plt.figure()
            plt.hist(data, bins=bins, edgecolor='black')
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.title(title)

            # Store the histogram as a .png in memory
            buffer = io.BytesIO()
            plt.savefig(buffer, format="png")
            plt.close()

            # Send image bytes in response
            socket.send(buffer.getvalue())
            print("Response sent!")

    except Exception as e:
        socket.send_string(f"Error: {str(e)}")
        print(f"Response sent: There was an error: {str(e)}")