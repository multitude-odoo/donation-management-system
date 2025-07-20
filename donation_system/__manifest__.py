{
    'name': 'Donation Management System',
    'version': '1.1',
    'category': 'Charity',
    'sequence': 13,
    'author': 'Dextra Technologies',
    'website': 'http://www.dextratechnologies.com',
    'summary': 'Manage charity donations, volunteers, campaigns and payments',
    'description': "",
    'depends': ['base', 'mail','website','crm'],
    'data': [
        # 'security/security.xml',
        'security/ir.model.access.csv',

        'data/donation_sequence.xml',

        'views/menus.xml',
        'views/campaign.xml',
        'views/donor.xml',
        'views/volunteer.xml',
        'views/donations.xml',
        'views/campaign_template.xml',
        'views/donor_template.xml',
        'views/donation_form.xml',

    ],
    'qweb': [

    ],
    'demo': [
    ],
    'css': [],
    'images': ['static/description/icon.png'],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',



}
