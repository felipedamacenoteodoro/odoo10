class ResPartner(models.Model):
	_inherit = 'res.partner'
	_order = 'name'
	authored_book_ids = fields.Many2many(
		'library.book', string='Authored Books')
	count_books = fields.Integer(
		'Number of Authored Books',
		compute='_compute_count_books'
		)
