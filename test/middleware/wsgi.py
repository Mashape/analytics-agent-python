import time
import ujson

from unittest import TestCase
from werkzeug.test import Client

from mashape_analytics.storage import Storage
from mashape_analytics.middleware import WsgiMiddleware
from test.helpers import collector

store = Storage()

def create_app():
  def app(env, start_response):
    start_response('200 OK CUSTOM', [('Content-Type','text/plain')])
    return ['Hello World']

  return app

##
# Test WSGI middleware
##
class WsgiMiddewareTest(TestCase):

  def setUp(self):
    store.reset()
    self.app = WsgiMiddleware(create_app(), 'SERVICE-TOKEN', 'ENVIRONMENT', host='localhost', port=10000)

  def tearDown(self):
    pass

  @classmethod
  def tearDownClass(cls):
    app = WsgiMiddleware(create_app(), 'SERVICE-TOKEN', 'ENVIRONMENT', host='localhost', port=10000)
    app.analytics.put_queue('exit')
    print 'wait 2 seconds for teardown'
    time.sleep(2)

  def test_should_get(self):
    # TODO check timeout
    status = '200 OK' # HTTP Status
    headers = [('Content-type', 'application/json')] # HTTP Headers
    with collector(10000, status, headers, 'Hello') as requests:
      client = Client(self.app)
      data, status, headers = client.open()
      data = b''.join(data)

      self.assertIn('Hello', data)

      request = requests.get()
      alf = ujson.loads(request.get('body'))
      print alf

  def test_should_get_multiple(self):
    # TODO check timeout
    status = '200 OK' # HTTP Status
    headers = [('Content-type', 'application/json')] # HTTP Headers
    with collector(10000, status, headers, 'Hello World') as requests:
      client = Client(self.app)
      data, status, headers = client.open()
      data = b''.join(data)

      self.assertIn('Hello', data)

      request = requests.get()
      alf = ujson.loads(request.get('body'))
      print alf

      # second
      data, status, headers = client.open()
      data = b''.join(data)

      self.assertIn('Hello', data)

      request = requests.get()
      alf = ujson.loads(request.get('body'))
      print alf
  #
  #     # self.assertEqual(version, 'alf_1.0.0')
  #     #
  #     # self.assertEqual(alf['serviceToken'], 'SERVICE-TOKEN')
  #     # self.assertEqual(alf['har']['log']['creator']['name'], 'mashape-analytics-agent-python')
  #     # self.assertEqual(alf['har']['log']['entries'][0]['request']['method'], 'GET')
  #     # self.assertEqual(alf['har']['log']['entries'][0]['request']['url'], 'http://localhost/')
  #     # self.assertEqual(alf['har']['log']['entries'][0]['response']['status'], 200)
  #     # self.assertEqual(alf['har']['log']['entries'][0]['response']['statusText'], 'OK CUSTOM')
  #     # self.assertEqual(alf['har']['log']['entries'][0]['response']['content']['mimeType'], 'text/plain')
  #     # self.assertEqual(alf['har']['log']['entries'][0]['response']['content']['size'], 11)
  #     # self.assertTrue(alf['har']['log']['entries'][0]['timings']['wait'] >= 10)
