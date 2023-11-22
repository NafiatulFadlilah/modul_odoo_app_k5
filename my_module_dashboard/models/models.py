from odoo import models, fields

class StudentAchievement(models.Model):
    _name = 'student.achievement'
    _description = 'Student Achievement'

    name = fields.Char(string='Student Name', required=True)
    achievement = fields.Text(string='Achievement')
    date = fields.Date(string='Date')
