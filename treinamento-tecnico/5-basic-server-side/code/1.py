from openerp import models, fields, api
class LibraryBook(models.Model):
	# [...]
	state = fields.Selection([('draft', 'Unavailable'),
		('available', 'Available'),
		('borrowed', 'Borrowed'),
		('lost', 'Lost')],
		'State')
