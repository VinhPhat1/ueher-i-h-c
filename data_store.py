"""
In-memory data store for UEHer application
Contains static data and mock functions for services, pricing, FAQ, etc.
"""

from datetime import datetime, timedelta
from models import Order, Feedback, BlogPost

def get_services():
    """Get available services data"""
    return [
        {
            'id': 'schedule',
            'name': 'Xếp lịch học tập',
            'name_en': 'Schedule Management',
            'icon': 'calendar',
            'description': 'Tự động sắp xếp lịch học, thi và deadline một cách khoa học.',
            'description_en': 'Automatically organize study schedules, exams and deadlines scientifically.',
            'features': ['Đồng bộ Google Calendar', 'Nhắc nhở thông minh', 'Phân tích thời gian'],
            'features_en': ['Google Calendar sync', 'Smart reminders', 'Time analysis'],
            'category': 'productivity'
        },
        {
            'id': 'memes',
            'name': 'Meme Pack',
            'name_en': 'Meme Pack',
            'icon': 'smile',
            'description': 'Bộ sưu tập meme độc quyền cho sinh viên UEH để giải stress.',
            'description_en': 'Exclusive meme collection for UEH students to relieve stress.',
            'features': ['Meme mới hàng tuần', 'Tùy chỉnh theo ngành', 'Chia sẻ dễ dàng'],
            'features_en': ['Weekly new memes', 'Major-specific content', 'Easy sharing'],
            'category': 'entertainment'
        },
        {
            'id': 'documents',
            'name': 'Tài liệu học tập',
            'name_en': 'Study Materials',
            'icon': 'book',
            'description': 'Thư viện tài liệu chất lượng cao được biên soạn bởi các anh chị khóa trước.',
            'description_en': 'High-quality document library compiled by senior students.',
            'features': ['Đáp án chi tiết', 'Video giải thích', 'Cập nhật liên tục'],
            'features_en': ['Detailed answers', 'Explanation videos', 'Regular updates'],
            'category': 'education'
        },
        {
            'id': 'other',
            'name': 'Dịch vụ khác',
            'name_en': 'Other Services',
            'icon': 'settings',
            'description': 'Các dịch vụ hỗ trợ khác như tư vấn học tập, làm CV, tìm việc.',
            'description_en': 'Other support services like academic consulting, CV creation, job hunting.',
            'features': ['Tư vấn 1-1', 'Mẫu CV chuyên nghiệp', 'Kết nối việc làm'],
            'features_en': ['1-on-1 consultation', 'Professional CV templates', 'Job connections'],
            'category': 'support'
        }
    ]

def get_pricing_plans():
    """Get pricing plans data"""
    return [
        {
            'id': 'free',
            'name': 'Free',
            'name_vi': 'Miễn phí',
            'price_monthly': 0,
            'price_yearly': 0,
            'features': [
                'Xếp lịch cơ bản',
                '5 meme/tuần',
                'Tài liệu giới hạn',
                'Hỗ trợ email'
            ],
            'features_en': [
                'Basic scheduling',
                '5 memes/week',
                'Limited documents',
                'Email support'
            ],
            'popular': False,
            'cta': 'Bắt đầu miễn phí',
            'cta_en': 'Start Free'
        },
        {
            'id': 'basic',
            'name': 'Basic',
            'name_vi': 'Cơ bản',
            'price_monthly': 99000,
            'price_yearly': 990000,
            'features': [
                'Xếp lịch thông minh',
                'Meme không giới hạn',
                'Tài liệu đầy đủ',
                'Hỗ trợ chat',
                'Đồng bộ Google Calendar'
            ],
            'features_en': [
                'Smart scheduling',
                'Unlimited memes',
                'Full documents',
                'Chat support',
                'Google Calendar sync'
            ],
            'popular': True,
            'cta': 'Chọn gói Basic',
            'cta_en': 'Choose Basic'
        },
        {
            'id': 'pro',
            'name': 'Pro',
            'name_vi': 'Chuyên nghiệp',
            'price_monthly': 199000,
            'price_yearly': 1990000,
            'features': [
                'Tất cả tính năng Basic',
                'AI phân tích học tập',
                'Tư vấn 1-1',
                'Mẫu CV premium',
                'Ưu tiên hỗ trợ'
            ],
            'features_en': [
                'All Basic features',
                'AI study analysis',
                '1-on-1 consultation',
                'Premium CV templates',
                'Priority support'
            ],
            'popular': False,
            'cta': 'Chọn gói Pro',
            'cta_en': 'Choose Pro'
        },
        {
            'id': 'team',
            'name': 'Team',
            'name_vi': 'Nhóm',
            'price_monthly': 499000,
            'price_yearly': 4990000,
            'features': [
                'Tất cả tính năng Pro',
                'Quản lý nhóm học tập',
                'Dashboard thống kê',
                'API tích hợp',
                'Hỗ trợ 24/7'
            ],
            'features_en': [
                'All Pro features',
                'Study group management',
                'Analytics dashboard',
                'API integration',
                '24/7 support'
            ],
            'popular': False,
            'cta': 'Liên hệ tư vấn',
            'cta_en': 'Contact Sales'
        }
    ]

