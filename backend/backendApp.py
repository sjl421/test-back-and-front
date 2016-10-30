"""Banckend module for the lendingfront test app."""

import logging

from datetime import date
import tornado.escape
import tornado.ioloop
import tornado.web
import tornado.options

from settings import config
from database import Database


class BaseHandler(tornado.web.RequestHandler):
    """Base class with header definition."""

    def set_default_headers(self):
        """Set the default headers."""
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Access-Control-Allow-Methods",
                        "GET,PUT,POST, OPTIONS")
        self.set_header("Access-Control-Allow-Headers",
                        ("Content-Type, Depth, User-Agent, X-File-Size, "
                         "X-Requested-With, X-Requested-By, "
                         "If-Modified-Since, X-File-Name, Cache-Control"))
        self.set_header('Content-Type', 'application/json')

    def get_body_params(self):
        """Return the params in the request body."""
        return tornado.escape.json_decode(self.request.body)


class VersionHandler(BaseHandler):
    """Version handler."""

    def get(self):
        """Get the API version."""
        response = {'version': config.API_VERSION}
        self.write(response)


class GetLoanStatus(BaseHandler):
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
        amount = int(business['amount'])
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


class AddOwnerToBusiness(BaseHandler):
    """Add a new owner to the business."""

    def post(self):
        """Post the new owner."""
        db = Database()
        owner = self.get_body_params()
        business_id = owner['businessId']
        if not db.hasBusiness():
            self.set_status(404, reason='There is no business created')
            return None
        if not db.existsBusiness(business_id):
            self.set_status(404, reason='The business doesn\'t exists,' +
                            'please create it first')
            return None

        try:
            db.storeOwner(business_id, owner)
            response = {'ssnumber': owner['ssnumber']}
            self.write(response)
        except Exception, e:
            logging.critical(str(e))
            self.set_status(404, reason=str(e))
            return None

    def options(self):
        """Option method."""
        pass


class AddBusiness(BaseHandler):
    """Create a new business."""

    def post(self):
        """Post the new business."""
        db = Database()
        business = self.get_body_params()

        if db.existsBusiness(business['tax_id']):
            self.set_status(404, reason='The business already exists')
            return None

        try:
            db.storeBusiness(business)
            response = {'tax_id': business['tax_id']}
            self.write(response)
        except Exception, e:
            logging.critical(str(e))
            self.set_status(404, reason=str(e))
            return None

    def options(self):
        """Option method."""
        pass


class GetBusiness(BaseHandler):
    """Get a stored business."""

    def get(self, business_id):
        """Search and return the business."""
        db = Database()

        if not db.existsBusiness(business_id):
            self.write({'tax_id': None})
        else:
            business = db.getBusiness(business_id)
            self.write({'tax_id': business['tax_id']})

    def options(self):
        """Option method."""
        pass


application = tornado.web.Application([
    (r"/api/getloanstatus/([0-9]+)", GetLoanStatus),
    (r"/api/addowner/", AddOwnerToBusiness),
    (r"/api/addbusiness/", AddBusiness),
    (r"/api/getbusiness/([0-9]+)", GetBusiness),
    (r"/api/version", VersionHandler),
])


if __name__ == "__main__":
    tornado.options.parse_command_line()
    logging.info('Starting the server')
    application.listen(8080)
    tornado.ioloop.IOLoop.instance().start()
