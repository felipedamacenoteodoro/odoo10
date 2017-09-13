@api.model
def is_allowed_transition(self, old_state, new_state):
    allowed= [
        ('draft', 'available'),
        ('available', 'borrowed'),
        ('borrowed', 'available'),
        ('available', 'lost'),
        ('borrowed', 'lost'),
        ('lost', 'available'),
    ]
    return (old_state, new_state) in allowed