def get_faq_data():
    """Get FAQ data"""
    return [
        {
            'question': 'UEHer đi học là gì?',
            'question_en': 'What is UEHer Study?',
            'answer': 'UEHer đi học là nền tảng hỗ trợ sinh viên UEH tự động hóa việc học tập, quản lý thời gian và giải stress thông qua các dịch vụ thông minh.',
            'answer_en': 'UEHer Study is a platform that helps UEH students automate learning, manage time, and relieve stress through smart services.'
        },
        {
            'question': 'Làm sao để đăng ký dịch vụ?',
            'question_en': 'How to register for services?',
            'answer': 'Bạn có thể đăng ký qua trang Order, chọn gói phù hợp và điền thông tin. Chúng tôi sẽ liên hệ lại trong 24h.',
            'answer_en': 'You can register through the Order page, choose a suitable plan and fill in information. We will contact you within 24 hours.'
        },
        {
            'question': 'Có miễn phí không?',
            'question_en': 'Is it free?',
            'answer': 'Có! Chúng tôi có gói Free với các tính năng cơ bản. Bạn có thể nâng cấp lên các gói trả phí để có thêm nhiều tính năng.',
            'answer_en': 'Yes! We have a Free plan with basic features. You can upgrade to paid plans for more features.'
        },
        {
            'question': 'Tài liệu có được cập nhật không?',
            'question_en': 'Are documents updated?',
            'answer': 'Tài liệu được cập nhật liên tục theo chương trình học mới nhất của UEH và góp ý từ sinh viên.',
            'answer_en': 'Documents are continuously updated according to UEH\'s latest curriculum and student feedback.'
        },
        {
            'question': 'Có hỗ trợ các ngành khác ngoài UEH không?',
            'question_en': 'Do you support majors outside UEH?',
            'answer': 'Hiện tại chúng tôi chỉ tập trung vào sinh viên UEH, nhưng sẽ mở rộng ra các trường khác trong tương lai.',
            'answer_en': 'Currently we only focus on UEH students, but will expand to other universities in the future.'
        },
        {
            'question': 'Làm sao để hủy đăng ký?',
            'question_en': 'How to cancel subscription?',
            'answer': 'Bạn có thể hủy đăng ký bất cứ lúc nào qua email hoặc liên hệ support. Không có phí hủy.',
            'answer_en': 'You can cancel anytime via email or contact support. No cancellation fees.'
        },
        {
            'question': 'Có bảo mật thông tin không?',
            'question_en': 'Is information secure?',
            'answer': 'Thông tin của bạn được bảo mật tuyệt đối và chỉ được sử dụng để cung cấp dịch vụ tốt nhất.',
            'answer_en': 'Your information is absolutely secure and only used to provide the best service.'
        },
        {
            'question': 'Có app mobile không?',
            'question_en': 'Is there a mobile app?',
            'answer': 'Website hiện tại đã tối ưu cho mobile. App mobile riêng đang trong kế hoạch phát triển.',
            'answer_en': 'The current website is mobile-optimized. A dedicated mobile app is in development.'
        },
        {
            'question': 'Thanh toán như thế nào?',
            'question_en': 'How to pay?',
            'answer': 'Chúng tôi hỗ trợ chuyển khoản ngân hàng, ví điện tử và thẻ tín dụng. Thanh toán an toàn 100%.',
            'answer_en': 'We support bank transfer, e-wallets and credit cards. 100% secure payment.'
        },
        {
            'question': 'Có chính sách hoàn tiền không?',
            'question_en': 'Is there a refund policy?',
            'answer': 'Có! Nếu không hài lòng trong 7 ngày đầu, chúng tôi sẽ hoàn tiền 100%.',
            'answer_en': 'Yes! If not satisfied within the first 7 days, we will refund 100%.'
        }
    ]

