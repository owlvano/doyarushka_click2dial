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
    ],
    'demo': [],
    'depends': ['website_support', 'crm_phone', 'asterisk_click2dial'],
    'installable': True,
}