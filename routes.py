from flask import render_template, request, redirect, url_for, flash, session, jsonify
from app import app, db
from models import Order, Feedback, BlogPost, User
from data_store import get_services, get_pricing_plans, get_faq_data, get_blog_posts, get_stats
from werkzeug.security import generate_password_hash
import hashlib
import json
from datetime import datetime

# Language handling
@app.context_processor
def inject_language():
    return {'current_lang': session.get('language', 'vi')}

@app.route('/set_language/<language>')
def set_language(language):
    session['language'] = language
    return redirect(request.referrer or url_for('index'))

# Public routes
@app.route('/')
def index():
    """Homepage with hero section, stats, and video demo"""
    stats = get_stats()
    return render_template('index.html', stats=stats)

@app.route('/about')
def about():
    """About page with timeline and team gallery"""
    return render_template('about.html')

@app.route('/services')
def services():
    """Services page with flip-card grid"""
    services_data = get_services()
    filter_type = request.args.get('filter', 'all')
    return render_template('services.html', services=services_data, filter_type=filter_type)

@app.route('/pricing')
def pricing():
    """Pricing page with plan comparison"""
    plans = get_pricing_plans()
    return render_template('pricing.html', plans=plans)

@app.route('/order', methods=['GET', 'POST'])
def order():
    """3-step order form"""
    if request.method == 'POST':
        # Process order form
        step = request.form.get('step', '1')
        
        if step == '3':  # Final submission
            # Create order
            order = Order(
                customer_name=request.form.get('customer_name'),
                customer_email=request.form.get('customer_email'),
                customer_phone=request.form.get('customer_phone'),
                service_type=request.form.get('service_type'),
                plan_type=request.form.get('plan_type'),
                description=request.form.get('description'),
                total_amount=float(request.form.get('total_amount', 0))
            )
            
            db.session.add(order)
            db.session.commit()
            
            # Mock blockchain transaction
            order_data = {
                'id': order.id,
                'customer': order.customer_name,
                'service': order.service_type,
                'plan': order.plan_type,
                'timestamp': order.created_at.isoformat()
            }
            order_hash = hashlib.sha256(json.dumps(order_data, sort_keys=True).encode()).hexdigest()
            
            # Mock transaction hash (in real implementation, this would be from blockchain)
            tx_hash = f"0x{hashlib.sha256(f'{order.id}{datetime.now()}'.encode()).hexdigest()}"
            order.tx_hash = tx_hash
            db.session.commit()
            
            flash('Đơn hàng đã được tạo thành công! Mã giao dịch: ' + tx_hash, 'success')
            return redirect(url_for('verify_order', tx_hash=tx_hash))
    
    services_data = get_services()
    plans = get_pricing_plans()
    return render_template('order.html', services=services_data, plans=plans)

@app.route('/verify/<tx_hash>')
def verify_order(tx_hash):
    """Order verification page"""
    order = Order.query.filter_by(tx_hash=tx_hash).first()
    if not order:
        flash('Không tìm thấy đơn hàng với mã giao dịch này.', 'error')
        return redirect(url_for('index'))
    
    return render_template('verify.html', order=order)

@app.route('/faq')
def faq():
    """FAQ page with accordion"""
    faq_data = get_faq_data()
    return render_template('faq.html', faqs=faq_data)

@app.route('/blog')
def blog():
    """Blog listing page"""
    posts = get_blog_posts()
    return render_template('blog.html', posts=posts)

@app.route('/blog/<slug>')
def blog_post(slug):
    """Individual blog post page"""
    post = BlogPost.query.filter_by(slug=slug, published=True).first_or_404()
    return render_template('blog_post.html', post=post)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
    """Contact page with feedback form"""
    if request.method == 'POST':
        feedback = Feedback(
            name=request.form.get('name'),
            email=request.form.get('email'),
            subject=request.form.get('subject'),
            message=request.form.get('message')
        )
        db.session.add(feedback)
        db.session.commit()
        
        flash('Cảm ơn bạn đã gửi phản hồi! Chúng tôi sẽ liên hệ lại sớm.', 'success')
        return redirect(url_for('contact'))
    
    return render_template('contact.html')

# Admin routes
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    """Admin login page"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Simple admin check (in production, use proper authentication)
        if username == 'admin' and password == 'admin123':
            session['admin_logged_in'] = True
            flash('Đăng nhập thành công!', 'success')
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Tên đăng nhập hoặc mật khẩu không đúng.', 'error')
    
    return render_template('admin/login.html')

@app.route('/admin/logout')
def admin_logout():
    """Admin logout"""
    session.pop('admin_logged_in', None)
    flash('Đã đăng xuất thành công.', 'info')
    return redirect(url_for('index'))

def admin_required(f):
    """Decorator to require admin login"""
    def decorated_function(*args, **kwargs):
        if not session.get('admin_logged_in'):
            flash('Vui lòng đăng nhập để truy cập trang quản trị.', 'error')
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@app.route('/admin')
@admin_required
def admin_dashboard():
    """Admin dashboard with KPIs"""
    stats = get_stats()
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(5).all()
    recent_feedbacks = Feedback.query.order_by(Feedback.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html', 
                         stats=stats, 
                         recent_orders=recent_orders, 
                         recent_feedbacks=recent_feedbacks)

@app.route('/admin/orders')
@admin_required
def admin_orders():
    """Admin orders management"""
    status_filter = request.args.get('status', 'all')
    page = request.args.get('page', 1, type=int)
    
    query = Order.query
    if status_filter != 'all':
        query = query.filter_by(status=status_filter)
    
    orders = query.order_by(Order.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False)
    
    return render_template('admin/orders.html', orders=orders, status_filter=status_filter)

@app.route('/admin/orders/<int:order_id>/update_status', methods=['POST'])
@admin_required
def update_order_status(order_id):
    """Update order status"""
    order = Order.query.get_or_404(order_id)
    new_status = request.form.get('status')
    
    if new_status in ['pending', 'in_progress', 'completed']:
        order.status = new_status
        order.updated_at = datetime.utcnow()
        db.session.commit()
        flash(f'Đã cập nhật trạng thái đơn hàng #{order.id}', 'success')
    
    return redirect(url_for('admin_orders'))

@app.route('/admin/feedbacks')
@admin_required
def admin_feedbacks():
    """Admin feedbacks management"""
    page = request.args.get('page', 1, type=int)
    feedbacks = Feedback.query.order_by(Feedback.created_at.desc()).paginate(
        page=page, per_page=20, error_out=False)
    
    return render_template('admin/feedbacks.html', feedbacks=feedbacks)

@app.route('/admin/feedbacks/<int:feedback_id>/process', methods=['POST'])
@admin_required
def process_feedback(feedback_id):
    """Mark feedback as processed"""
    feedback = Feedback.query.get_or_404(feedback_id)
    feedback.is_processed = True
    db.session.commit()
    
    flash(f'Đã đánh dấu phản hồi #{feedback.id} đã xử lý', 'success')
    return redirect(url_for('admin_feedbacks'))

# Search functionality
@app.route('/search')
def search():
    """Search functionality"""
    query = request.args.get('q', '')
    if not query:
        return redirect(url_for('index'))
    
    # Search in blog posts and services
    blog_results = BlogPost.query.filter(
        BlogPost.title.contains(query) | BlogPost.content.contains(query),
        BlogPost.published == True
    ).all()
    
    return render_template('search_results.html', 
                         query=query, 
                         blog_results=blog_results)

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html'), 500
