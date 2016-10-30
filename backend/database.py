"""In memmory persistence module."""

from settings.config import DATABASE


class Database:
    """In memory database."""

    database = DATABASE['business']

    def hasBusiness(self):
        """Check if there is data stored."""
        return len(self.database) > 0

    def existsBusiness(self, tax_id):
        """Check if the business exists."""
        return tax_id in self.database

    def hasOwners(self, tax_id):
        """Check if the business has owners."""
        return len(self.database[tax_id]['owners']) > 0

    def existsOwner(self, tax_id, ssnumber):
        """Check if the owner exists."""
        if not self.hasOwners(tax_id):
            raise DatabaseException('The business doesn\'t have any owner')
        return ssnumber in self.database[tax_id]['owners']

    def storeBusiness(self, business):
        """Store a new business in the database."""
        if self.existsBusiness(business['tax_id']):
            raise DatabaseException('Business already exists')
        business['owners'] = {}
        self.database[business['tax_id']] = business
        return business['tax_id']

    def getBusiness(self, tax_id):
        """Get a business by the tax_id."""
        if not self.existsBusiness(tax_id):
            raise DatabaseException('Business doesn\'t exists')
        return self.database[tax_id]

    def storeOwner(self, tax_id, owner):
        """Store an owner in the corresponding business."""
        if not self.existsBusiness(tax_id):
            raise DatabaseException('Business doesn\'t exists')
        if self.hasOwners(tax_id) and \
           self.existsOwner(tax_id, owner['ssnumber']):
            raise DatabaseException('The owner already exists')
        self.database[tax_id]['owners'][owner['ssnumber']] = owner
        return owner['ssnumber']

    def getOwner(self, tax_id, ssnumber):
        """Get an owner by the owner id."""
        pass


class DatabaseException(Exception):
    """Database exception."""

    pass
