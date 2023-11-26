from odoo import models, fields

class StudentAchievement(models.Model):
    _name = 'student.achievement'
    _description = 'Student Achievement'

    name = fields.Char(string='Student Name', required=True)
    #achievement1 = fields.Text(string='Achievement1')
    #achievement2 = fields.Text(string='Achievement2')
    nlratio = fields.Float(string='Nilai Ratio')
    rank = fields.Integer(string='Peringkat')
    #date = fields.Date(string='Date')
    
