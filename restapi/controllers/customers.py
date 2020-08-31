from odoo import http,fields,models
from odoo.http import request,Response,JsonRequest
from odoo.exceptions import ValidationError,AccessError,AccessDenied
import io
import base64
import jwt
import re
from datetime import datetime,timedelta,timezone
from . import controllers

class customers(controllers.Restapi):
     @http.route('/list_customers',type='json',auth='none',cors='*')
     def list_customers(self,DevToken,UserToken,base_location=None):
        result = []
        try:
            if self.authrize_developer(DevToken) == False:
                return {'error':'developer token expired'}
            elif not self.authrize_user(UserToken):
                return {'error':'invalid user token'}
            else:
                user_info = self.authrize_user(UserToken)
                request.session.authenticate(self.db,user_info['login'],user_info['password'])
                params = self.get_params(request.httprequest.url)
                limit = params.get('limit',5)
                offset = params.get('offset',0)
                customers = request.env['res.partner'].search([('customer_rank','=',True),('company_id','=',False)],limit=limit,offset=offset)
                for customer in customers:
                    vals = {
                        'customer_name':customer.name,
                        'mobile':customer.mobile,
                        'email':customer.email,
                        'customer_id':customer.id,
                        'history' : {}
                    }
                    result.append(vals)
                return result if len(result) > 0 else 'no customers found'
        except AccessError:
            return {'error':'You are not allowed to do this'}  
    
    
    
     @http.route('/customers_search',type='json',auth='none',cors='*')                                                               
     def search_products(self,DevToken,UserToken,keyword,base_location=None):
        try:
            if self.authrize_developer(DevToken) == False:
                return {'error':'developer token expired'}
            elif not self.authrize_user(UserToken):
                return {'error':'invalid user token'}
            else:
                user_info = self.authrize_user(UserToken)
                request.session.authenticate(self.db,user_info['login'],user_info['password'])
                customers = request.env['res.partner'].search([('company_id','=',False),('customer_rank','=',True)])
                result = []
                for customer in customers:
                    search = str(keyword).lower()
                    if re.search(search,customer.name.lower()) != None or customer.mobile == keyword or customer.phone == keyword:   
                        result.append({
                        'customer_name':customer.name,
                        'mobile':customer.mobile,
                        'email':customer.email,
                        'customer_id':customer.id,
                        'history' : {}
                        })     
                return result if len(result) > 0 else 'no customers found'
                    
                
        except AccessError:
            return {'error':'You are not allowed to do this'}
        
        
    
    
     @http.route('/edit_customer',type='json',auth='none',cors='*')
     def edit_customer(self,customer_id,full_name,country_code,mobile,email,DevToken,UserToken,base_location=None):
        try:
            if self.authrize_developer(DevToken) == False:
                return {'error':'developer token expired'}     
            elif not self.authrize_user(UserToken):
                return {'error':'invalid user token'}
            else:
                user_info = self.authrize_user(UserToken)
                request.session.authenticate(self.db,user_info['login'],user_info['password'])
                country = request.env['res.country'].search([('code','=',country_code.upper())],limit=1).id
                if not country:
                    return 'invalid country code'
                customer = request.env['res.partner'].search([('id','=',customer_id)],limit=1)
                if not customer:
                    return 'customer not found'
                vals = {
                    'name':full_name,
                    'phone':mobile,
                    'mobile':mobile,
                    'email':email,
                    'country_id':country,
                }
                customer.write(vals)
                return 'edited successfully'
        
        except AccessError:
            return {'error':'You are not allowed to do this'}
        
        except ValidationError as e:
            return {'error':e.name}
     
     @http.route('/create_customer',type='json',auth='none',cors='*')
     def create_customer(self,email,full_name,country_code,mobile,DevToken,UserToken,base_location=None):
        try:
            if self.authrize_developer(DevToken) == False:
                return {'error':'developer token expired'}
            elif not self.authrize_user(UserToken):
                return {'error':'invalid user token'}
            else:
                user_info = self.authrize_user(UserToken)
                request.session.authenticate(self.db,user_info['login'],user_info['password'])
                country = request.env['res.country'].search([('code','=',country_code.upper())],limit=1).id
                if not country:
                    return 'invalid country code'
                vals = {
                    'name':full_name,
                    'mobile':mobile,
                    'email':email,
                    'country_id':country,
                    'customer_rank':True
                }
                request.env['res.partner'].create(vals)
                return 'created successfully '
            
        except AccessError:
            return {'error':'You are not allowed to do this'}
        
        except ValidationError as e:
            return {'error':e.name}