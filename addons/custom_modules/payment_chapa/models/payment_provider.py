import logging
import requests
from odoo import http
import random
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
import json
import base64
# from Crypto.PublicKey import RSA
# from Crypto.Cipher import PKCS1_v1_5
import binascii
from odoo.exceptions import AccessError


_logger = logging.getLogger(__name__)

class PaymentProvider(models.Model):
    _inherit = 'payment.provider'

    code = fields.Selection(selection_add=[('chapa', 'chapa')],
                            ondelete={'chapa': 'set default'},
                            help="The technical code of this payment provider",
                            string="Code")
    
    chapa_public_api_key = fields.Char(
        string="Chapa Public API Key", help="The API key of the webservice user", required_if_provider='chapa',
        groups='base.group_system')
    chapa_private_key = fields.Char(
        string="Chapa Private Key", help="The client key of the webservice user",
        required_if_provider='chapa')
    chapa_checkout_api_url = fields.Char(
        string="Chapa Checkout API URL", help="The base URL for the Checkout API endpoints",
        required_if_provider='chapa')
    chapa_return_api_url = fields.Char(
        string="Return Url", help="The base URL for the return API endpoints",
        required_if_provider='chapa')
    chapa_callback_api_url = fields.Char(
        string="Chapa callback API URL", help="The base URL for the callback API endpoints",
        required_if_provider='chapa')
    
    @api.model
    def create(self, vals):
        if not self.env.user._is_superuser():
            raise AccessError("Only superusers can create or edit Payment Data")
        return super(PaymentProvider, self).create(vals)
    @api.model
    def write(self, vals):
        if not self.env.user._is_superuser():
            raise AccessError("Only superusers can create or edit Payment Data")
        return super(PaymentProvider, self).write(vals)
    
    def parse_public_key(self,public_key):
        decoded_public_key = base64.b64decode(public_key)
        rsa_key = RSA.import_key(decoded_public_key)
        return rsa_key

    def parse_private_key(self,private_key):
        decoded_private_key = base64.b64decode(private_key)
        rsa_key = RSA.import_key(decoded_private_key)
        return rsa_key

    def encrypt_data(self,data, public_key):
        rsa_key = self.parse_public_key(public_key)
        cipher = PKCS1_v1_5.new(rsa_key)
        encrypted_bytes = cipher.encrypt(data.encode())
        return base64.b64encode(encrypted_bytes).decode()

    def decrypt_data(self,encrypted_data, private_key):
        rsa_key = self.parse_private_key(private_key)
        cipher = PKCS1_v1_5.new(rsa_key)
        decoded_encrypted_data = base64.b64decode(encrypted_data)
        decrypted_bytes = cipher.decrypt(decoded_encrypted_data, None)
        return decrypted_bytes.decode()

    def encryptor(self,data):
        return data
        encrypted = self.encrypt_data(data, str(self.chapa_public_api_key).strip())
        return encrypted


    @api.model
    def _get_payment_method_information(self):
        res = super()._get_payment_method_information()
        res['chapa'] = {'mode': 'unique', 'domain': [('type', '=', 'bank')]}
        return res

    def _chapa_make_request(self, url, data=None, method='GET'):
        callback_url= "https://elearning.daminaa.org"+"/get-status-chapa"
        return_url="https://elearning.daminaa.org"+"/payment/status"
        datua = {
            "data": {
                "amount": -1,
                "tx_ref": "",
                "currency": self.encryptor("ETB"),
                "first_name": "haile",
                "email": self.encryptor("remamtsega@gmail.com"),
                "phone_number":self.encryptor("0947731212"),
                "last_name": "tsega",
                "customization": {
                    "title": "Payment",
                    "description": "I love online payments"
                },
            "callback_url":self.encryptor(callback_url),
            "return_url":self.encryptor(return_url)
    
            },
            
            "message": self.encryptor("hello work my..")
            
        }

        headers = {
    'Authorization': f'Bearer {self.chapa_private_key}',
    'Content-Type': 'application/json'
    }

    
        self.ensure_one()
        datua["data"]["first_name"]=self.encryptor(data["partner_name"])
        datua["data"]["last_name"]=self.encryptor(data["partner_name"])
        datua["data"]["tx_ref"]=self.encryptor(data["ref"])
        datua["data"]["amount"]=self.encryptor(data["amount"])
        headers["Auth"]=self.chapa_callback_api_url
        response = requests.post(self.chapa_checkout_api_url, json=datua['data'], headers=headers)
        response_content = response.json()
        data["Auth_key"]=self.chapa_public_api_key
        data["api_url"] = response_content['data']["checkout_url"]
        return data
    
