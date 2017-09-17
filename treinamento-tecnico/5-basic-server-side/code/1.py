from odoo import models, fields, api
class LibraryBook(models.Model):
    # [...]
    state = fields.Selection([
        ('draft', 'Unavailable'),
        ('available', 'Available'),
        ('borrowed', 'Borrowed'),
        ('lost', 'Lost')],
        default='draft',
        string='State',
    )
