# -*- coding: utf-8 -*-

import re

from odoo import api, fields, models, _
from odoo.exceptions import Warning,ValidationError
from odoo.osv import expression


# Ahmed Salama Code Start ---->


class ProductAttributeInherit(models.Model):
    _inherit = "product.attribute"
    
    def unlink(self):
        color_attr = self.env.ref('product.product_attribute_2')
        treatment_attr = self.env.ref('egymentors_product_code.product_attribute_treatment')
        
        if color_attr.id in self.ids or treatment_attr.id in self.ids:
            raise Warning(_("You are not authorized to delete Color or Treatment Attribute"))
        return super(ProductAttributeInherit, self).unlink()


class ResCompanyInherit(models.Model):
    _inherit = "res.company"
    
    company_registry = fields.Char(size=2)


class ProductCategoryInherit(models.Model):
    _inherit = "product.category"
    
    code = fields.Char(string="Code", size=2)
    category_type = fields.Selection([('fabric', 'Fabric'),
                                      ('yarn', 'Yarn'),
                                      ('other', 'Other'),
                                      ('not', 'Un-Specified')], "Category Type", default='not')
    
    @api.model
    def create(self, vals):
        """
        Inherit Category type to childs
        :param vals:
        :return: Super
        """
        print("VALS ", vals)
        if vals.get('parent_id'):
            parent_id = self.browse(vals.get('parent_id'))
            if parent_id:
                vals['category_type'] = parent_id.category_type
        return super(ProductCategoryInherit, self).create(vals)
    
    def unlink(self):
        """
        Prevent Delete one of master categories
        :return:
        """
        unlinkable_categs = [self.env.ref('egymentors_product_code.product_category_fabric'),
                             self.env.ref('egymentors_product_code.product_category_yarn'),
                             self.env.ref('egymentors_product_code.product_category_other')]
        for cat in self:
            if cat in unlinkable_categs:
                raise Warning(_("You are not authorized to delete one"
                                " of un-linkable categories (Fabric, Yarn, Other)"))
            return super(ProductCategoryInherit, self).unlink()


class ProductTemplateInherit(models.Model):
    _inherit = 'product.template'
    
#     _sql_constraints = [
#                      ('default_code_unique', 
#                       'unique(default_code)',
#                       'Internal Reference has to be unique!')
#     ]
    
    placeholder = fields.Char(compute='o_change')
    parent_categ = fields.Many2one(related = 'categ_id.parent_id')
    style_field = fields.Char(string="Style", copy = False)
    # Cloths Parameters
    category_type = fields.Selection(related='categ_id.category_type')
    
    default_code = fields.Char('Internal Reference', index=True, copy = False)
    barcode = fields.Char('Barcode', store = True, readonly=False)
    # Fabric Parameters
    landry_code_id = fields.Many2one('product.landry.code', "Landry Code")
    texmar_weight = fields.Many2many('texmar.weight', 'product_weight_rel', 'product_id', 'weight_id',
                                     string='SUB CATEGORY')
    texmar_weight_2 = fields.Many2many('texmar.weight', 'product_weight2_rel', 'product_id', 'weight_id',
                                     string='DISCONTINUED')
#     texmar_width = fields.Float("Width")
    repeat_id = fields.Many2one('product.repeat', "Repeat")
    composition_id = fields.Many2one('product.composition', "Composition")
    abrasion = fields.Char("Abrasion")
    category_id = fields.Many2one('texmar.product.category', "Category")
    sub_category_id = fields.Many2one('texmar.product.sub.category', "Under Testing 1")
    collection_id = fields.Many2many('product.collection', 'product_collection_rel', 'product_id', 'coll_id',
                                     string='Collection Year')
    collection_id_2 = fields.Many2many('product.collection', 'product_collection2_rel', 'product_id', 'coll_id',
                                     string='Sample Box')
    manufacture_id = fields.Many2one('product.manufacture', "Manufacture")
    manufacture_type_id = fields.Many2one('product.manufacture.type', "Under Testing 2")
    fabric_type_id = fields.Many2one('product.fabric.type', "Fabric Type")
    usage_id = fields.Many2one('product.usage', "Usage")
    # Yarn Parameters
    texmar_color_id = fields.Many2one('product.texmar.color', "Color")
    kind_id = fields.Many2one('product.kind', "Kind")
    group_name_id = fields.Many2one('product.group.name', "Group Name")
    group_code = fields.Char(related='group_name_id.group_code')
    pant_id = fields.Many2one('product.pant', "Pant Name")
    pant_code = fields.Char(related='pant_id.pant_code')
    origin_id = fields.Many2many('product.origin', 'product_origin_rel', 'product_id', 'origin_id',
                                 string='Origin')
    under_testing_id = fields.Many2one('product.under.testing', "Under-Testing")
    
    texmar_width = fields.Many2one('product.width',"Width")
    
    @api.constrains('default_code')
    def default_code_unique_constrain(self):
        for product in self:
            if product.default_code and \
            self.env['product.template'].search_count([('default_code', '=', product.default_code)]) > 1:
                raise Warning(_("Internal Reference violating unique constrain!!!"))

    @api.onchange('style_field','attribute_line_ids')
    @api.depends('style_field')
    def o_change(self):
        for line in self:
            variants = line.env['product.product'].search([('product_tmpl_id.id','=',self.id.origin)])
            if len(variants) > 1:
                for variant in  variants:
                    variant.style_field = line.style_field
                    variant._generate_product_code()
        self._generate_product_code()


    @api.onchange('parent_categ', 'categ_id','attribute_line_ids')
    @api.depends('categ_id.code')
    def _generate_product_code(self):
        """
		Generate code of each product using it's component
        parent categ Code from field [parent categ code] [2 digits]
        Category Code from field [Category Code] [2 digits]
        Style Code from field [Variant Style] [8 digits]
		"""
        for template in self:
            single_product_code = False
            if template.categ_id.category_type != 'not':
                parent_categ = ''
                category_code = ''
                style_code = ''
                barcode_style_code = ''
                if template.parent_categ and template.parent_categ.code:
                    parent_categ = template.parent_categ.code[:2]
                else:
                    parent_categ = "TX"
                if template.categ_id and template.categ_id.code:
                    category_code = template.categ_id.code[:2]
                else:
                    category_code = "00"
                if template.style_field:
                    style_code = template.style_field
                    barcode_style_code = template.style_field
                else:
                    style_code = "00000000"
                    barcode_style_code = "00000"
                color_code = ''
                treatment_code = ''
