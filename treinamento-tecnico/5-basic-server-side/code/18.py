	domain = ['|',
		'&',
		('is_company', '=', True),
		('name', 'like', name),
		'&',
		('is_company', '=', False),
		('parent_id.name', 'like', name)
		]
