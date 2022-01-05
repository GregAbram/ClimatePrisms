import web, pdb

from api import API
api = API()

urls = (
    '/api.*', 'api_wrapper'
)

class api_wrapper:
    def GET(self):
        web.header('Access-Control-Allow-Origin', '*')
        web.header('Access-Control-Allow-Credentials', 'true')
        web.header('Content-Type', 'application/json')
        op = web.url()[1:].split('/')[1]
        return api.run(op, web.input())

if __name__ == "__main__":
    app = web.application(urls, globals(), autoreload=False)
    app.run()
