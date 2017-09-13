class LibraryLoadWizard(models.Model):
    #...
    _name='library.load.wizard'
    @api.multi
    def record_loads(self):
        for wizard in self:
            books = wizard.book_ids
            load = self.env['library.book.load']
            for book in wizard.book_ids:
                values = self._prepare_load(book)
                load.create(values)

    @api.multi
    def _prepare_load(self, book):
        return {'member_id': self.member_id.id,
                'book_id': book.id,
                }
