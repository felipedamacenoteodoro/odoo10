import os
from openerp import models, fields, api

class SomeModel(models.Model):
	data = fields.Text('Data')
	@api.multi
	def save(self, filename):
		path = os.path.join('/opt/exports', filename)
		with open(path, 'w') as fobj:
		for record in self:
			fobj.write(record.data)
			fobj.write('\n')
