from flask import Blueprint, render_template, abort, flash, redirect, url_for
from flask_login import login_required, current_user

admin_bp = Blueprint("admin_bp", __name__)

@admin_bp.route("/admin")
@login_required
def admin():
    if current_user.is_anonymous:
        abort(403)
    
    if current_user.role != 'admin':
        flash('You have No access right to the Admin content.')
        return redirect(url_for("main_bp.index"))
        
    return render_template("admin/admin.html")