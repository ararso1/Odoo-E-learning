from odoo import models, fields ,api

class SlideChannel(models.Model):
    _inherit = 'slide.channel'
    overview_content = fields.Html('Over view Content', translate=True, sanitize_attributes=False, sanitize_form=False, help="Overview Content")
    instructor_content = fields.Html('instructor Content', translate=True, sanitize_attributes=False, sanitize_form=False, help="Instructor Content")
    demina_course_type = fields.Selection(
        selection=[
            ('certificate', 'Certificate'),
             ('deploma', 'Deploma'),
        ]
    )
    chat_url = fields.Char(string='Chat Group URL')
    @api.onchange('demina_course_type')
    def _onchange_demina_course_type(self):
        litags=[]
        for tag in self.tag_ids:
            if tag.name not in ['Certificate','Deploma']:
                litags.append(tag.id)
            self.tag_ids = litags
        if self.demina_course_type:
            tag_mapping = {
                'certificate': 'Certificate',
                'deploma': 'Deploma',
            }
            tag_name = tag_mapping.get(self.demina_course_type)
            if tag_name:
                tag = self.env['slide.channel.tag'].search([('name', '=', tag_name)], limit=1)
                if not tag:
                    group = self.env['slide.channel.tag.group'].search([('name','=','course')],limit=1)
                    if not group:
                        group = self.env['slide.channel.tag.group'].create({'name':'course'})
                    tag = self.env['slide.channel.tag'].sudo().create({'name': tag_name,'group_id':group.id})
                self.tag_ids = [(4, tag.id)]
