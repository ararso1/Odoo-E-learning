import csv
import base64
from io import StringIO
from odoo.http import request
from odoo import api, fields, models, _
from odoo.exceptions import UserError

class SlideChannelInvite(models.TransientModel):
    _inherit = 'slide.channel.invite'
    csv_file = fields.Binary(string="CSV File")
    csv_filename = fields.Char(string="CSV Filename")

    @api.onchange('csv_file')
    def _onchange_csv_file(self):
        """ Populate partner_ids based on the uploaded CSV file. """
        if not self.csv_file:
            self.partner_ids = [(5, 0, 0)]  # Clear partner_ids if no file is uploaded
            return

        try:
            # Decode and read the CSV file
            decoded_file = base64.b64decode(self.csv_file).decode('utf-8')
            csv_reader = csv.DictReader(StringIO(decoded_file))
        except Exception as e:
            raise UserError(_("Failed to process the CSV file. Ensure it is properly formatted: %s") % e)

        # Extract emails and find matching partners
        emails = []
        for row in csv_reader:
            email = row.get('email')
            if email:
                emails.append(email.strip())

        if not emails:
            raise UserError(_("No valid email addresses found in the CSV file."))

        # Search for partners with the extracted emails
        print(emails)
        partners = self.env['res.partner'].search([('email', 'in', emails)])

        if not partners:
            raise UserError(_("No matching partners found for the provided email addresses."))

        # Populate the partner_ids field
        self.partner_ids = [(6, 0, partners.ids)] 