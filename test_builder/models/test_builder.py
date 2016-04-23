# -*- coding: utf-8 -*-
# © 2016 Francesco Apruzzese <cescoap@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

from openerp import models, fields, api
from openerp.exceptions import Warning as UserError


class TestBuilder(models.Model):

    _name = 'test.builder'

    name = fields.Char(required=True)
    model_id = fields.Many2one('ir.model', required=True)
    ref_ir_act_window_id = fields.Many2one('ir.actions.act_window')
    ref_ir_value_id = fields.Many2one('ir.values')
    fields_ids = fields.One2many('test.builder.fields', 'test_builder_id')

    @api.onchange('model_id')
    def on_change_model_id(self):
        if self.model_id:
            self.name = self.model_id.name
            # ----- Extract the readable fields of the model
            fields = self.env['ir.model.fields'].search([
                ('model_id', '=', self.model_id.id),
                # ----- Exlude relation fields. Will be implemented.
                ('ttype', 'in', ('boolean', 'char', 'date', 'datetime', 'float',
                                 'html', 'integer', 'selection', 'text')),
                # ----- Exlude ORM fields
                ('name', 'not in', ('active', 'create_date', 'id',
                                    '__last_update', 'write_date'))
                ])
            self.fields_ids = [(5, ), ]
            self.fields_ids = [(0, 0, {'field_id': f.id}) for f in fields]

    @api.multi
    def create_action(self):
        self.ensure_one()
        action_model = self.env['ir.actions.act_window']
        ir_values_model = self.env['ir.values']
        tb = self[0]
        src_model = tb.model_id.model
        button_name = 'Test Builder (%s)' % tb.name
        ref_ir_act_window = action_model.sudo().create(
            {
                'name': button_name,
                'type': 'ir.actions.act_window',
                'res_model': 'test.builder.wizard',
                'src_model': src_model,
                'view_type': 'form',
                'context': "{'test_builder_object' : %d}" % tb.id,
                'view_mode': 'form,tree',
                'target': 'new',
                'auto_refresh': 1,
            })
        ref_ir_value = ir_values_model.sudo().create(
            {
                'name': button_name,
                'model': src_model,
                'key2': 'client_action_multi',
                'value': (
                    "ir.actions.act_window," +
                    str(ref_ir_act_window.id)),
                'object': True,
            })
        self.ref_ir_act_window_id = ref_ir_act_window.id \
            if ref_ir_act_window \
            else False
        self.ref_ir_value_id = ref_ir_value.id \
            if ref_ir_value \
            else False
        return True

    @api.multi
    def unlink_action(self):
        self.ensure_one()
        tb = self[0]
        try:
            if tb.ref_ir_act_window_id:
                tb.ref_ir_act_window_id.unlink()
            if tb.ref_ir_value_id:
                tb.ref_ir_value_id.unlink()
        except:
            raise UserError("Deletion of the action record failed.")
        return True


class TestBuilderFields(models.Model):

    _name = 'test.builder.fields'

    field_id = fields.Many2one('ir.model.fields', required=True,
                               string='Field')
    test_builder_id = fields.Many2one('test.builder')
