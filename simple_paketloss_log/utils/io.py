from simple_paketloss_log.utils.measurement import Measurement


def load_measurements(filename, delimiter_line='---------------------', fail_line='Trying to start a new check, but check already running\n'):
    """Load measurements from a file."""
    measurements = []
    with open(filename, 'r') as f:
        buffer = [] # Holds the lines of the current check
        for line in f:
            if line.startswith(delimiter_line):
                measurements.append(Measurement.from_buffer(buffer))
                buffer = []
            elif line == fail_line:
                continue
            else:
                buffer.append(line)
    
    return measurements


def print_summary(measurements):
    "Print a summary of measurements."
    print(f"Found {len(measurements)} measurements")
    print(f"Maximal paket loss: {max([m.paket_loss for m in measurements])}")
    print(f"Average rtt: {sum([m.rtt_avg for m in measurements])/len(measurements)} ms")
