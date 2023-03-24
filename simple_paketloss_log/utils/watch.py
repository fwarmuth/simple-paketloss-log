import os

from loguru import logger
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from simple_paketloss_log.utils.measurement import Measurement
from simple_paketloss_log.utils.influxdb import add_measurement

def read_last_n_lines(file_path, n):
    with open(file_path, 'rb') as file:
        file.seek(0, os.SEEK_END)
        position = file.tell()
        lines = []
        while position >= 0 and len(lines) < n:
            file.seek(position)
            next_char = file.read(1)
            if next_char == b'\n' and position != file.tell():
                line = file.readline().decode().rstrip()
                lines.append(line)
            position -= 1
        return lines[::-1]

def get_last_line(file_path):
    last_line = None
    with open(file_path, 'rb') as f:
        try:  # catch OSError in case of a one line file 
            f.seek(-2, os.SEEK_END)
            while f.read(1) != b'\n':
                f.seek(-2, os.SEEK_CUR)
        except OSError:
            f.seek(0)
        last_line = f.readline().decode()

    return last_line

class FileModifiedHandler(FileSystemEventHandler):
    def __init__(self, filename, host, token, org, bucket) -> None:
        self.filename = filename
        self.host = host
        self.token = token
        self.org = org
        self.bucket = bucket
        # 
        self.last_file_size = 0

        super().__init__()

    def on_modified(self, event):
        if event.src_path != self.filename:
            return None
        current_file_size = os.path.getsize(self.filename)
        if self.last_file_size != current_file_size:
            logger.info(f"File {self.filename} has been modified")
            lines = read_last_n_lines(self.filename, 5)
            lines = lines[:-2]
            measurement = Measurement.from_buffer(lines)
            add_measurement(self.host, self.token, self.org, self.bucket, measurement)
            self.last_file_size = current_file_size
    

def watch_file(filename, host, token, org, bucket):
    logger.info(f"Watching file {filename}")
    event_handler = FileModifiedHandler(filename, host, token, org, bucket)
    observer = Observer()
    observer.schedule(event_handler, path=filename, recursive=False)
    observer.start()
    
    try:
        while True:
            pass
    except KeyboardInterrupt:
        observer.stop()

