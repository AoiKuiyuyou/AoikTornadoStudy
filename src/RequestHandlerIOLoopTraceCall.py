# coding: utf-8
from __future__ import absolute_import

# Standard imports
import sys
import logging

# External imports
import aoiktracecall.config
import aoiktracecall.logging
import aoiktracecall.trace


# Traced modules should be imported after `trace_calls_in_specs` is called.


# Set configs
aoiktracecall.config.set_configs({
    # Whether use wrapper class.
    #
    # Wrapper class is more adaptive to various types of callables but will
    # break if the code that was using the original function requires a real
    # function, instead of a callable. Known cases include PyQt slot functions.
    #
    'WRAP_USING_WRAPPER_CLASS': True,

    # Whether wrap base class attributes in a subclass.
    #
    # If enabled, wrapper attributes will be added to a subclass even if the
    # wrapped original attributes are defined in a base class.
    #
    # This helps in the case that base class attributes are implemented in C
    # extensions thus can not be traced directly.
    #
    'WRAP_BASE_CLASS_ATTRIBUTES': True,

    # Indentation unit text
    'INDENT_UNIT_TEXT': ' ' * 8,

    # Whether highlight title shows `self` argument's class instead of called
    # function's defining class.
    #
    # This helps reveal the real type of the `self` argument on which the
    # function is called.
    #
    'HIGHLIGHT_TITLE_SHOW_SELF_CLASS': True,

    # Highlight title line character count max
    'HIGHLIGHT_TITLE_LINE_CHAR_COUNT_MAX': 265,

    # Whether show function's file path and line number in pre-call hook
    'SHOW_FUNC_FILE_PATH_LINENO_PRE_CALL': True,

    # Whether show function's file path and line number in post-call hook
    'SHOW_FUNC_FILE_PATH_LINENO_POST_CALL': False,

    # Whether wrapper function should debug info dict's URIs
    'WRAPPER_FUNC_DEBUG_INFO_DICT_URIS': False,

    # Whether printing handler should debug arguments inspect info
    'PRINTING_HANDLER_DEBUG_ARGS_INSPECT_INFO': False,

    # Whether printing handler should debug info dict.
    #
    # Notice info dict contains called function's arguments and printing these
    # arguments may cause errors.
    #
    'PRINTING_HANDLER_DEBUG_INFO_DICT': False,

    # Whether printing handler should debug info dict, excluding arguments.
    #
    # Use this if `PRINTING_HANDLER_DEBUG_INFO_DICT` causes errors.
    #
    'PRINTING_HANDLER_DEBUG_INFO_DICT_SAFE': False,
})


# Add debug logger handler
aoiktracecall.logging.get_debug_logger().addHandler(logging.NullHandler())

# Add info logger handler
aoiktracecall.logging.get_info_logger().addHandler(
    logging.StreamHandler(sys.stdout)
)

# Add error logger handler
aoiktracecall.logging.get_error_logger().addHandler(
    logging.StreamHandler(sys.stderr)
)


# Constant for `highlight`
HL = 'highlight'