#                 raise ValidationError('%s'%len(template.attribute_line_ids.value_ids))
                if (len(template.attribute_line_ids) == 1 and len(template.attribute_line_ids[0]['value_ids'])==1)\
                or (len(template.attribute_line_ids) == 2 and len(template.attribute_line_ids[0]['value_ids'])==1 \
                   and len(template.attribute_line_ids[1]['value_ids'])==1):
                        single_product_code = True
                        color_attr = self.env.ref('product.product_attribute_2')
                        treatment_attr = self.env.ref('egymentors_product_code.product_attribute_treatment')
                    
                        for attribute in template.attribute_line_ids:
                            if attribute.attribute_id == color_attr and attribute.value_ids:
                                color_code = attribute.value_ids.name[:4]
                            if attribute.attribute_id == treatment_attr and attribute.value_ids:
                                treatment_code = attribute.value_ids.name[:2]
                        new_color_code = ''
                        for word in color_code.split():
                            if word.isdigit():
                                new_color_code += word
                        
                if single_product_code == True:
                    if treatment_code == "":
                            template.default_code = "%s%s-%s-%s" % (parent_categ, category_code,
                                                   style_code, new_color_code)
                    else:
                            template.default_code = "%s%s-%s-%s-%s" % (parent_categ, category_code,
                                                   style_code, new_color_code, treatment_code)
                            template.barcode = "%s%s%s%s%s" % (parent_categ, category_code,
                                                   style_code, new_color_code, treatment_code)
                else:
                    template.default_code = "%s%s-%s" % (parent_categ, category_code, style_code)
                    template.barcode = "%s%s%s" % (parent_categ, category_code, style_code)
                    
                    
            else:
                template.default_code = ""
                template.barcode = ""
                        
            # raise ValidationError('afafa')

class ProductProductInherit(models.Model):
    _inherit = 'product.product'
    
#     _sql_constraints = [
#                      ('default_code_unique', 
#                       'unique(default_code)',
#                       'Internal Reference has to be unique!')
#     ]
    
    style_field = fields.Char(string="Style")
    default_code = fields.Char(copy=False,compute='_generate_product_code',store = True)
    barcode = fields.Char(copy=False, compute='_generate_product_code', store = True)
    parent_categ = fields.Many2one('product.category', 'Parent Category')
    category_code = fields.Char(compute='_generate_product_code', size=2,
                                help="Category Code from field [Category Code] [2 digits]")
    style_code = fields.Char(compute='_generate_product_code', size=8,
                             help="Style Code from field [Variant Style] [8 digits")
    barcode_style_code = fields.Char(compute='_generate_product_code', size=5,
                                     help="Style Code from field [Variant Style] [8 digits")
    color_code = fields.Char(compute='_generate_product_code', size=4,
                             help="Color Code from field [Variant Color Attribute] [4 digits]")
    treatment_code = fields.Char(compute='_generate_product_code', size=2,
                                 help="Treatment Code from field [Variant Treatment Attribute] [2 digits]")
    parent_categ_code = fields.Char(related = 'parent_categ.code')
    
    @api.onchange('parent_categ', 'categ_id', 'product_tmpl_id',
                  'product_template_attribute_value_ids','product_tmpl_id.attribute_line_ids')
    @api.depends('categ_id.code','product_template_attribute_value_ids')
    def _generate_product_code(self):
        """
        Generate code of each product using it's component 
            parent categ Code from field [parent categ code] [2 digits]
            Category Code from field [Category Code] [2 digits]
            Style Code from field [Variant Style] [8 digits]
            Color Code from field [Variant Color Attribute] [4 digits]
            Treatment Code from field [Variant Treatment Attribute] [2 digits]
        """
        for product in self:
            color_attr = self.env.ref('product.product_attribute_2')
            treatment_attr = self.env.ref('egymentors_product_code.product_attribute_treatment')
            if product.categ_id.category_type != 'not':
                if product.parent_categ and product.parent_categ.code:
                    categ_code = product.parent_categ.code[:2]
                else:
                    categ_code  = "TX"
                if product.categ_id and product.categ_id.code:
                    product.category_code = product.categ_id.code[:2]
                else:
                    product.category_code = "00"
                if product.style_field:
                    product.style_code = product.style_field[:8]
                    product.barcode_style_code = product.style_field[-5:].lstrip("0")
                else:
                    product.style_code = "00000000"
                    product.barcode_style_code = "00000"
            
                for attr_val_line in product.product_template_attribute_value_ids:

                    if attr_val_line.attribute_id == color_attr \
                            and attr_val_line.product_attribute_value_id:
                        product.color_code = attr_val_line.product_attribute_value_id.name[:4]
                    if attr_val_line.attribute_id == treatment_attr \
                            and attr_val_line.product_attribute_value_id:
                        product.treatment_code = attr_val_line.product_attribute_value_id.name[:2]
            
                if not product.color_code:
                    product.color_code = "0000"
                if not product.treatment_code:
                    product.treatment_code = ""
                elif product.treatment_code == "00":
                    product.treatment_code = ""
                color_code = ""
                for word in product.color_code.split():
                    if word.isdigit():
                        color_code += word
