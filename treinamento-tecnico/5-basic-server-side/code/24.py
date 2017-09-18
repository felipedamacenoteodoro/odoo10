class LibraryMember(models.Model):
    _inherit = 'library.member'
    load_duration = fields.Integer('Load duration',
                                   default=15,
                                   required=True,
                                   )
