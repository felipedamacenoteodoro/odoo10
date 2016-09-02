Web Server Development
======================


Tornando um patch acessivel atraves da web
------------------------------------------

1.	 Crie um arquivo controllers/main.py :

.. code-block:: python


    from openerp import http
    from openerp.http import request


    class Main(http.Controller):
        @http.route('/my_module/books', type='http', auth='none')
        def books(self):
            records = request.env['library.book'].sudo().search([])
            result = '<html><body><table><tr><td>'
            result += '</td></tr><tr><td>'.join(records.mapped('name'))
            result += '</td></tr></table></body></html>'
            return result

        # test this with
        # curl -i -X POST -H "Content-Type: application/json" -d {} $URL
        @http.route('/my_module/books/json', type='json', auth='none')
        def books_json(self):
            records = request.env['library.book'].sudo().search([])
            return records.read(['name'])

.. nextslide::

2. Testando:

.. code-block:: shell

    curl -i -X POST -H "Content-Type: application/json" -d "{}" \
    localhost:8069/my_module/books/json

Utilizando a API
----------------

1. Acesso via XMLRPC

.. code-block:: python

    #!/usr/bin/env python2
    import xmlrpclib

    db = 'odoo9'
    user = 'admin'
    password = 'admin'
    uid = xmlrpclib.ServerProxy('http://localhost:8069/xmlrpc/2/common')\
        .authenticate(db, user, password, {})
    odoo = xmlrpclib.ServerProxy('http://localhost:8069/xmlrpc/2/object')
    installed_modules = odoo.execute_kw(
        db, uid, password, 'ir.module.module', 'search_read',
        [[('state', '=', 'installed')], ['name']], {})
    for module in installed_modules:
        print module['name']

.. nextslide::

2. Acesso via JSONRPC

.. code-block:: python

    #!/usr/bin/env python2
    import json
    import urllib2

    db = 'odoo9'
    user = 'admin'
    password = 'admin'

    request = urllib2.Request(
        'http://localhost:8069/web/session/authenticate',
        json.dumps({
            'jsonrpc': '2.0',
            'params': {
                'db': db,
                'login': user,
                'password': password,
            },
        }),
        {'Content-type': 'application/json'})
    result = urllib2.urlopen(request).read()
    result = json.loads(result)
    session_id = result['result']['session_id']

.. nextslide::

.. code-block:: python

    request = urllib2.Request(
        'http://localhost:8069/web/dataset/call_kw',
        json.dumps({
            'jsonrpc': '2.0',
            'params': {
                'model': 'ir.module.module',
                'method': 'search_read',
                'args': [
                    [('state', '=', 'installed')],
                    ['name'],
                ],
                'kwargs': {},
            },
        }),
        {
            'X-Openerp-Session-Id': session_id,
            'Content-type': 'application/json',
        })
    result = urllib2.urlopen(request).read()
    result = json.loads(result)
    for module in result['result']:
        print module['name']