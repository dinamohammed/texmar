from odoo import http,fields,models
from odoo.http import request,Response,JsonRequest
from odoo.exceptions import ValidationError,AccessError,AccessDenied
import io
import base64
import jwt
import re
from datetime import datetime,timedelta,timezone
from . import controllers

class products(controllers.Restapi):
     @http.route('/scan_product',type='json',auth='none',cors='*')
     def scan_product(self,code,DevToken,UserToken,base_location=None):
        try:
            if self.authrize_developer(DevToken) == False:
                return {'error':'developer token expired'}
            elif not self.authrize_user(UserToken):
                return {'error':'invalid user token'}
            else:
                user_info = self.authrize_user(UserToken)
                request.session.authenticate(self.db,user_info['login'],user_info['password'])
                product = request.env['product.product'].search([('barcode','=',code)],limit=1)
                info = {
                    'name':product.name,
                    'code':product.barcode,
                    'price':product.list_price,
                    'description':product.description if product.description else '' ,
                    'stock_availability':product.virtual_available,
                    'product_id':product.id
                }
                return info if product else 'no product found'
        except AccessError:
            return {'error':'You are not allowed to do this'}

     
     @http.route('/popular_products',type='json',auth='none',cors='*')
     def popular_products(self,DevToken,UserToken,base_location=None):
        result = []
        try:
            if self.authrize_developer(DevToken) == False:
                return {'error':'developer token expired'}
            elif not self.authrize_user(UserToken):
                return {'error':'invalid user token'}
            else:
                params = self.get_params(request.httprequest.url)
                limit = params.get('limit',5)
                offset = params.get('offset',0)
                
                user_info = self.authrize_user(UserToken)
                request.session.authenticate(self.db,user_info['login'],user_info['password'])
                
                products = request.env['product.product'].search([('company_id','=',False)],limit=limit,offset=offset)
                
                for product in products:
                    result.append(self.product_info(product))
                    
                return result if len(result) > 0 else 'no products found'  
        except AccessError:
            return {'error':'You are not allowed to do this'}
        except AccessDenied:
            return {'error':'You are not allowed to do this'}
            
     
     @http.route('/new_products',type='json',auth='none',cors='*')
     def new_product(self,DevToken,UserToken,base_location=None):
        result = []
        try:
            if self.authrize_developer(DevToken) == False:
                return {'error':'developer token expired'}
            elif not self.authrize_user(UserToken):
                return {'error':'invalid user token'}
            else:
                params = self.get_params(request.httprequest.url)
                limit = params.get('limit',5)
                offset = params.get('offset',0)
                
                user_info = self.authrize_user(UserToken)
                request.session.authenticate(self.db,user_info['login'],user_info['password'])
                
                exp_time = datetime.utcnow() - timedelta(days=30)
                products = request.env['product.product'].search([('company_id','=',False),('create_date','>',exp_time)],limit=limit,offset=offset)
                
                for product in products:
                    result.append(self.product_info(product))
                    
                return result if len(result) > 0 else 'no products found'
            
        except AccessError:
            return {'error':'You are not allowed to do this'}
     
     
     
     @http.route('/search_products',type='json',auth='none',cors='*')
     def search_products(self,DevToken,UserToken,keyword,base_location=None):
        try:
            if self.authrize_developer(DevToken) == False:
                return {'error':'developer token expired'}
            elif not self.authrize_user(UserToken):
                return {'error':'invalid user token'}
            else:
                user_info = self.authrize_user(UserToken)
                request.session.authenticate(self.db,user_info['login'],user_info['password'])
                products = request.env['product.product'].search([('company_id','=',False)])
                result = []
                for product in products:
                    search = str(keyword).lower()
                    code = '' if not product.default_code else product.default_code.lower()
                    
                    if re.search(search,product.name.lower()) != None or                                                                                                      re.search(search,code) != None:
                        result.append(self.product_info(product))
                        
                return result if len(result) > 0 else 'no product found'
                    
                
        except AccessError:
            return {'error':'You are not allowed to do this'}