@api.model
def add_contacts(self, partner, contacts):
	partner.ensure_one()
	if contacts:
		partner.date = fields.Date.context_today()
		partner.child_ids |= contacts
