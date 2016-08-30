@api.model
def fields_get(self,
                allfields=None,
                write_access=True,
                attributes=None):
        fields = super(LibraryBook, self).fields_get(
                allfields=allfields,
                write_access=write_access,
                attributes=attributes
        )
        if not self.user_has_groups(
                        'library.group_library_manager'):
                if 'manager_remarks' in fields:
                        fields['manager_remarks']['readonly'] = True

