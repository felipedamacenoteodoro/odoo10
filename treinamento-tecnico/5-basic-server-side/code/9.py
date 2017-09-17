class ResPartner(models.Model):
    #[...]

    name = fields.Char('Name', required=True)
    email = fields.Char('Email')
    date = fields.Date('Date')
    is_company = fields.Boolean('Is a company')
    parent_id = fields.Many2one(
        comodel_name='res.partner',
        string='Related Company',
    )
    child_ids = fields.One2many(
        comodel_name='res.partner',
        inverse_name='parent_id',
        string='Contacts',
    )
