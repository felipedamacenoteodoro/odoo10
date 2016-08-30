# ...
from openerp import api # if not already imported
# class ResPartner(models.Model):
# ...
	@api.depends('authored_book_ids')
		def _compute_count_books(self):
			for r in self:
				r.count_books = len(r.authored_book_ids)
