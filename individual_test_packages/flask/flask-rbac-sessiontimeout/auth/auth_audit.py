# login_audit.py

from datetime import datetime

def update_login_audit_info(user, ip_address):
    # Shift the current login information to the last login before updating
    user.last_login_at = user.current_login_at
    user.last_login_ip = user.current_login_ip

    # Update current login information
    user.current_login_at = datetime.now()
    user.current_login_ip = ip_address
    user.login_count += 1  # Increment the total login count
