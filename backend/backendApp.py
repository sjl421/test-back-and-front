"""Banckend module for the lendingfront test app."""

import logging

from datetime import date
import tornado.escape
import tornado.ioloop
import tornado.web
import tornado.options

from settings import config
from database import Database


class VersionHandler(tornado.web.RequestHandler):
    """Version handler."""

    def get(self):
        """Get the API version."""
        response = {'version': config.API_VERSION}
        self.write(response)


class GetLoanStatus(tornado.web.RequestHandler):
    """This module does the backend logic for the test app."""

    def get(self, business_id):
        """Get method, just a welcome for the user."""
        db = Database()
        if not db.hasBusiness():
            self.set_status(404, reason='There is no business created')
            return None
        if not db.existsBusiness(business_id):
            self.set_status(404, reason='The business doesn\'t exists,' +
                            'please create it first')
            return None

        business = db.getBusiness(business_id)
        amount = business['ammount']
        if amount > config.BASE_AMOUNT:
            loan_status = config.status['DECLINED']
        elif amount == config.BASE_AMOUNT:
            loan_status = config.status['UNDECIDED']
        else:
            loan_status = config.status['APPROVED']

        response = {'business_id': business_id,
                    'loan_status': loan_status,
                    'status_date': date.today().isoformat()}
        self.write(response)


class AddOwnerToBusiness(tornado.web.RequestHandler):
    """Add a new owner to the business."""

    def post(self):
        """Post the new owner."""
        db = Database()
        business_id = self.get_body_argument('business_id')
        if not db.hasBusiness():
            self.set_status(404, reason='There is no business created')
            return None
        if not db.existsBusiness(business_id):
            self.set_status(404, reason='The business doesn\'t exists,' +
                            'please create it first')
            return None

        sec_number = self.get_body_argument('security_number')
        name = self.get_body_argument('name')
        email = self.get_body_argument('email')
        address = self.get_body_argument('address')
        city = self.get_body_argument('city')
        state = self.get_body_argument('state')
        postal_code = self.get_body_argument('postal_code')

        owner = {
            'owner_id': sec_number,
            'name': name,
            'email': email,
            'address': address,
            'city': city,
            'state': state,
            'postal_code': postal_code
        }

        try:
            db.storeOwner(business_id, owner)
            response = {'owner_id': sec_number}
            self.write(response)
        except Exception, e:
            self.set_status(404, reason=str(e))
            return None


class AddBusiness(tornado.web.RequestHandler):
    """Create a new business."""

    def post(self):
        """Post the new business."""
        db = Database()
        tax_id = self.get_body_argument('tax_id')
        name = self.get_body_argument('name')
        address = self.get_body_argument('address')
        city = self.get_body_argument('city')
        state = self.get_body_argument('state')
        postal_code = self.get_body_argument('postal_code')
        ammount = self.get_body_argument('ammount')

        business = {
            'tax_id': tax_id,
            'name': name,
            'address': address,
            'city': city,
            'state': state,
            'postal_code': postal_code,
            'ammount': ammount
        }

        db.storeBusiness(business)
        response = {'tax_id': tax_id}
        self.write(response)


application = tornado.web.Application([
    (r"/api/getloanstatus/([0-9]+)", GetLoanStatus),
    (r"/api/addowner/", AddOwnerToBusiness),
    (r"/api/addbusiness/", AddBusiness),
    (r"/api/version", VersionHandler)
])


if __name__ == "__main__":
    tornado.options.parse_command_line()
    logging.info('Starting the server')
    application.listen(8080)
    tornado.ioloop.IOLoop.instance().start()
