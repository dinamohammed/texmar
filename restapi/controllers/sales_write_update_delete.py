from odoo import http,fields,models
from odoo.http import request,Response,JsonRequest
from odoo.exceptions import ValidationError,AccessError
import io
import base64
from . import controllers
class reporting(controllers.Restapi): 
 
     @http.route('/confirm_order',type='json',auth='none',cors='*')
     def confirm_order(self,DevToken,UserToken,order_id,base_location=None):
         try:
            if self.authrize_developer(DevToken) == False:
                return {'error':'your session is expired , please relogin  '}
            elif not self.authrize_user(UserToken):
                return {'error':'invalid user token'}
            else:
                user_info = self.authrize_user(UserToken)
                request.session.authenticate(self.db,user_info['login'],user_info['password'])
                sale = request.env['sale.order'].search([('id','=',order_id)])
                if sale: 
                    company_id = sale.company_id.id
                    company = request.env['res.company'].search([('id','=',company_id)])
                    #ensuring that there is parent_id in the company to avoid error
                    if not(company.parent_id):
                        parent_company_id = request.env['res.company'].search([('company_registry','!=',False)]) #the main company
                        company.parent_id = parent_company_id 
                        
                    sale.env.company = company
                    sale.action_confirm_note_order()
                    
                return 'order confirmed' if sale else 'sale order not found'
         
         except AccessError:
            return 'You are not allowed to do this'    
     
    
     @http.route('/delete_order',type='json',auth='none',cors='*')
     def delete_order(self,DevToken,UserToken,order_id,base_location=None):
         try:
            if self.authrize_developer(DevToken) == False:
                return {'error':'your session is expired , please relogin  '}
            elif not self.authrize_user(UserToken):
                return {'error':'invalid user token'}
            else:
                user_info = self.authrize_user(UserToken)
                request.session.authenticate(self.db,user_info['login'],user_info['password'])
                sale = request.env['sale.order'].search([('id','=',order_id)])
                sale.write({'state':'cancel'})
                sale.unlink()
                return 'order deleted' if sale else 'sale order not found'
         
         except AccessError:
            return 'You are not allowed to do this'
        
     
     @http.route('/add_to_cart',type='json',auth='none',cors='*')
     def add_to_cart(self,DevToken,UserToken,customer_id,product_id,qty,order_id,base_location=None):
         try:            
            if self.authrize_developer(DevToken) == False:
                return {'error':'your session is expired , please relogin  '}
            elif not self.authrize_user(UserToken):
                return {'error':'invalid user token'}
            else:
                user_info = self.authrize_user(UserToken)
                request.session.authenticate(self.db,user_info['login'],user_info['password'])
                #get companies
                company_id = self.prepare_allowed_companies(user_info['login'])[0]
                company = request.env['res.company'].search([('id','=',company_id)])
                # sale order preprations
                sale_order = request.env['sale.order']
                sale_order.env.company = company
                #get customers info
                customer =  request.env['res.partner'].search([('id','=',customer_id)])
                #get product
                product =  request.env['product.product'].search([('id','=',product_id)])                
                # check if this customer has a note order still open
                if order_id:
                    old_sale = request.env['sale.order'].search([('id','=',order_id)])
                    if old_sale:  
                        sol = {
                            'product_id':product.id,
                            'product_uom_qty':qty,
                            'order_id':old_sale.id,
                            'to_sell':True
                        }
                        old_sale['order_line'].create(sol)
                        return 'added successfully'
                    else:
                        return 'order not found'
                else:
                    new_sale = sale_order.create({
                        'partner_id':customer.id,
                        'state':'note_order',
                        'company_id':company_id,
                        'order_line':[]
                    })
                    sol = {
                        'product_id':product.id,
                        'product_uom_qty':qty,
                        'order_id':new_sale.id,
                        'to_sell':True
                    }
                    new_sale['order_line'].create(sol)
                    return {'order_id':new_sale.id}
                    
                
     
         except AccessError:
            return 'You are not allowed to do this'
        
        
        
     @http.route('/delete_product',type='json',auth='none',cors='*')
     def delete_product(self,DevToken,UserToken,order_id,base_location=None):
        try:            
            if self.authrize_developer(DevToken) == False:
                return {'error':'your session is expired , please relogin  '}
            elif not self.authrize_user(UserToken):
                return {'error':'invalid user token'}
            else:
                user_info = self.authrize_user(UserToken)
                request.session.authenticate(self.db,user_info['login'],user_info['password'])
                line = request.env['sale.order.line'].search([('id','=',order_id)])
                line.unlink()
                return 'deleted succesfully'
                
         
        except AccessError:
            return 'You are not allowed to do this'            

     
     @http.route('/edit_product_qty',type='json',auth='none',cors='*')
     def edit_product_qty(self,DevToken,UserToken,order_line_id,qty,base_location=None):
        try:            
            if self.authrize_developer(DevToken) == False:
                return {'error':'your session is expired , please relogin  '}
            elif not self.authrize_user(UserToken):
                return {'error':'invalid user token'}
            else:
                user_info = self.authrize_user(UserToken)
                request.session.authenticate(self.db,user_info['login'],user_info['password'])
                line = request.env['sale.order.line'].search([('id','=',order_line_id)])
                line.write({
                    "product_uom_qty":qty
                })
                return 'edited succesfully'
                
         
        except AccessError:
            return 'You are not allowed to do this' 