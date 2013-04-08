#!/usr/bin/env python2
#
# Contains a basic gui for recording EEG data. Displays real-time graphs of the eeg signals. Should
# eventually contain a real-time scrolling scalogram.

import emotiv
import gevent

import matplotlib
import matplotlib.pyplot as plot

import numpy

matplotlib.use('Qt4Agg')

# Sensor channels.
channels = [
  'F3',
  'FC6',
  'P7',
  'T8',
  'F7',
  'F8',
  'T7',
  'P8',
  'AF4',
  'F4',
  'AF3',
  'O2',
  'O1',
  'FC5',
  'X',
  'Y'
]

signals = { channel: numpy.array([]) for channel in channels }

# Setup connection to Emotiv EPOC headset.
headset = emotiv.Emotiv()
gevent.spawn(headset.setup)
gevent.sleep(1)

# Build the GUI.
plot.ion()
main_win = plot.figure(1)
subplots = {}
i = 1
for channel in channels:
  subplots[channel] = main_win.add_subplot(len(channels), 1, i)
  i += 1
lines = { channel: subplots[channel].plot(numpy.array([]))[0] for channel in channels }

displayed_points = 100
try:
  while(True):
    packet = headset.dequeue()
    buf_size = len(signals['X']) + 1
    t_begin = buf_size - 100
    t_end = buf_size
    # Build an array containing the timestamp dimension (sample rate of the emotiv epoc is 128Hz).
    # Note: This is incredibly inefficient.
    # t = numpy.array(range(t_begin, t_end)) / 128.0
    # t = numpy.array(range(t_end)) / 128.0
    t = numpy.linspace(0, t_end / 128.0, t_end)

    print("Displaying t window: [{0}, {1})".format(t_begin, t_end))

    for channel in channels:
      current_value = packet.sensors[channel]

      # Store this packet's value.
      signals[channel] = numpy.append(signals[channel], current_value['value'])

      # Display the last ${displayed_points} points.
      lines[channel].set_data(t, signals[channel])
      subplots[channel].relim()
      subplots[channel].set_xlim(t_begin / 128.0, t_end / 128.0)
      subplots[channel].autoscale_view(
          tight = True,
          scalex = False,
          scaley = True)

    # Update the figure.
    main_win.canvas.draw()

    # Print diagnostic information.
    if len(signals['X']) % 1000 == 0:
      print("Current buffer size: {0}".format(len(signals['X'])))

    gevent.sleep(0)
except KeyboardInterrupt:
  print("Closing connection to headset...")
  headset.close()
finally:
  print("Closing connection to headset...")
  headset.close()
