from odoo import models, fields, api

class DataTes(models.Model):
    _name = "data.tes"
    _description = "data Import"
    # external_id,name,email,phone,gender,age

    external_id = fields.Char(string="external_id", required=True)
    name = fields.Char(string="name", required=True)
    email = fields.Char(string="email", required=True)
    phone = fields.Char(string="phone", required=True)
    gender = fields.Char(string="gender", required=True)
    age = fields.Char(string="age", required=True)