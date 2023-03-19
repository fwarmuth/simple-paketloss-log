import datetime
from dataclasses import dataclass

@dataclass
class Measurement:
    """A measurement of a ping to a host."""
    timestamp: datetime.datetime  = None # timestamp at end of measurement
    duration: float = None  # duration of measurement in miliseconds
    pakets_sent: int = None  # number of pakets sent
    pakets_received: int = None  # number of pakets received
    pakets_lost: int = None  # number of pakets lost
    paket_loss: float = None  # percentage of pakets lost
    rtt_min: float = None  # minimum round trip time in miliseconds
    rtt_avg: float = None  # average round trip time in miliseconds
    rtt_max: float = None  # maximum round trip time in miliseconds
    rtt_mdev: float = None  # standard deviation of round trip time in miliseconds

    @classmethod
    def from_buffer(self, buffer):
        """Parse a buffer and return a Measurement object"""
        result = Measurement() # create empty object

        # first line
        line = buffer[0]
        result.timestamp = datetime.datetime.strptime(line[1:19], "%Y-%m-%d %H:%M:%S")
        # 2nd line
        line = buffer[1].replace("\n", "")
        splits = line.split(" ")
        result.duration = float(splits[-1][:-2])
        result.pakets_sent = int(splits[2])
        result.pakets_received = int(splits[5])
        result.pakets_lost = int(result.pakets_sent - result.pakets_received)
        result.paket_loss = float(splits[7][:1])/100
        # 3rd line
        line = buffer[2].replace("\n", "")
        splits = line.split("/")
        result.rtt_min = float(splits[3].split(" ")[-1])
        result.rtt_avg = float(splits[4])
        result.rtt_max = float(splits[5])
        result.rtt_mdev = float(splits[6].split(' ')[0])

        return result

    def __str__(self):
        return f"{self.timestamp}: pakets: {self.pakets_sent}, loss: {self.paket_loss}"
