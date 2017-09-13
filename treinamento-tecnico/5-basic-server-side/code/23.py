class LibraryBookLoad(models.Model):
    _inherit = 'library.book.load'
    expected_return_date = fields.Date('Due for', required=True)
