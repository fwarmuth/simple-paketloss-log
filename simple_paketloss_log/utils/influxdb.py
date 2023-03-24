from dataclasses import asdict
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb_client.rest import ApiException


def add_measurement(host, token, org, bucket, measurement, name="Default", tags=None, timestamp=None):
    """
    Add a measurement to an InfluxDB v2 database.
    Args:
    host (str): The URL of the InfluxDB v2 host.
    token (str): An authorization token with write access to the database.
    org (str): The name of the organization that owns the database.
    bucket (str): The name of the bucket to write to.
    measurement (str): The name of the measurement to add.
    tags (dict, optional): A dictionary of tag values for the measurement. Defaults to None.
    timestamp (str, optional): A timestamp for the measurement in ISO-8601 format. Defaults to None.
    """

    client = InfluxDBClient(url=host, token=token)
    query_api = client.query_api()
    write_api = client.write_api(write_options=SYNCHRONOUS)

    # Convert the datetime object to a Unix timestamp in seconds
    timestamp_sec = measurement.timestamp.timestamp()
    # Convert the timestamp to nanoseconds
    timestamp_ns = int(timestamp_sec * 1000000000)
    # Save it in measurement
    measurement.timestamp = timestamp_ns

    # Create a new point and write it to the database
    point = Point(name)

    # point.fields(asdict(measurement))
    for key, value in asdict(measurement).items():
        point.field(key, value)

    if tags:
        point.tags(tags)
    if timestamp:
        point.time(timestamp)
    elif measurement.timestamp:
        point.time(measurement.timestamp)

    write_api.write(bucket=bucket, org=org, record=point, write_precision="ns")
    print(f"Measurement '{measurement}' added to database.")