#!/bin/sh
/usr/bin/mjpg_streamer -i "/usr/lib/mjpg-streamer/input_file.so -e -n camera.jpg -f ${PWD}" -o "/usr/lib/mjpg-streamer/output_http.so -p 8090 -w /usr/share/mjpg-streamer/www"
