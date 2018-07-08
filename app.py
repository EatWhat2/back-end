# !/usr/bin/env python3
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado, sys, argparse

sys.path.append('./src/')

from urls import url_patterns
from settings import settings

# Define the arguments for the app.
parser = argparse.ArgumentParser(description="app option")
parser.add_argument('-p', type=int)

# Get the arguments.
args = parser.parse_args()
if not args.p:
  args.p = 8888

class eatwhat(tornado.web.Application):
  def __init__(self):
    tornado.web.Application.__init__(self, url_patterns, **settings, debug=True)


if __name__ == "__main__":
  # Create http server.
  app = eatwhat()
  http_server = tornado.httpserver.HTTPServer(app, max_buffer_size=1024 * 1024 * 1024)

  # listen on port.
  print("tornado listens on", args.p)
  http_server.listen(args.p)

  # Start looping.
  tornado.ioloop.IOLoop.instance().start()
