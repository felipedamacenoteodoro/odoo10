class LibraryMember(models.Model):
    _name = 'library.member'
    _inherits = {'res.partner': 'partner_id'}
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        ondelete='cascade',
    )
