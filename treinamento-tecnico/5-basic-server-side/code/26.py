from datetime import timedelta
from odoo import models, fields, api
class LibraryLoadWizard(models.TransientModel):
    _inherit = 'library.load.wizard'
    def _prepare_load(self, book):
        values = super(LibraryLoadWizard,self)._prepare_load(book)
        load_duration = self.member_id.load_duration
        today_str = fields.Date.context_today()
        today = fields.Date.from_string(today_str)
        expected = today + timedelta(days=load_duration)
        values.update({
            'expected_return_date':fields.Date.to_string(expected)
        })
        return values
