from handlers import application
import settings as  app_config
from tornado import httpserver, ioloop, options

def main():
    if not app_config.settings['debug']:
        options.options.log_file_prefix = app_config.settings['logfile_path']
    options.parse_command_line()
    http_server = httpserver.HTTPServer(application, xheaders=True)
    http_server.bind(app_config.settings['port'])
    http_server.start()

    ioloop.IOLoop.instance().start()

if __name__ == "__main__":
    main()
