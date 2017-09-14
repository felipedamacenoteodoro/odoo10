class ResPartner(models.Model):
        #...

	_order = 'name'

	authored_book_ids = fields.Many2many(
	    comodel_name='library.book',
	    string='Authored Books',
	)
	count_books = fields.Integer(
	    comodel_name='Number of Authored Books',
	    compute='_compute_count_books',
	)
