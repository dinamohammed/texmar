from odoo import http,fields,models
from odoo.http import request,Response,JsonRequest
from odoo.exceptions import ValidationError,AccessError
import io
import base64
from . import controllers
class reporting(controllers.Restapi): 
    
     @http.route('/sales_home',type='json',auth='none',cors='*')
     def sales_home(self,DevToken,UserToken,base_location=None):
        result = []
        try:
            if self.authrize_developer(DevToken) == False:
                return {'error':'developer token expired'}
            elif not self.authrize_user(UserToken):
                return {'error':'invalid user token'}
            else:
                user_info = self.authrize_user(UserToken)
                request.session.authenticate(self.db,user_info['login'],user_info['password'])
                allowed_companies = self.prepare_allowed_companies(user_info['login'])
                sales = request.env['sale.order'].search([('company_id','in',allowed_companies),                                                                                       ('user_id.login','=',user_info['login']),('state','!=','note_order'),                                                               ('due_amount','=',0)])
                drafts = request.env['sale.order'].search([('state','=','note_order'),('is_confirmed','=',False),                                   ('user_id.login','=',user_info['login'])]) 
                drafts_arr = []
                for draft in drafts:
                    drafts_arr.append({
                        'order_id':draft.id,
                        'date':draft.date_order,
                        'customer_name':draft.partner_id.name,
                        'state':draft.state,
                        'amount':draft.amount_total
                    })
                    

                #dates
                day = fields.date.today().day 
                month = fields.date.today().month
                year = fields.date.today().year
                #filtering sale depending on date
                sales_today = [sale for sale in sales if sale.date_order.day == day and sale.date_order.month == month and sale.date_order.year == year]                                                        
                sales_yesterday = [sale for sale in sales if sale.date_order.day == day - 1 and sale.date_order.month == month and sale.date_order.year == year]  
                # getting the sum of all sales
                sales_today_sum = self.get_total_sales(sales_today)
                sales_yesterday_sum = self.get_total_sales(sales_yesterday)

                # calculating the percentage
                perc = self.get_percentage(sales_yesterday_sum,sales_today_sum) if sales_today_sum > 1 else -100 #abbas
                
                return {
                    'today_sales_amount':sales_today_sum,
                    'today_sales_percentage':float("{0:.1f}".format(perc)),
                    'draft_notes':drafts_arr
                }
        except AccessError:
            return {'error':'You are not allowed to do this'}
        
    
     def get_salesman_target_history(self,login,sales_sum,sales):
        sales_teams = request.env['crm.team'].search([])
        #geting target
        sales_team_target = 0
        for sales_team in sales_teams:
            logins = [member.login for member in sales_team.member_ids]
            if login in logins:
                sales_team_target += sales_team.invoiced_target
                
        target = {
            'date':fields.date.today(),
            'sales_amount':sales_sum,
            'sales_percentage':float("{0:.2f}".format((sales_sum/sales_team_target)*100)),
            'target_amount':sales_team_target
        }
        
        #getting history
        history = []
        for sale in sales:
            history.append({
                'date':sale.date_order,
                'sales_amount':sale.amount_total
            })
            
        
        return {'target':target,'history':history}

        
        
        
            
        
     
        
     @http.route('/sales_dashboard',type='json',auth='none',cors='*')
     def sales_dashboard(self,DevToken,UserToken,base_location=None):
        result = []
        try:
            if self.authrize_developer(DevToken) == False:
                return {'error':'developer token expired'}
            elif not self.authrize_user(UserToken):
                return {'error':'invalid user token'}
            else:
                user_info = self.authrize_user(UserToken)
                request.session.authenticate(self.db,user_info['login'],user_info['password'])
                allowed_companies = self.prepare_allowed_companies(user_info['login'])
                sales = request.env['sale.order'].search([('company_id','in',allowed_companies),('due_amount','=',0),                                       ('user_id.login','=',user_info['login']),('state','!=','note_order')])

                #dates
                day = fields.date.today().day 
                month = fields.date.today().month
                year = fields.date.today().year
                
                #filtering sale depending on date
                sales_today = [sale for sale in sales if sale.date_order.day == day and sale.date_order.month == month and sale.date_order.year == year]                                                        
                sales_yesterday = [sale for sale in sales if sale.date_order.day == day - 1 and sale.date_order.month == month and sale.date_order.year == year]                                                          
                sales_this_month = [sale for sale in sales if sale.date_order.month == month and sale.date_order.year == year]                                                                                                                                             
                sales_last_month = [sale for sale in sales if sale.date_order.month == month - 1 and sale.date_order.year == year]                                                                           

                # getting the sum of all sales
                sales_today_sum = self.get_total_sales(sales_today)
                sales_yesterday_sum = self.get_total_sales(sales_yesterday)
                sales_this_month_sum = self.get_total_sales(sales_this_month)
                sales_last_month_sum = self.get_total_sales(sales_last_month)

                # calculating the percentage
                daily_perc = self.get_percentage(sales_yesterday_sum,sales_today_sum) if sales_today_sum > 1 else -100
                monthly_perc = self.get_percentage(sales_last_month_sum,sales_this_month_sum) if sales_this_month_sum > 1 else -100

                salesman = self.get_salesman_target_history(user_info['login'],sales_this_month_sum,sales_this_month)
                return {'sales' : [
                            {'period' : 'daily' , 'amount': sales_today_sum , 'percentage' : float("{0:.1f}".format(daily_perc))},
                            {'period' : 'monthly' , 'amount': sales_this_month_sum , 'percentage' :float("{0:.1f}".format(monthly_perc))},
                            ],
                                    'target' :salesman['target'],
                                    'history' :salesman['history'],
                        }
        except AccessError:
            return 'You are not allowed to do this'