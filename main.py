#!/usr/bin/env python
#
# Project: Video Streaming with Flask
# Author: Log0 <im [dot] ckieric [at] gmail [dot] com>
# Date: 2014/12/21
# Website: http://www.chioka.in/
# Description:
# Modified to support streaming out with webcams, and not just raw JPEGs.
# Most of the code credits to Miguel Grinberg, except that I made a small tweak. Thanks!
# Credits: http://blog.miguelgrinberg.com/post/video-streaming-with-flask
#
# Usage:
# 1. Install Python dependencies: cv2, flask. (wish that pip install works like a charm)
# 2. Run "python main.py".
# 3. Navigate the browser to the local webpage.
from flask import Flask, render_template, Response
from camera import VideoCamera
import argparse
import sys

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

def parse_arguments(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument('--card', type=str, 
        help='Network Card', default='eth0')
    parser.add_argument('--debug', 
        help='Debug', action='store_true')
    return parser.parse_args(argv)

def get_ip(net_card):
    import netifaces as ni
    ni.ifaddresses(net_card)
    ip = ni.ifaddresses(net_card)[2][0]['addr']
    print ip  # should print "192.168.0.18" 
    return ip 

if __name__ == '__main__':
    args = parse_arguments(sys.argv[1:])
    host = get_ip(args.card)

    app.run(host=host, debug=args.debug)