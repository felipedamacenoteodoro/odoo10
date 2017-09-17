from odoo import models, fields, api

class LibraryBookLoad(models.Model):
    _inherit = 'library.book'
    expected_return_date = fields.Date('Due for', required=True)
