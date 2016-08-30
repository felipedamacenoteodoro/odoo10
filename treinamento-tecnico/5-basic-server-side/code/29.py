@api.model
@api.returns('self', lambda rec: rec.id)
def create(self, values):
	if not self.user_has_groups(
	'library.group_library_manager'):
	if 'manager_remarks' in values:
		raise exceptions.UserError(
			'You are not allowed to modify '
			'manager_remarks'
		)
	return super(LibraryBook, self).create(values)
@api.multi
def write(self, values):
	if not self.user_has_groups(
			'library.group_library_manager'):
		if 'manager_remarks' in values:
			raise exceptions.UserError(
				'You are not allowed to modify '
				'manager_remarks'
			)
	return super(LibraryBook, self).write(values)
