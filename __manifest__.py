{
    'name': "Doyarushka Click2dial",
    'version': "1.6.0",
    'author': "Ivan Sova",
    'category': "Tools",
    'license':'LGPL-3',
    'data': [
        # 'security/ir.model.access.csv',

        'views/crm_phonecall.xml',
        'views/website_support_ticket_views.xml',
        'views/res_users_views.xml',
        'web_asterisk_click2dial.xml',
    ],
    'demo': [],
    'depends': ['support_ticket', 
                'crm_phone', 
                'asterisk_click2dial'
                ],
    'installable': True,
}