#                 style_code2 = ""
#                 if len(product.style_code.lstrip("0")) < 8 :        
#                     style_code2 = '0' + product.style_code.lstrip("0")
#                 else:
#                     style_code2 = product.style_code.lstrip("0")
                if product.treatment_code == "":
                    product.default_code = "%s%s-%s-%s" % (categ_code, product.category_code,
                                                   product.style_field, color_code)
                else:
                    product.default_code = "%s%s-%s-%s-%s" % (categ_code, product.category_code,
                                                   product.style_field, color_code, product.treatment_code)
                product.barcode = "%s%s%s%s%s" % (categ_code, product.category_code,
                                            product.style_field, color_code,product.treatment_code)
            else:
                product.default_code = ""
                product.barcode = ""


            

class TexmarWeight(models.Model):
    _name = 'texmar.weight'
    _description = "SUB CATEGORY / DISCONTINUED"
    
    name = fields.Char("SUB CATEGORY / DISCONTINUED") 
    
            
class ProductLandryCode(models.Model):
    _name = 'product.landry.code'
    _description = "Landry Code"
    
    name = fields.Char("Landry Code")


class ProductRepeat(models.Model):
    _name = 'product.repeat'
    _description = "Repeat"
    
    name = fields.Char("Repeat")


class ProductComposition(models.Model):
    _name = 'product.composition'
    _description = "Composition"
    
    name = fields.Char("Composition")


class ProductCategory(models.Model):
    _name = 'texmar.product.category'
    _description = "Category"
    
    name = fields.Char("category")


class ProductSubCategory(models.Model):
    _name = 'texmar.product.sub.category'
    _description = "Sub Category"
    
    name = fields.Char("Sub Category")


class ProductCollection(models.Model):
    _name = 'product.collection'
    _description = "Collection"
    
    name = fields.Char("Collection Year / Sample Box")


class ProductManufacture(models.Model):
    _name = 'product.manufacture'
    _description = "Manufacture"
    
    name = fields.Char("Manufacture")


class ProductManufactureType(models.Model):
    _name = 'product.manufacture.type'
    _description = "Manufacture Type"
    
    name = fields.Char("Manufacture Type")
    
    
class ProductFabricType(models.Model):
    _name = 'product.fabric.type'
    _description = "Fabric Type"
    
    name = fields.Char("Fabric Type")


class ProductUsage(models.Model):
    _name = 'product.usage'
    _description = "Usage"
    
    name = fields.Char("Usage")

class ProductTexmarColor(models.Model):
    _name = 'product.texmar.color'
    _description = "Color"
    
    name = fields.Char("Color")


class ProductKind(models.Model):
    _name = 'product.kind'
    _description = "Kind"
    
    name = fields.Char("Kind")


class ProductPant(models.Model):
    _name = 'product.pant'
    _description = "Pant"
    
    name = fields.Char("Pant Name")
    pant_code = fields.Char("Pant Code")


class ProductGroupName(models.Model):
    _name = 'product.group.name'
    _description = "Group Name"
    
    name = fields.Char("Group Name")
    group_code = fields.Char("Group Code")


class ProductOrigin(models.Model):
    _name = 'product.origin'
    _description = "Origin"
    
    name = fields.Char("Origin")


class ProductUnderTesting(models.Model):
    _name = 'product.under.testing'
    _description = "Under-Testing"
    
    name = fields.Char("Under-Testing")
    

class ProductWidth(models.Model):
    _name = 'product.width'
    _description = "Product Width"
    
    name = fields.Float("Width")
# Ahmed Salama Code End.
