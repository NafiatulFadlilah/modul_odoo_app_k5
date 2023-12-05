from odoo import api, models, fields

class StudentAchievement(models.Model):
    _name = 'student.achievement'
    _description = 'Student Achievement'

    name = fields.Char(string='Student Name', required=True)
    #achievement1 = fields.Text(string='Achievement1')
    #achievement2 = fields.Text(string='Achievement2')
    nlratio = fields.Float(string='Nilai Ratio')
    rank = fields.Integer(string='Peringkat')
    #date = fields.Date(string='Date')
    @api.model
    def _write_records(self):
        rank_model = self.env['rank.model'].search([], limit=5)
        for record in rank_model:
            self.create({
                'name': record.name,
                'nlratio': record.ratio,
                'rank': record.rank
            })

    @api.model
    def _register_hook(self):
        super(StudentAchievement, self)._register_hook()
        self._write_records()
