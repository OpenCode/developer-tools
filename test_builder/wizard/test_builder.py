# -*- coding: utf-8 -*-
# © 2016 Francesco Apruzzese <cescoap@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).


from openerp import models, fields, api


class TestBuilderWizard(models.TransientModel):

    _name = 'test.builder.wizard'

    result = fields.Text()

    @api.multi
    def build(self):
        self.ensure_one()
        wizard = self[0]
        # ----- Define a template for function
        def_template = """def _create_{model_name}_{id}(self):
    return self.env['{model}'].create({values})"""
        model = self.env.context['active_model']
        result = ''
        test_builder = self.env['test.builder'].search([
            ('ref_ir_act_window_id', '=', self.env.context['params']['action'])
            ])
        # ----- Create a function for every selected record
        for record in self.env[model].browse(self.env.context['active_ids']):
            # ----- Extract the value for every valied field
            values = []
            for field in test_builder.fields_ids:
                val = record[field.field_id.name]
                if val is not False and field.field_id.ttype in (
                        'char', 'html', 'selection', 'text'):
                    val = "'%s'" % val
                values.append("'{f}': {v}".format(f=field.field_id.name,
                                                  v=val))
            # ----- Fill the function template
            function = def_template.format(
                model_name=model.replace('.', '_'),
                model=model,
                id=record.id,
                values='{\n        %s}' % ',\n        '.join(values),
                )
            # ----- Update global text
            result = '{function}\n\n{result}'.format(
                function=function,
                result=result, )
        self.result = result
        return {
            'context': self.env.context,
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'test.builder.wizard',
            'res_id': wizard.id,
            'view_id': False,
            'type': 'ir.actions.act_window',
            'target': 'new',
            }
