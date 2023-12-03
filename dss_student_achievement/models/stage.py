from odoo import models, fields, api, _
from odoo.exceptions import UserError
class Rank_stage(models.Model):
    _name = "rank.stage"
    _description = "Model to store the sequence stage"

    # name = fields.Char('Name', required=True)
    criteria = fields.Char('Criteria', required=True)
    group_id = fields.Char('Group', default='Criteria')
    sequence = fields.Integer('Sequence')
    readonly = fields.Boolean('Readonly', default=False)
                
    # untuk mencegah kriteria tidak diubah rank ordernya
    @api.constrains('sequence')
    def _check_sequence(self):
        # stage_first_id = self.env.ref('dss_student_achievement.rank_stage_first').id 
        # stage_last_id = self.env.ref('dss_student_achievement.rank_stage_last').id 
        stage_first_id = self.env['rank.stage'].search([])[0].id
        stage_last_id = self.env['rank.stage'].search([])[-1].id
        for stage in self:
            if stage.id == stage_first_id:
                if stage.sequence != 1:
                    raise UserError(_(f'You cannot change the order of first stage. ID: {stage.id} sequence: {stage.sequence}'))
            if stage.id == stage_last_id:
                if stage.sequence != len(self.env['rank.stage'].search([])):
                    raise UserError(_(f'You cannot change the order of last stage. ID: {stage.id} sequence: {stage.sequence}'))
    
    def get_stage_rank(self):
        datastage = self.env['rank.stage'].search_read([])
        arrstage = []
        for item in datastage:
            arrstage.append({
                'name':item['criteria'],
                'rank':item['sequence'],
            })
        return arrstage



