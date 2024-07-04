# SDRPlayBatDetector

Hat tip to TechMinds for outlining the [art of the possible](https://www.youtube.com/watch?v=-ikeMSn35T0) here.

Now have more insight as to when these fascinating beasties visit my back garden.

# Installation

Tested on Pi Debian Bookwork 64bit 2024-03-15.

I connected [one of these](https://www.ebay.co.uk/itm/115592159244) to [one of those](https://www.sdrplay.com/sdrplay-announces-the-rspdx-r2/) for this.

Some experience will be needed with Linux, GnuRadio and a sensor / SDR receiver pair that works in the range 40 to 120 kHz or so.

```console
sudo apt-get update upgrade
sudo apt-get install cmake gnuradio python3-paho-mqtt ffmpeg
```

Then follow the instructions here to install required APIs:

https://www.sdrplay.com/api/

https://github.com/fventuri/gr-sdrplay3

# Design

![GRC sketch](./sketch.png)

This sketch uses an asistant python program called [zmqpubsink.py](./zmqpubsink.py) which looks for bat activity as defined by the [config file](SDRPlayBatDetector.ini) and

- Sends out frequency shifted audio of the latest event to the default sound card and/or a remote location.
- Creates a csv file of events for further analysis and visualisation.
- Optionally sends events to your messaging server.

# Configuration file

Edit the [config file](SDRPlayBatDetector.ini) to adjust the following

| Key | Notes |
|    :----:   |          :--- |
| sample_rate  | Suggest leaving, may need to subsequently tweak the decimation and interpolation values on the graph. |
| fft_resolution | Suggest leaving works well on Pi4 @ 18% CPU. |
| fft_frame_rate  | Ditto. |
| squelch | You will need to increase or decrease this depending on environmental noise. |
| default_tuning_frequency  | This will change automatically as activity happens. |
| start_freq  | Where to start looking for bats. |
| end_freq  | If you need to increase this, you will need to increase the sample rate and then maybe tweak the decimation and interpolation values on the graph. |
| freq_bin_range  | The fft is re-aggregrated based on this size to allow for more detailed but not over the top event generation. |
| trigger_gain_threshold  | Spike in received power required to generate an event. |
| retrigger_seconds | Do not generate more than one event in this 'comparison against rolling average' interval. |
| mqtt_ip_address  | Optional messaging server. |
| mqtt_username  | Ditto. |
| mqtt_password  | Ditto. |
| mqtt_topic  | Ditto. |

# Starting and stopping

```console
bash start.sh
```

```console
bash stop.sh
```

# Example output

A real-time csv file is created with a timestamp and peak frequency of the bat event. 

```console
pi@ShedPi:~/Documents/SDRPlayBatDetector $ tail -f SDRPlayBatDetector.csv 
2024-07-01 13:29:59,66465
2024-07-01 13:30:00,70859
2024-07-01 13:30:02,69395
2024-07-01 13:30:03,55488
2024-07-01 13:30:04,70859
```

# Configuration

Edit the gnuradio sketch source block if you have a different source than the rspdx-r2.

For remote audio place you remote IP and port in the [UDP sink](./sketch.png) block and run this at the remote end:

```console
ffplay -f f32le -ar 24000 -sync ext -fflags nobuffer -nodisp -i udp://127.0.0.1:50243
```

# Notes

I have to initially connect then disconnect a SDRconnect client after a reboot on the target to allow the gnuradio graph to work. 

Can do this remotely using the excellent [VirtualHere](https://www.virtualhere.com/).

Enjoy!

