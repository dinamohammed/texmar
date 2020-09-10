from odoo import http,fields,models
from odoo.http import request,Response,JsonRequest
from odoo.exceptions import ValidationError,AccessError,AccessDenied
import io
import base64
import jwt
import re
from datetime import datetime,timedelta,timezone
from . import controllers

class get(controllers.Restapi):
     @http.route('/stores_locations',type='json',auth='none',cors='*')
     def stores_locations(self,DevToken,UserToken,base_location=None):
        result = []
        try:
            if self.authrize_developer(DevToken) == False:
                return {'error':'developer token expired'}
            elif not self.authrize_user(UserToken):
                return {'error':'invalid user token'}
            else:
                user_info = self.authrize_user(UserToken)
                request.session.authenticate(self.db,user_info['login'],user_info['password'])
                companies = request.env['res.company'].search([])
                for company in companies:
                    vals = {
                            'mobile':company.phone,
                            'address':company.street or company.street2,
                            'lat':company.lat,
                            'long':company.long,
                        }
                    result.append(vals)
                return result
        except AccessError:
            return 'You are not allowed to do this'
    
    
    
     @http.route('/notes',type='json',auth='none',cors='*')
     def notes(self,DevToken,UserToken,base_location=None):
         try:
            if self.authrize_developer(DevToken) == False:
                return {'error':'developer token expired'}
            elif not self.authrize_user(UserToken):
                return {'error':'invalid user token'}
            else:
                user_info = self.authrize_user(UserToken)
                request.session.authenticate(self.db,user_info['login'],user_info['password'])
                
                drafts = request.env['sale.order'].search([('state','=','note_order'),('is_confirmed','=',False),                                                                             ('user_id.login','=',user_info['login'])]) 
                
                notes = request.env['sale.order'].search([('state','!=','note_order'),('user_id.login','=',user_info['login'])])
                
                requests = request.env['sale.order.line'].search([('to_request','=',True),                                                                      ('order_id.user_id.login','=',user_info['login'])])
                
                result = {'draft_draft':[],'notes':[],'requests':[]}
                
                for req in requests:
                    sale = request.env['sale.order'].search([('id','=',req.order_id.id)])
                    result['requests'].append({
                        'date':sale.date_order,
                        'order_id':req.id,
                        'customer_name':sale.partner_id.name,
                        'state':sale.state,
                        'amount':req.price_subtotal
                    })
                
                for note in notes:
                    result['notes'].append({
                        'date':note.date_order,
                        'order_id':note.id,
                        'customer_name':note.partner_id.name,
                        'state':note.state,
                        'amount':note.amount_total
                    })
                
                for draft in drafts:
                    result['draft_draft'].append({
                        'date':draft.date_order,
                        'order_id':draft.id,
                        'customer_name':draft.partner_id.name,
                        'state':draft.state,
                        'amount':draft.amount_total
                    })                    
                return result
         
         except AccessError:
            return 'You are not allowed to do this'
        
     
     @http.route('/order_details',type='json',auth='none',cors='*')
     def order_details(self,order_id,DevToken,UserToken,base_location=None):
        try:
            if self.authrize_developer(DevToken) == False:
                return {'error':'developer token expired'}
            elif not self.authrize_user(UserToken):
                return {'error':'invalid user token'}
            else:
                user_info = self.authrize_user(UserToken)
                request.session.authenticate(self.db,user_info['login'],user_info['password'])
                sale = request.env['sale.order'].search([('id','=',int(order_id))])
                customer = sale.partner_id
                products = []
                for line in sale.order_line:
                    product = line.product_id
                    products.append({
                        'order_line_id':line.id,
                        'product_id':product.id,
                        'product_name':product.name,
                        'product_price':line.price_unit,
                        'product_code':product.barcode,
                        'product_qty':line.product_uom_qty,
                    })
                return {
                    'customer_name':customer.name,
                    'mobile':customer.mobile or customer.phone,
                    'email':customer.email or '',
                    'customer_id':customer.id,
                    'order_id':sale.id,
                    'draft_name':sale.name,
                    'amount':sale.amount_total,
                    'products':products
                }
        
        except AccessError:
            return 'You are not allowed to do this'        
     

