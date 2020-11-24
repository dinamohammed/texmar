# -*- coding: utf-8 -*-

from odoo import api, fields, models, _


class SpecsConditions(models.Model):
    _inherit = 'sale.order'
    
    template_selection = fields.Selection(
        [('template_one', 'Template 1'), ('template_two', 'Template 2'),
         ('template_three', 'Template 3'), ('template_four', 'Template 4')],
        'Specifications and Conditions Template', default="template_one",
        help="Select a Specifications and Conditions Template")
    
    
    #TEMPLATE 1
    specs_conditions_1 = fields.Html(string='Template 1', required=True, default="""
                                    <ul>
                                    <li style='font-size:20px;'><b>All prices are in Egyptian pound LE and subject to 14% vat.</b></li>
                                    <li style='font-size:20px;'>Please note any fabric marked WRF are 100% flam ratadant polyster durable for 12 to 16 wash to match and pass the highest required American standard NFPA701</li>
                                    <li style='font-size:20px;'>All original fabric is construction engineered to match the project durability use and safety requirements.</li>
                                    <li style='font-size:20px;'>All fabrics made to pass aatcc 16e (U.S.A) Xeon test 5 blue scale minimum (for light fastness)</li>
                                    <li style='font-size:20px;'>Fabric specifications for indoor use only</li>
                                    <li style='font-size:20px;'>All fabrics made to pass aatcc 8 (U.S.A) for dry and wet grey scale (crocking fastness rubbing)</li>
                                    <li style='font-size:20px;'>All upholstery fabrics made to pass astm 4966 Abrasion test for upholstery items (20000 rubs minimum)</li>
                                    <p style='font-size:20px;'>Ordered qty subject for (5% + or -) on delivery</p>""")
    
    
    #TEMPLATE 2
    specs_conditions_2 = fields.Html(string='Template 2', required=True, default="""
                                    <ul>
                                    <li style='font-size:20px;'><b>All prices are in Egyptian pound LE and subject to 14% vat.</b></li>
                                    <li style='font-size:20px;'>Please note any fabric marked WRF are 100% flam ratadant polyster durable for 12 to 16 wash to match and pass the highest required American standard NFPA701</li>
                                    <li style='font-size:20px;'>All original fabric is construction engineered to match the project durability use and safety requirements.</li>
                                    <li style='font-size:20px;'>All fabrics made to pass aatcc 16e (U.S.A) Xeon test 5 blue scale minimum (for light fastness)</li>
                                    <li style='font-size:20px;'>Fabric specifications for indoor use only</li>
                                    <li style='font-size:20px;'>All fabrics made to pass aatcc 8 (U.S.A) for dry and wet grey scale (crocking fastness rubbing)</li>
                                    <li style='font-size:20px;'>All upholstery fabrics made to pass astm 4966 Abrasion test for upholstery items (20000 rubs minimum)</li>
                                    <p style='font-size:20px;'>Ordered qty subject for (5% + or -) on delivery</p>""")
    

    
    #TEMPLATE 3
    specs_conditions_3 = fields.Html(string='Template 3', required=True, default="""
                                    <ul>
                                    <li style='font-size:20px;'><b>All prices are in Egyptian pound LE and subject to 14% vat.</b></li>
                                    <li style='font-size:20px;'>Please note any fabric marked WRF are 100% flam ratadant polyster durable for 12 to 16 wash to match and pass the highest required American standard NFPA701</li>
                                    <li style='font-size:20px;'>All original fabric is construction engineered to match the project durability use and safety requirements.</li>
                                    <li style='font-size:20px;'>All fabrics made to pass aatcc 16e (U.S.A) Xeon test 5 blue scale minimum (for light fastness)</li>
                                    <li style='font-size:20px;'>Fabric specifications for indoor use only</li>
                                    <li style='font-size:20px;'>All fabrics made to pass aatcc 8 (U.S.A) for dry and wet grey scale (crocking fastness rubbing)</li>
                                    <li style='font-size:20px;'>All upholstery fabrics made to pass astm 4966 Abrasion test for upholstery items (20000 rubs minimum)</li>
                                    <p style='font-size:20px;'>Ordered qty subject for (5% + or -) on delivery</p>""")
    
    
    
    #TEMPLATE 4
    specs_conditions_4 = fields.Html(string='Template 4', required=True, default="""
                                    <ul>
                                    <li style='font-size:20px;'><b>All prices are in Egyptian pound LE and subject to 14% vat.</b></li>
                                    <li style='font-size:20px;'>Please note any fabric marked WRF are 100% flam ratadant polyster durable for 12 to 16 wash to match and pass the highest required American standard NFPA701</li>
                                    <li style='font-size:20px;'>All original fabric is construction engineered to match the project durability use and safety requirements.</li>
                                    <li style='font-size:20px;'>All fabrics made to pass aatcc 16e (U.S.A) Xeon test 5 blue scale minimum (for light fastness)</li>
                                    <li style='font-size:20px;'>Fabric specifications for indoor use only</li>
                                    <li style='font-size:20px;'>All fabrics made to pass aatcc 8 (U.S.A) for dry and wet grey scale (crocking fastness rubbing)</li>
                                    <li style='font-size:20px;'>All upholstery fabrics made to pass astm 4966 Abrasion test for upholstery items (20000 rubs minimum)</li>

                                    <p style='font-size:20px;'>Ordered qty subject for (5% + or -) on delivery</p>""")