def get_blog_posts():
    """Get sample blog posts"""
    return [
        {
            'id': 1,
            'title': '5 Mẹo quản lý thời gian hiệu quả cho sinh viên UEH',
            'title_en': '5 Effective Time Management Tips for UEH Students',
            'slug': '5-meo-quan-ly-thoi-gian-hieu-qua',
            'excerpt': 'Khám phá những phương pháp đã được kiểm chứng giúp sinh viên UEH tối ưu hóa thời gian học tập và nghỉ ngơi.',
            'excerpt_en': 'Discover proven methods that help UEH students optimize study and rest time.',
            'author': 'UEHer Team',
            'created_at': datetime.now() - timedelta(days=2),
            'image': 'https://images.unsplash.com/photo-1434030216411-0b793f4b4173?w=800&h=400&fit=crop'
        },
        {
            'id': 2,
            'title': 'Cách sử dụng Google Calendar để không bao giờ quên deadline',
            'title_en': 'How to Use Google Calendar to Never Miss Deadlines',
            'slug': 'cach-su-dung-google-calendar',
            'excerpt': 'Hướng dẫn chi tiết cách thiết lập và sử dụng Google Calendar một cách thông minh.',
            'excerpt_en': 'Detailed guide on how to set up and use Google Calendar smartly.',
            'author': 'Minh Anh',
            'created_at': datetime.now() - timedelta(days=5),
            'image': 'https://images.unsplash.com/photo-1611224923853-80b023f02d71?w=800&h=400&fit=crop'
        },
        {
            'id': 3,
            'title': 'Top 10 meme sinh viên UEH không thể bỏ qua',
            'title_en': 'Top 10 UEH Student Memes You Cannot Miss',
            'slug': 'top-10-meme-sinh-vien-ueh',
            'excerpt': 'Những meme kinh điển chỉ sinh viên UEH mới hiểu, đảm bảo cười đau bụng!',
            'excerpt_en': 'Classic memes that only UEH students understand, guaranteed to make you laugh!',
            'author': 'Thảo Nguyên',
            'created_at': datetime.now() - timedelta(days=7),
            'image': 'https://images.unsplash.com/photo-1516414447565-b14be0adf13e?w=800&h=400&fit=crop'
        }
    ]

def get_stats():
    """Get application statistics"""
    from models import Order, Feedback
    
    # Real stats from database
    total_orders = Order.query.count()
    pending_orders = Order.query.filter_by(status='pending').count()
    completed_orders = Order.query.filter_by(status='completed').count()
    total_feedbacks = Feedback.query.count()
    unprocessed_feedbacks = Feedback.query.filter_by(is_processed=False).count()
    
    # Today's stats
    today = datetime.now().date()
    today_orders = Order.query.filter(Order.created_at >= today).count()
    
    # Conversion rate (completed orders / total orders)
    conversion_rate = (completed_orders / total_orders * 100) if total_orders > 0 else 0
    
    return {
        'total_orders': total_orders or 1247,  # Fallback to sample data if no real orders
        'today_orders': today_orders,
        'pending_orders': pending_orders,
        'completed_orders': completed_orders,
        'total_feedbacks': total_feedbacks,
        'unprocessed_feedbacks': unprocessed_feedbacks,
        'conversion_rate': round(conversion_rate, 1),
        'total_users': 1500,  # Mock data
        'growth_rate': 15.3   # Mock data
    }
