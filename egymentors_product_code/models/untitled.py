if template.valid_product_template_attribute_line_ids:
                color_code = ''
                treatment_code = ''
                color_attr = self.env.ref('product.product_attribute_2')
                treatment_attr = self.env.ref('egymentors_product_code.product_attribute_treatment')
                for attribute in template.valid_product_template_attribute_line_ids:
                    if attr_val_line.attribute_id == color_attr \
                            and attr_val_line.product_attribute_value_id:
                        color_code = attr_val_line.product_attribute_value_id.name[:4]
                    if attr_val_line.attribute_id == treatment_attr \
                            and attr_val_line.product_attribute_value_id:
                        treatment_code = attr_val_line.product_attribute_value_id.name[:2]
                    
                    for word in color_code.split():
                        if word.isdigit():
                            color_code += word
                            
                if treatment_code == "":
                    template.default_code = "%s%s-%s-%s" % (parent_categ, category_code,
                                                   style_code, color_code)
                else:
                    template.default_code = "%s%s-%s-%s-%s" % (parent_categ, category_code,
                                                   style_code, color_code, treatment_code)
                template.barcode = "%s%s%s%s%s" % (parent_categ, category_code,
                                                   style_code, color_code, treatment_code)