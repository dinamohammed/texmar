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
                return {'error':'developer token expired'}
            elif not self.authrize_user(UserToken):
                return {'error':'invalid user token'}
            else:
                user_info = self.authrize_user(UserToken)
                request.session.authenticate(self.db,user_info['login'],user_info['password'])
                sale = request.env['sale.order'].search([('id','=',order_id)])
                company_id = sale.company_id.id
                company = request.env['res.company'].search([('id','=',company_id)])
                sale.env.company = company
                sale.action_confirm_note_order()
                return 'order confirmed' if sale else 'sale order not found'
         
         except AccessError:
            return 'You are not allowed to do this'    
     
    
     @http.route('/delete_order',type='json',auth='none',cors='*')
     def delete_order(self,DevToken,UserToken,order_id,base_location=None):
         try:
            if self.authrize_developer(DevToken) == False:
                return {'error':'developer token expired'}
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
     def add_to_cart(self,DevToken,UserToken,customer_id,product_id,qty,base_location=None):
         try:            
            if self.authrize_developer(DevToken) == False:
                return {'error':'developer token expired'}
            elif not self.authrize_user(UserToken):
                return {'error':'invalid user token'}
            else:
                user_info = self.authrize_user(UserToken)
                request.session.authenticate(self.db,user_info['login'],user_info['password'])
                #get companies
                company_id = self.prepare_allowed_companies(user_info['login'])[0]
                company = request.env['res.company'].search([('id','=',company_id)])
                old_sale = request.env['sale.order'].search([('partner_id.id','=',customer_id),('state','=','note_order'),('is_confirmed','=',False)])
                # sale order preprations
                sale_order = request.env['sale.order']
                sale_order.env.company = company
                #get customers info
                customer =  request.env['res.partner'].search([('id','=',customer_id)])
                #get product
                product =  request.env['product.product'].search([('id','=',product_id)])
                # check if this customer has a note order still open
                if old_sale:
                    sol = {
                        'product_id':product.id,
                        'product_uom_qty':qty,
                        'order_id':old_sale.id
                    }
                    old_sale['order_line'].create(sol)
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
                        'order_id':new_sale.id
                    }
                    new_sale['order_line'].create(sol)
 
                return 'added successfully'
     
         except AccessError:
            return 'You are not allowed to do this'     
        
        