# Create trace specs.
#
# The order of the specs determines the matching precedence, with one exception
# that URI patterns consisting of only alphanumerics, underscores, and dots are
# considered as exact URI matching, and will have higher precedence over all
# regular expression matchings. The rationale is that a spec with exact URI
# matching is more specific therefore should not be shadowed by any spec with
# regular expression matching that has appeared early.
#
trace_specs = [
    # ----- aoiktracecall -----
    ('aoiktracecall([.].+)?', False),

    # ----- * -----
    # Tracing `__setattr__` will reveal instances' attribute assignments.
    # Notice Python 2 old-style classes have no `__setattr__` attribute.
    ('.+[.]__setattr__', True),

    # Not trace most of double-underscore functions.
    # Tracing double-underscore functions is likely to break code, e.g. tracing
    # `__str__` or `__repr__` may cause infinite recursion.
    ('.+[.]__(?!init|call)[^.]+__', False),

    # ----- socket._socketobject (Python 2), socket.socket (Python 3) -----
    # Notice in Python 2, class `socket._socketobject`'s instance methods
    # - recv
    # - recvfrom
    # - recv_into
    # - recvfrom_into
    # - send
    # - sendto
    # are dynamically generated in `_socketobject.__init__`. The approach of
    # wrapping class attributes is unable to trace these methods.

    ('socket[.](_socketobject|socket)[.]__init__', HL),

    ('socket[.](_socketobject|socket)[.]bind', HL),

    ('socket[.](_socketobject|socket)[.]listen', HL),

    ('socket[.](_socketobject|socket)[.]connect', HL),

    ('socket[.](_socketobject|socket)[.]accept', HL),

    ('socket[.](_socketobject|socket)[.]setsockopt', HL),

    ('socket[.](_socketobject|socket)[.]setblocking', HL),

    ('socket[.](_socketobject|socket)[.]makefile', HL),

    ('socket[.](_socketobject|socket)[.]recv.*', HL),

    ('socket[.](_socketobject|socket)[.]send.*', HL),

    ('socket[.](_socketobject|socket)[.]shutdown', HL),

    ('socket[.](_socketobject|socket)[.]close', HL),

    # ----- socket._fileobject (Python 2), socket.SocketIO (Python 3) -----
    ('socket[.](SocketIO|_fileobject)[.]__init__', HL),

    ('socket[.](SocketIO|_fileobject)[.]read.*', HL),

    ('socket[.](SocketIO|_fileobject)[.]write.*', HL),

    ('socket[.](SocketIO|_fileobject)[.]flush', HL),

    ('socket[.](SocketIO|_fileobject)[.]close', HL),

    ('socket[.](SocketIO|_fileobject)[.].+', True),

    # ----- socket -----
    ('socket._intenum_converter', False),

    ('socket[.].+[.]_decref_socketios', False),

    ('socket[.].+[.]fileno', False),

    # Ignore to avoid error in `__repr__` in Python 3
    ('socket[.].+[.]getpeername', False),

    # Ignore to avoid error in `__repr__` in Python 3
    ('socket[.].+[.]getsockname', False),

    ('socket[.].+[.]gettimeout', False),

    ('socket([.].+)?', True),

    # ----- select (Python 2) -----
    ('select.select', HL),

    ('select([.].+)?', True),

    # ----- selectors (Python 3) -----
    ('selectors.SelectSelector.__init__', HL),

    ('selectors.SelectSelector.register', HL),

    ('selectors.SelectSelector.select', HL),

    ('selectors([.].+)?', True),

    # ----- SocketServer (Python 2), socketserver (Python 3) -----
    ('SocketServer._eintr_retry', False),

    ('(socketserver|SocketServer)[.]BaseServer[.]__init__', HL),

    ('(socketserver|SocketServer)[.]TCPServer[.]__init__', HL),

    ('(socketserver|SocketServer)[.]ThreadingMixIn[.]process_request', HL),

    (
        '(socketserver|SocketServer)[.]ThreadingMixIn[.]'
        'process_request_thread', HL
    ),

    # Ignore to avoid error:
    # ```
    # 'WSGIServer' object has no attribute '_BaseServer__is_shut_down'
    # ```
    ('(socketserver|SocketServer)[.]ThreadingMixIn[.].+', False),

    ('(socketserver|SocketServer)[.]BaseRequestHandler[.]__init__', HL),

    ('(socketserver|SocketServer)[.].+[.]service_actions', False),

    ('.+[.]server_bind', HL),

    ('.+[.]server_activate', HL),

    ('.+[.]serve_forever', HL),

    ('.+[.]_handle_request_noblock', HL),

    ('.+[.]get_request', HL),

    ('.+[.]verify_request', HL),

    ('.+[.]process_request', HL),

    ('.+[.]process_request_thread', HL),

    ('.+[.]finish_request', HL),

    ('.+[.]setup', HL),

    ('.+[.]handle', HL),

    ('.+[.]finish', HL),

    ('.+[.]shutdown_request', HL),

    ('.+[.]close_request', HL),

    ('.+[.]fileno', False),

    ('(socketserver|SocketServer)([.].+)?', True),

    # ----- mimetools -----
    # `mimetools` is used for parsing HTTP headers in Python 2.

    ('mimetools([.].+)?', True),

    # ----- email -----
    # `email` is used for parsing HTTP headers in Python 3.

    ('email([.].+)?', True),

    # ----- BaseHTTPServer (Python 2), http.server (Python 3) -----
    ('.+[.]handle_one_request', HL),

    ('.+[.]parse_request', HL, 'hide_below'),

    ('.+[.]send_response', HL),

    ('.+[.]send_header', HL),

    ('.+[.]end_headers', HL),

    # ----- BaseHTTPServer (Python 2) -----
    ('BaseHTTPServer([.].+)?', True),

    # ----- http (Python 3) -----
    ('http([.].+)?', True),

    # ----- wsgiref -----
    ('wsgiref.handlers.BaseHandler.write', HL),

    ('wsgiref.handlers.BaseHandler.close', HL),

    ('wsgiref.handlers.SimpleHandler.__init__', HL),

    ('wsgiref.handlers.SimpleHandler._write', HL),

    ('wsgiref.handlers.SimpleHandler._flush', HL),

    ('wsgiref.simple_server.WSGIServer.__init__', HL),

    ('wsgiref.simple_server.ServerHandler.__init__', HL),

    ('wsgiref.simple_server.ServerHandler.close', HL),

    ('.+[.]make_server', HL),

    ('.+[.]setup_environ', HL, 'hide_below'),

    ('.+[.]set_app', HL),

    ('.+[.]get_environ', HL, 'hide_below'),

    ('.+[.]get_app', HL),

    ('.+[.]run', HL),

    ('.+[.]start_response', HL),

    ('.+[.]finish_response', HL),

    ('.+[.]send_headers', HL),

    ('.+[.]cleanup_headers', HL),

    ('.+[.]send_preamble', HL),

    ('.+[.]finish_content', HL),

    ('.+[.]finish', HL),

    ('wsgiref([.].+)?', True),

    # ----- tornado -----
    ('tornado.concurrent.Future.__init__', HL),

    ('tornado.concurrent.Future.add_done_callback', HL),

    ('tornado.concurrent.Future.result', HL),

    ('tornado.concurrent.Future.set_result', HL),

    ('tornado.gen.Runner.__init__', HL),

    ('tornado.gen.Runner.handle_yield', HL),

    ('tornado.gen.Runner.run', HL),

    ('tornado.gen.with_timeout', HL),

    ('tornado.http1connection.HTTP1Connection.__init__', HL),

    ('tornado.http1connection.HTTP1Connection._clear_callbacks', HL),

    ('tornado.http1connection.HTTP1Connection._finish_request', HL),

    ('tornado.http1connection.HTTP1Connection._finish_request', HL),

    ('tornado.http1connection.HTTP1Connection._format_chunk', HL),

    ('tornado.http1connection.HTTP1Connection._on_write_complete', HL),

    ('tornado.http1connection.HTTP1Connection._parse_headers', HL),

    ('tornado.http1connection.HTTP1Connection._read_body', HL),

    ('tornado.http1connection.HTTP1Connection._read_fixed_body', HL),

    ('tornado.http1connection.HTTP1Connection._read_message', HL),

    ('tornado.http1connection.HTTP1Connection.read_response', HL),

    ('tornado.http1connection.HTTP1Connection.set_close_callback', HL),

    ('tornado.http1connection.HTTP1Connection.write_headers', HL),

    ('tornado.http1connection.HTTP1ServerConnection.__init__', HL),

    ('tornado.http1connection.HTTP1ServerConnection._server_request_loop', HL),

    ('tornado.http1connection.HTTP1ServerConnection.start_serving', HL),

    ('tornado.http1connection._ExceptionLoggingContext.__init__', HL),

    ('tornado.httpserver.HTTPServer.__init__', HL),

    ('tornado.httpserver.HTTPServer.handle_stream', HL),

    ('tornado.httpserver.HTTPServer.initialize', HL),

    ('tornado.httpserver.HTTPServer.start_request', HL),

    ('tornado.httpserver._HTTPRequestContext.__init__', HL),

    ('tornado.httpserver._ServerRequestAdapter.__init__', HL),

    ('tornado.httpserver._ServerRequestAdapter.data_received', HL),

    ('tornado.httpserver._ServerRequestAdapter.headers_received', HL),

    ('tornado.httputil.HTTPHeaders.get_all', HL),

    ('tornado.httputil.HTTPServerRequest.__init__', HL),

    # Ignore to avoid error
    ('tornado.httputil.HTTPServerRequest.__setattr__', False),

    ('tornado.httputil.HTTPServerRequest._parse_body', HL),

    ('tornado.httputil.parse_body_arguments', HL),

    ('tornado.httputil.parse_request_start_line', HL),

    ('tornado.ioloop.IOLoop._run_callback', HL),

    ('tornado.ioloop.IOLoop.add_future', HL),

    ('tornado.ioloop.IOLoop.initialize', HL),

    ('tornado.ioloop.IOLoop.instance', HL),

    ('tornado.ioloop.PollIOLoop.add_handler', HL),

    ('tornado.ioloop.PollIOLoop.initialize', HL),

    ('tornado.ioloop.PollIOLoop.start', HL),

    ('tornado.iostream.BaseIOStream.__init__', HL),

    ('tornado.iostream.BaseIOStream._add_io_state', HL),

    ('tornado.iostream.BaseIOStream._consume', HL),

    ('tornado.iostream.BaseIOStream._find_read_pos', HL),

    ('tornado.iostream.BaseIOStream._find_read_pos', HL),

    ('tornado.iostream.BaseIOStream._handle_write', HL),

    ('tornado.iostream.BaseIOStream._maybe_add_error_listener', HL),

    ('tornado.iostream.BaseIOStream._maybe_add_error_listener', HL),

    ('tornado.iostream.BaseIOStream._maybe_run_close_callback', HL),

    ('tornado.iostream.BaseIOStream._read_from_buffer', HL),

    ('tornado.iostream.BaseIOStream._read_to_buffer', HL),

    ('tornado.iostream.BaseIOStream._read_to_buffer_loop', HL),

    ('tornado.iostream.BaseIOStream._run_read_callback', HL),

    ('tornado.iostream.BaseIOStream._run_streaming_callback', HL),

    ('tornado.iostream.BaseIOStream._run_streaming_callback', HL),

    ('tornado.iostream.BaseIOStream._set_read_callback', HL),

    ('tornado.iostream.BaseIOStream._try_inline_read', HL),

    ('tornado.iostream.BaseIOStream.read_bytes', HL),

    ('tornado.iostream.BaseIOStream.read_until_regex', HL),

    ('tornado.iostream.BaseIOStream.set_close_callback', HL),

    ('tornado.iostream.BaseIOStream.write', HL),

    ('tornado.iostream.IOStream.__init__', HL),

    ('tornado.iostream.IOStream.read_from_fd', HL),

    ('tornado.iostream.IOStream.set_nodelay', HL),

    ('tornado.iostream.IOStream.write_to_fd', HL),

    ('tornado.iostream._merge_prefix', HL),

    ('tornado.netutil.add_accept_handler', HL),

    ('tornado.netutil.bind_sockets', HL),

    ('tornado.platform.common.Waker.__init__', HL),

    ('tornado.platform.select.SelectIOLoop.initialize', HL),

    ('tornado.platform.select._Select.__init__', HL),

    ('tornado.platform.select._Select.poll', HL),

    ('tornado.platform.select._Select.register', HL),

    ('tornado.tcpserver.TCPServer.__init__', HL),

    ('tornado.tcpserver.TCPServer._handle_connection', HL),

    ('tornado.tcpserver.TCPServer.add_sockets', HL),

    ('tornado.tcpserver.TCPServer.listen', HL),

    ('tornado.util.Configurable.__new__', HL),

    ('tornado.web.Application.__init__', HL),

    ('tornado.web.Application.add_handlers', HL),

    ('tornado.web.Application.listen', HL),

    ('tornado.web.Application.start_request', HL),

    ('tornado.web.RequestHandler.__init__', HL),

    ('tornado.web.RequestHandler._execute', HL),

    ('tornado.web.RequestHandler.clear', HL),

    ('tornado.web.RequestHandler.flush', HL),

    ('tornado.web.RequestHandler.initialize', HL),

    ('tornado.web.RequestHandler.prepare', HL),

    ('tornado.web.RequestHandler.set_header', HL),

    ('tornado.web.RequestHandler.write', HL),

    # Ignore to avoid error
    ('tornado.web.URLSpec.__setattr__', False),

    ('tornado.web._RequestDispatcher.__init__', HL),

    ('tornado.web._RequestDispatcher._find_handler', HL),

    ('tornado.web._RequestDispatcher.data_received', HL),

    ('tornado.web._RequestDispatcher.execute', HL),

    ('tornado.web._RequestDispatcher.headers_received', HL),

    ('tornado.web._RequestDispatcher.set_request', HL),

    ('tornado([.].+)?', True),

    # ----- __main__ -----
    ('__main__.main', HL),

    ('__main__.CustomRequestHandler', HL),

    ('__main__.CustomRequestHandler.post', HL),

    ('__main__([.].+)?', True),
]


