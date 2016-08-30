@api.model
def add_contacts(self, partner, contacts):
	partner.ensure_one()
	if contacts:
		today = fields.Date.context_today()
		partner.update(
			{'date': today,
			'child_ids': partner_child_ids | contacts}
		)
