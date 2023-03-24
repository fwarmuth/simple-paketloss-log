import os

import click
import loguru
import tqdm

from simple_paketloss_log.utils.io import load_measurements, print_summary
from simple_paketloss_log.utils.visuals import plot_loss
from simple_paketloss_log.utils.influxdb import add_measurement
from simple_paketloss_log.utils.watch import watch_file

@click.group()
def cli():
    pass

@cli.command()
@click.argument('filename')
@click.option('-v', '--verbose', count=True)
def read(filename, verbose):
    # Set log level
    if verbose == 1:
        loguru.logger.level("INFO")
    elif verbose >= 2:
        loguru.logger.level("DEBUG")
    else:
        loguru.logger.level("WARNING")

    measurements = load_measurements(filename)

    print(f"Read measurements from file {filename}")
    print_summary(measurements)


@cli.command()
@click.argument('filename')
@click.option('-v', '--verbose', count=True)
def graph(filename, verbose):
    "Create a graph of measurements in a file."
    print("Create graph of measurements in file", filename)

    # Set log level
    if verbose == 1:
        loguru.logger.level("INFO")
    elif verbose >= 2:
        loguru.logger.level("DEBUG")
    else:
        loguru.logger.level("WARNING")
    
    # Load measurements
    measurements = load_measurements(filename)

    # Create graph
    fig = plot_loss(measurements, "Paket loss")
    fig.savefig("paket_loss.png")

    # Plot summary
    print_summary(measurements)

@cli.command()
@click.argument('filename')
@click.option('-v', '--verbose', count=True)
@click.option('-h', '--host', default="influxdb.dmz:8086")
@click.option('-t', '--token', default=None)
@click.option('-o', '--org', default="home")
@click.option('-b', '--bucket', default="simple-paketloss")
def send2influx(filename, verbose, host, token, org, bucket):
    "Send measurements to InfluxDB"
    print("Send measurements to InfluxDB")
    # Set log level
    if verbose == 1:
        loguru.logger.level("INFO")
    elif verbose >= 2:
        loguru.logger.level("DEBUG")
    else:
        loguru.logger.level("WARNING")
    
    if token is None:
        token = os.environ.get("INFLUXDB_TOKEN")
        if token is None:
            raise ValueError("No token provided and INFLUXDB_TOKEN environment variable not set.")

    measurements = load_measurements(filename)
    for measurement in tqdm.tqdm(measurements):
        add_measurement(host, token, org, bucket, measurement)

@cli.command()
@click.argument('filename')
@click.option('-v', '--verbose', count=True)
@click.option('-h', '--host', default="influxdb.dmz:8086")
@click.option('-t', '--token', default=None)
@click.option('-o', '--org', default="home")
@click.option('-b', '--bucket', default="simple-paketloss")
def watch(filename, verbose, host, token, org, bucket):
    """Watch a file for changes and send new measurements to InfluxDB."""
    print("Watch file for changes and send new measurements to InfluxDB")
    # Set log level
    if verbose == 1:
        loguru.logger.level("INFO")
    elif verbose >= 2:
        loguru.logger.level("DEBUG")
    else:
        loguru.logger.level("WARNING")
    
    if token is None:
        token = os.environ.get("INFLUXDB_TOKEN")
        if token is None:
            raise ValueError("No token provided and INFLUXDB_TOKEN environment variable not set.")
    
    watch_file(filename, host, token, org, bucket)


@cli.command()
@click.argument('filename')
@click.option('-v', '--verbose', count=True)
@click.option('-h', '--host', default="influxdb.dmz:8086")
@click.option('-t', '--token', default=None)
@click.option('-o', '--org', default="home")
@click.option('-b', '--bucket', default="simple-paketloss")
def read_and_watch(filename, verbose, host, token, org, bucket):
    """Read measurements from a file and send them to InfluxDB.
    Then watch the file for changes and send new measurements to InfluxDB."""
    print("Read measurements from a file and send them to InfluxDB. Then watch the file for changes and send new measurements to InfluxDB.")
    # Set log level
    if verbose == 1:
        loguru.logger.level("INFO")
    elif verbose >= 2:
        loguru.logger.level("DEBUG")
    else:
        loguru.logger.level("WARNING")
    
    if token is None:
        token = os.environ.get("INFLUXDB_TOKEN")
        if token is None:
            raise ValueError("No token provided and INFLUXDB_TOKEN environment variable not set.")
    
    measurements = load_measurements(filename)
    for measurement in tqdm.tqdm(measurements):
        add_measurement(host, token, org, bucket, measurement)
    
    watch_file(filename, host, token, org, bucket)



if __name__ == "__main__":
    cli()