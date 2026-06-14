# gui/utils/navigation.py
from gui.components.sidebar import sidebar

def render_role_sidebar(current_frame, current_user, active_title="Home"):
    master = current_frame.master  

    def go_home():
        from gui.frames.home import HomeFrame
        master.switch_frame(HomeFrame, current_user=current_user)

    def go_saved_post():
        from gui.frames.saved_post import SavedPostFrame
        master.switch_frame(SavedPostFrame, current_user=current_user)
         
    def go_comunity():
        from gui.frames.comunity import ComunityFrame
        master.switch_frame(ComunityFrame, current_user=current_user)
        
    def go_notification():
        from gui.frames.notification import NotificationFrame
        master.switch_frame(NotificationFrame, current_user=current_user)

    def go_dashboard_moderator():
        from gui.frames.moderator.dashboard_moderator import DashboardModeratorFrame    
        master.switch_frame(DashboardModeratorFrame , current_user=current_user)
        
    def go_dashboard_admin():
        from gui.frames.admin.dashboard_admin import DashboardAdminFrame
        master.switch_frame(DashboardAdminFrame, current_user=current_user)
            
    def go_user_management():
        from gui.frames.admin.user_management import UserManagementFrame
        master.switch_frame(UserManagementFrame, current_user=current_user)     

    def go_comunity_management():
        from gui.frames.moderator.comunity_management import CommunityManagementFrame
        master.switch_frame(CommunityManagementFrame, current_user=current_user)      

    def go_badword_management():
        from gui.frames.moderator.badword_management import BadwordManagementFrame
        master.switch_frame(BadwordManagementFrame, current_user=current_user)           

    nav_items = [
        {"title": "Home", "comand": go_home, "active": active_title == "Home"},
        {"title": "Saved Post", "comand": go_saved_post, "active": active_title == "Saved_Post"},
        {"title": "Comunity", "comand": go_comunity, "active": active_title == "Comunity"},
        {"title": "Notification", "comand": go_notification, "active": active_title == "Notification"}
    ]
    
    if current_user.role == "moderator":            
        nav_items.insert(0, {
            "title": "Badword Management", 
            "comand": go_badword_management, 
            "active": active_title == "Badword_Management"
        })
        nav_items.insert(0, {
            "title": "Comunity Management", 
            "comand": go_comunity_management, 
            "active": active_title == "Comunity_Management"
        })
        nav_items.insert(0, {
            "title": "Dashboard", 
            "comand": go_dashboard_moderator, 
            "active": active_title == "Dashboard_Moderator"
        })
    elif current_user.role == "admin":
        nav_items.insert(0, {
            "title": "Badword Management", 
            "comand": go_badword_management, 
            "active": active_title == "Badword_Management"
        })
        nav_items.insert(0, {
            "title": "Comunity Management", 
            "comand": go_comunity_management, 
            "active": active_title == "Comunity_Management"
        })
        nav_items.insert(0, {
            "title": "User Management", 
            "comand": go_user_management, 
            "active": active_title == "User_Management"
        })
        nav_items.insert(0, {
            "title": "Dashboard", 
            "comand": go_dashboard_admin, 
            "active": active_title == "Dashboard_Admin"
        },)   
       
       

    sidebar(current_frame, current_user, nav_items)