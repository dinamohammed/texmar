from odoo import http,fields,models
from odoo.http import request,Response,JsonRequest
from odoo.exceptions import ValidationError,AccessError,AccessDenied
from datetime import datetime,timedelta,timezone
from werkzeug.wrappers import AcceptMixin, BaseRequest
import time
import io
import base64
import jwt
from . import controllers

class security(controllers.Restapi):
    
     @http.route('/forget_password',type='json',auth='none',cors='*')
     def forget_password(self,email,base_location=None):
        dev_token = request.httprequest.headers['DevToken']
        try:
            if self.authrize_developer(dev_token) == False:
                return {'error':'developer token expired'}
            else:
                user = request.env['res.users'].sudo().search([('login','=',email)],limit=1)
                user.sudo().action_reset_password()
                return 'resend a reset password to user mail' if user else 'no user found'
        except AccessError:
            return {'error':'You are not allowed to do this'}
        except:
            return {'error':'unexcepcted error occured'}
        
    
     @http.route('/create_dev_token',type='json',auth='none',cors='*')
     def create_dev_token(self,login,password,**kw): 
        try:
            request.session.authenticate(self.db,login,password)
            exp_time = datetime.utcnow() + timedelta(days=7)
            token = jwt.encode({'exp':exp_time}, self.secret, algorithm=self.algorithm)
            request.env['restapi.tokens'].create({'name':token})
            return token
        except AccessError:
            return {'error':'You are not allowed to do this'}
        except AccessDenied:
            return {'error':'wrong user name or password'}
            
     
     @http.route('/login',type='json',auth='none',cors='*')
     def login(self,login,password,headers = None,base_location=None):
        dev_token = request.httprequest.headers['DevToken']
        try:
            if self.authrize_developer(dev_token) == False:
                return {'error':'developer token expired'}
            else:
                request.session.authenticate(self.db,login,password)
                user = request.env['res.users'].sudo().search([('login','=',login)])
                token = jwt.encode({'user_id':user.id,'login':login,'password':password}, self.secret, algorithm=self.algorithm)
                request.env['restapi.user.tokens'].sudo().create({
                    'name':token,
                    'user_id':user.id
                })

                return token
        except AccessError:
            return {'error':'You are not allowed to do this'}
        except AccessDenied:
            return {'error':'wrong user name or password'}
        
        
    
