from odoo import http
from odoo.http import request
import json

class UserRestAPI(http.Controller):
    end_point_url = "/csolve_create_user"
    
    @http.route(end_point_url, type='json', auth='public',
                methods=['POST'], csrf=False, save_session=False)
    def csolve_user_controller(self, **kw):
        try:
            # Parse incoming JSON data
            data = json.loads(request.httprequest.data)
            print("Incoming data:", data)

            # Extract required fields from the data
            name = data.get("name")
            login = data.get("login")
            password = data.get("password")
            email = data.get("email")

            if not all([name, login, password, email]):
                return {"error": "Missing required fields: name, login, password, or email"}

            # Check if a user with the same login already exists
            existing_user = request.env['res.users'].sudo().search([('login', '=', login)], limit=1)
            if existing_user:
                return {"error": f"User with login '{login}' already exists."}

            # Get the Portal group
            portal_group = request.env.ref('base.group_portal', raise_if_not_found=False)
            if not portal_group:
                return {"error": "Portal group not found in the system."}

            # Create the user with Portal group assigned
            new_user = request.env['res.users'].sudo().create({
                'name': name,
                'login': login,
                'password': password,
                'email': email,
                'groups_id': [(6, 0, [portal_group.id])]  # Assign the Portal group
            })

            return {
                "success": True,
                "message": f"User '{name}' created successfully.",
                "user_id": new_user.id
            }

        except Exception as e:
            return {"error": str(e)}
        

    @http.route("/send_invite_course", type='json', auth='public',
                methods=['POST'], csrf=False, save_session=False)
    def send_course_invite(self,**kw):
        for i in range(10):
            print(i)
        vals={
            "partner_ids":[41],
            "channel_id":1,
            "send_email":True
        }
        x=request.env["slide.channel.invite"].sudo().create(vals)
        x.sudo().action_invite()
        return 0
