import click
import loguru

from simple_paketloss_log.utils.io import load_measurements, print_summary
from simple_paketloss_log.utils.visuals import plot_loss

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


if __name__ == "__main__":
    cli()