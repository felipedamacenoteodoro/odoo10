@api.multi
def change_state(self, new_state):
    for book in self:
        if book.is_allowed_transition(book.state, new_state):
            book.state = new_state
        else:
            raise UserError("Transição de estados não permitida!")
