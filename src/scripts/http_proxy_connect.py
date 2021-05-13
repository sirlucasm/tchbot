'''
Establish a socket connection through an HTTP proxy.
Author: Fredrik Østrem <frx.apps@gmail.com>
License:
  Copyright 2013 Fredrik Østrem
  Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
  documentation files (the "Software"), to deal in the Software without restriction, including without
  limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the
  Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
  The above copyright notice and this permission notice shall be included in all copies or substantial portions
  of the Software.
  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED
  TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
  THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF
  CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
  DEALINGS IN THE SOFTWARE.
'''

import socket
from base64 import b64encode

def http_proxy_connect(address, proxy = None, auth = None, headers = {}):
  """
  Establish a socket connection through an HTTP proxy.
  
  Arguments:
    address (required)     = The address of the target
    proxy (def: None)      = The address of the proxy server
    auth (def: None)       = A tuple of the username and password used for authentication
    headers (def: {})      = A set of headers that will be sent to the proxy
  
  Returns:
    A 3-tuple of the format:
      (socket, status_code, headers)
    Where `socket' is the socket object, `status_code` is the HTTP status code that the server
     returned and `headers` is a dict of headers that the server returned.
  """
  
  def valid_address(addr):
    """ Verify that an IP/port tuple is valid """
    return isinstance(addr, (list, tuple)) and len(addr) == 2 and isinstance(addr[0], str) and isinstance(addr[1], int)
  
  if not valid_address(address):
    raise ValueError('Invalid target address')
  
  if proxy == None:
    s = socket.socket()
    s.connect(address)
    return s, 0, {}
  
  if not valid_address(proxy):
    raise ValueError('Invalid proxy address')
  
  headers = {
    'host': address[0]
  }
  
  if auth != None:
    if isinstance(auth, str):
      headers['proxy-authorization'] = auth
    elif auth and isinstance(auth, (tuple, list)) and len(auth) == 2:
      headers['proxy-authorization'] = 'Basic ' + b64encode('%s:%s' % auth)
    else:
      raise ValueError('Invalid authentication specification')
  
  s = socket.socket()
  s.connect(proxy)
  fp = s.makefile('r+')
  
  fp.write('CONNECT %s:%d HTTP/1.0\r\n' % address)
  fp.write('\r\n'.join('%s: %s' % (k, v) for (k, v) in headers.items()) + '\r\n\r\n')
  fp.flush()
  
  statusline = fp.readline().rstrip('\r\n')
  
  if statusline.count(' ') < 2:
    fp.close()
    s.close()
    raise IOError('Bad response')
  version, status, statusmsg = statusline.split(' ', 2)
  if not version in ('HTTP/1.0', 'HTTP/1.1'):
    fp.close()
    s.close()
    raise IOError('Unsupported HTTP version')
  try:
    status = int(status)
  except ValueError:
    fp.close()
    s.close()
    raise IOError('Bad response')
  
  response_headers = {}
  
  while True:
    tl = ''
    l = fp.readline().rstrip('\r\n')
    if l == '':
      break
    if not ':' in l:
      continue
    k, v = l.split(':', 1)
    response_headers[k.strip().lower()] = v.strip()
  
  fp.close()
  return (s, status, response_headers)