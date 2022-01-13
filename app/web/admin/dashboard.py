from app.web.admin import admin


@admin.get('/dashboard')
def dashboard():
    return 'admin dashboard'
