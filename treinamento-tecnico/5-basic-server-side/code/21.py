@api.model
def partners_with_email(self, partners):
    def predicate(partner):
        if partner.email:
            return True
        return False

    return partners.filter(predicate)
