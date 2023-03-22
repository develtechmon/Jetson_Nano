# Jetson Nano Service Installation

## Getting started

To start use `vi` or `gedit` to access into `crontab`. Refer to below guide on how to install
the service

```
$crontab -e

and below command

@reboot sudo /usr/bin/python3 /home/jlukas/Desktop/My_Project/Flask/Flask_Gate_System/v1_1/app_rpi_client_get_api_2nd_method.py &

$sudo reboot now

```