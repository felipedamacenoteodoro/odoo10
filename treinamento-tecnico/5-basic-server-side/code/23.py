class LibraryBookLoan(models.Model):
	_inherit = 'library.book.loan'
	expected_return_date = fields.Date('Due for', required=True)