# Trace calls according to trace specs.
#
# This function will hook the module importing system in order to intercept and
# process newly imported modules. Callables in these modules which are matched
# by one of the trace specs will be wrapped to enable tracing.
#
# Already imported modules will be processed as well. But their callables may
# have been referenced elsewhere already, making the tracing incomplete. This
# explains why import hook is needed and why modules must be imported after
# `trace_calls_in_specs` is called.
#
aoiktracecall.trace.trace_calls_in_specs(specs=trace_specs)


# Import modules after `trace_calls_in_specs` is called
import tornado.ioloop
import tornado.web


class CustomRequestHandler(tornado.web.RequestHandler):
    """
    This request handler echoes request body in response body.
    """

    def post(self):
        # Get request body
        request_body = self.request.body

        # Write response body
        self.write(request_body)


def main():
    # URL-to-handler mappings
    url_to_handler_mappings = [
        (r'/.*', CustomRequestHandler),
    ]

    # Create Tornado application
    tornado_app = tornado.web.Application(
        url_to_handler_mappings,
        debug=False,
    )

    # Create event loop
    io_loop = tornado.ioloop.IOLoop.current()

    # Start listening
    tornado_app.listen(8000, address='127.0.0.1')

    try:
        # Run event loop
        io_loop.start()

    # If have `KeyboardInterrupt`
    except KeyboardInterrupt:
        # Stop gracefully
        pass


# Trace calls in this module.
#
# Calling this function is needed because at the point `trace_calls_in_specs`
# is called, this module is being initialized, therefore callables defined
# after the call point are not accessible to `trace_calls_in_specs`.
#
aoiktracecall.trace.trace_calls_in_this_module()


# If is run as main module
if __name__ == '__main__':
    # Call main function
    exit(main())
