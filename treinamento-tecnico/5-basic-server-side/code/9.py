class ResPartner(models.Model):
	_name = 'res.partner'
	name = fields.Char('Name', required=True)
	email = fields.Char('Email')
	date = fields.Date('Date')
	is_company = fields.Boolean('Is a company')
	parent_id = fields.Many2one('res.partner', 'Related Company')
	child_ids = fields.One2many('res.partner', 'parent_id',
				'Contacts')
