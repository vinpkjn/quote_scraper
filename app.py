#!usr/bin/python

import web
import json
from scrap_cws import main

urls = (
    '/users', 'list_users',
    '/toc', 'table_of_contents',
    '/(.*)', 'index')

app = web.application(urls, globals())


class index:
    def GET(self, name):
        return "Hello, World!!!"


class list_users:
    def GET(self):
        return "vinu"


class table_of_contents:
    def GET(self):
        result = main()
        # return result
        return json.dumps(result)


if __name__ == "__main__":
    app.run()
