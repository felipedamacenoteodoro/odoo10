from odoo import models, fields, api
class LibraryBook(models.Model):
    _inherit = 'library.book'

    def _compute_age(self, partner, contacts):
        super(LibraryBook, self)._compute_age()

        for book in self.filtered('date_release'):
            if book.age_days == 0:
                book.age_days = -1
