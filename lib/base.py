#coding:utf-8

import time, json
import types
import tornado.web
from lib.session import session
from lib.template import render
from handlers import appConfig

class BaseHandler(tornado.web.RequestHandler):
    url_pattern = None
    _start_time = time.time()
    _finish_time = None

    def write_error(self, status_code, **kwargs):
        #import traceback
        if self.settings.get("debug") and "exc_info" in kwargs:
            exc_info = kwargs["exc_info"]
            #trace_info = ''.join(["%s<br/>" % line for line in traceback.format_exception(*exc_info)])
            #request_info = ''.join(["<strong>%s</strong>: %s<br/>" % (k, self.request.__dict__[k]) for k in self.request.__dict__.keys()])
            error = exc_info[1]

            self.set_header('Content-Type', 'text/html')
            self.finish("""<html>
                             <title>%s</title>
                             <body>
                                <h2>Error</h2>
                                <p>%s</p>
                             </body>
                           </html>""" % (error, error))



    def request_time(self):
        """Returns the amount of time it took for this request to execute."""
        if self._finish_time is None:
            return time.time() - self._start_time
        else:
            return self._finish_time - self._start_time

    @property
    def db(self):
        return self.application.db

    @session
    def get_current_user(self):
        return None

    def json_write(self, obj):
        self.set_header('Content-Type', 'application/json')
        self.write(json.dumps(obj))

    def render_self(self, **kwargs):
        super(BaseHandler, self).render(self.templname,
                                 **kwargs)

    def get_error_html(self, status_code, **kwargs):
        code = str(status_code)
        try:
            return self.render_string('errors/'+code+'.html', **kwargs)
        except:
            self.write('Sorry, happen an error.')

    def render_string(self, template_name, **context):
        '''Template render by Jinja2.'''
        default_context = {
            'xsrf': self.xsrf_form_html,
            'request': self.request,
            'settings': self.settings,
            'me': self.current_user,
            'static': self.static_url,
            'handler': self,
            'config': appConfig,
        }
        context.update(default_context)
        context.update(self.ui)     # Enabled tornado UI methods.
        return render(
            path=self.settings['template_path'],
            filename=template_name,
            auto_reload=self.settings['debug'],
            **context)

    def render(self, template_name, **kwargs):
        self.finish(self.render_string(template_name, **kwargs))


class Application(tornado.web.Application):
    """
    Tornado Application
    """
    def load_module(self, module, **options):
        """
        load RequestHandler moudle
        """
        assert type(module) is types.ModuleType
        host_pattern = options.get('host_pattern', '.*$')

        #process load RequestHandler & route rules
        cls_valid = lambda cls: type(cls) is types.TypeType \
                    and issubclass(cls, BaseHandler)
        url_valid = lambda cls: hasattr(cls, 'url_pattern') \
                    and cls.url_pattern #是否含有URL route pattern
        mod_attrs = (getattr(module, i) for i in dir(module) \
                    if not i.startswith('_'))
        valid_handlers = ((i.url_pattern, i) for i in mod_attrs if cls_valid(i) and url_valid(i))

        #processed and call add_handlers in superclass to load the valid_handlers
        self.add_handlers(host_pattern, valid_handlers)

    def _get_host_handlers(self, request):
        """docstring for _get_host_handlers"""
        host = request.host.lower().split(':')[0]
        handlers = (i for p, h in self.handlers for i in h if p.match(host))

        if not handlers and 'X-Real-Ip' not in request.headers:
            handlers = (i for p, h in self.handlers for i in h if p.match(host))

        return handlers

def route(url_pattern):
    """
    路由器装饰器
    """
    def handler_wapper(cls):
        assert(issubclass(cls, BaseHandler))
        cls.url_pattern = url_pattern
        return cls
    return handler_wapper
