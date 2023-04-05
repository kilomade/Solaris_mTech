import time

# Define the window size and interval for frequency averaging
WINDOW_SIZE = 10  # Number of data points to consider for frequency averaging
INTERVAL = 1.0  # Time interval in seconds between data points


# Define a function to read input data (in this case, we're simulating the data with a sine wave)
def read_data():
    t = 0
    while True:
        yield 50 + 50 * math.sin(2 * math.pi * t / 10)
        t += INTERVAL


# Define a function to calculate the frequency of a window of data points
def calculate_frequency(data):
    if len(data) < 2:
        return None
    else:
        dt = (data[-1][0] - data[0][0]) / (len(data) - 1)
        f = 1 / dt
        return f


# Initialize the data buffer and time counter
data_buffer = []
t_last = time.monotonic()

# Start reading input data and averaging its frequency
data_reader = read_data()
while True:
    # Read the next data point and update the time counter
    data_point = next(data_reader)
    t_now = time.monotonic()

    # Add the data point to the buffer and remove any points outside of the current window
    data_buffer.append((t_now, data_point))
    while len(data_buffer) > WINDOW_SIZE:
        data_buffer.pop(0)

    # If the window is full, calculate and print the average frequency of the data points in the window
    if len(data_buffer) == WINDOW_SIZE:
        frequency = calculate_frequency(data_buffer)
        if frequency is not None:
            print(f"Raw Input Average frequency: {frequency:.2f} Hz")

    # Wait until the next data point is due
    t_next = t_last + INTERVAL
    time.sleep(max(0, t_next - t_now))
    t_last = t_next
