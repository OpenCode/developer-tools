# -*- coding: utf-8 -*-
# © 2016 Francesco Apruzzese <cescoap@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

{
    "name": "Test Builder",
    "version": "8.0.0.1.0",
    "author": "Francesco Apruzzese",
    "category": "Tools",
    "website": "http://www.apuliasoftware.it",
    "license": "GPL-3 or any later version",
    'depends': [
        'base',
        ],
    'data': [
        'security/ir.model.access.csv',
        'views/test_builder_view.xml',
        'wizard/test_builder.xml',
        ],
    'installable': True,
}
