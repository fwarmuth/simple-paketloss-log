> **_NOTE:_**  Work in progress!
# Simple Paketloss Log
Simple tool to visualize `ping`s output.
This tool parses a simple `ping` std output and is able to create graphs using `matplotlib`.

A furture feature will be the posting to a `influxdb` to do a easy interactive visualization using `grafana` or so.

# Install:
This project uses `PyPoetry` as dependency management and structure.
- Install `pypoetry`
- Run `poetry install`
- Within that poetry env one can use the `simple-paketloss-log` cli.

# How to:
## 1. Setup a periodic `ping` run using `cron`:
- I use `pingcheck.sh` to trigger a such call with some parameters.
- The result gets append to a `ping.log` file.
- After every run, a `delimiter` line is added.
- To prevent from concurrent running, if one takes longer than 30s, i introduce a locking mechanism.

`crontab` setup: I start a ping run each 30s.
```
$ crontab -e
* * * * *  <PathToScript>/pingcheck.sh
* * * * * ( sleep 30 ; <PathToScript>/pingcheck.sh )
```
## 2. Wait until some runs logged in to the `ping.log`.
## 3. Run the `simple-paketloss-log` cli
### **Read** same measurements:
```
$ simple-paketloss-log read ping.log
```
Output:
```
Read measurements from file ping.log
Found 3098 measurements
Maximal paket loss: 0.09
Average rtt: 9.81804519044544 ms
``` 
### Create a **graph**:
```
$ simple-paketloss-log graph ping.log 
```

Output:

![image](docs/images/paket_loss.png)