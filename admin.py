from flask import render_template, request, redirect, url_for, flash, session
from werkzeug.security import check_password_hash, generate_password_hash
from app import app, db
from models import User, Order, Feedback
from data_store import get_service_by_id, get_plan_by_id
from datetime import datetime, timedelta
import functools

def admin_required(f):
    """Decorator to require admin authentication"""
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Simple admin authentication (in production, use proper user management)
        if username == 'admin' and password == 'admin123':
            session['admin_logged_in'] = True
            session['admin_username'] = username
            flash('Đăng nhập thành công!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Tên đăng nhập hoặc mật khẩu không đúng!', 'error')
    
    return render_template('admin/login.html')

@app.route('/admin/logout')
def admin_logout():
    """Admin logout"""
    session.pop('admin_logged_in', None)
    session.pop('admin_username', None)
    flash('Đã đăng xuất thành công!', 'success')
    return redirect(url_for('admin_login'))

@app.route('/admin')
@app.route('/admin/dashboard')
@admin_required
def admin_dashboard():
    """Admin dashboard with KPIs"""
    
    # Calculate date ranges
    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    last_week = today - timedelta(days=7)
    last_month = today - timedelta(days=30)
    
    # Get statistics
    stats = {
        'total_orders': Order.query.count(),
        'orders_today': Order.query.filter(Order.created_at >= today).count(),
        'orders_yesterday': Order.query.filter(
            Order.created_at >= yesterday,
            Order.created_at < today
        ).count(),
        'orders_week': Order.query.filter(Order.created_at >= last_week).count(),
        'orders_month': Order.query.filter(Order.created_at >= last_month).count(),
        'pending_orders': Order.query.filter_by(status='pending').count(),
        'in_progress_orders': Order.query.filter_by(status='in_progress').count(),
        'completed_orders': Order.query.filter_by(status='completed').count(),
        'total_feedbacks': Feedback.query.count(),
        'new_feedbacks': Feedback.query.filter_by(status='new').count(),
        'total_revenue': db.session.query(db.func.sum(Order.total_amount)).scalar() or 0,
        'revenue_month': db.session.query(db.func.sum(Order.total_amount)).filter(
            Order.created_at >= last_month
        ).scalar() or 0
    }
    
    # Calculate conversion rate
    stats['conversion_rate'] = (
        (stats['completed_orders'] / stats['total_orders'] * 100) 
        if stats['total_orders'] > 0 else 0
    )
    
    # Get recent orders
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
    
    # Get recent feedbacks
    recent_feedbacks = Feedback.query.order_by(Feedback.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html',
                         stats=stats,
                         recent_orders=recent_orders,
                         recent_feedbacks=recent_feedbacks)

@app.route('/admin/orders')
@admin_required
def admin_orders():
    """Admin orders management"""
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', 'all')
    search = request.args.get('search', '')
    
    # Build query
    query = Order.query
    
    if status_filter != 'all':
        query = query.filter(Order.status == status_filter)
    
    if search:
        query = query.filter(
            db.or_(
                Order.customer_name.ilike(f'%{search}%'),
                Order.customer_email.ilike(f'%{search}%'),
                Order.service_type.ilike(f'%{search}%')
            )
        )
    
    # Paginate results
    orders = query.order_by(Order.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    # Get service and plan names for each order
    for order in orders.items:
        order.service_name = get_service_by_id(order.service_type)
        order.plan_name = get_plan_by_id(order.plan_type)
    
    return render_template('admin/orders.html',
                         orders=orders,
                         status_filter=status_filter,
                         search=search)

@app.route('/admin/orders/<int:order_id>/status', methods=['POST'])
@admin_required
def update_order_status(order_id):
    """Update order status"""
    order = Order.query.get_or_404(order_id)
    new_status = request.form.get('status')
    
    if new_status in ['pending', 'in_progress', 'completed']:
        order.status = new_status
        order.updated_at = datetime.utcnow()
        
        try:
            db.session.commit()
            flash(f'Đã cập nhật trạng thái đơn hàng #{order.id}', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Có lỗi xảy ra khi cập nhật trạng thái', 'error')
    
    return redirect(url_for('admin_orders'))

@app.route('/admin/feedbacks')
@admin_required
def admin_feedbacks():
    """Admin feedbacks management"""
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status', 'all')
    search = request.args.get('search', '')
    
    # Build query
    query = Feedback.query
    
    if status_filter != 'all':
        query = query.filter(Feedback.status == status_filter)
    
    if search:
        query = query.filter(
            db.or_(
                Feedback.name.ilike(f'%{search}%'),
                Feedback.email.ilike(f'%{search}%'),
                Feedback.subject.ilike(f'%{search}%'),
                Feedback.message.ilike(f'%{search}%')
            )
        )
    
    # Paginate results
    feedbacks = query.order_by(Feedback.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False
    )
    
    return render_template('admin/feedbacks.html',
                         feedbacks=feedbacks,
                         status_filter=status_filter,
                         search=search)

@app.route('/admin/feedbacks/<int:feedback_id>/status', methods=['POST'])
@admin_required
def update_feedback_status(feedback_id):
    """Update feedback status"""
    feedback = Feedback.query.get_or_404(feedback_id)
    new_status = request.form.get('status')
    
    if new_status in ['new', 'processed']:
        feedback.status = new_status
        
        try:
            db.session.commit()
            flash(f'Đã cập nhật trạng thái phản hồi #{feedback.id}', 'success')
        except Exception as e:
            db.session.rollback()
            flash('Có lỗi xảy ra khi cập nhật trạng thái', 'error')
    
    return redirect(url_for('admin_feedbacks'))

@app.route('/admin/orders/<int:order_id>')
@admin_required
def admin_order_detail(order_id):
    """Admin order detail view"""
    order = Order.query.get_or_404(order_id)
    service = get_service_by_id(order.service_type)
    plan = get_plan_by_id(order.plan_type)
    
    return render_template('admin/order_detail.html',
                         order=order,
                         service=service,
                         plan=plan)

@app.route('/admin/feedbacks/<int:feedback_id>')
@admin_required
def admin_feedback_detail(feedback_id):
    """Admin feedback detail view"""
    feedback = Feedback.query.get_or_404(feedback_id)
    
    return render_template('admin/feedback_detail.html',
                         feedback=feedback)
