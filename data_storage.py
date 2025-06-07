"""
In-memory data storage for MVP version
This module provides sample data and utilities for the UEHer application
"""
import random
import hashlib
from datetime import datetime, timedelta

# Service data
SERVICES = {
    'schedule': {
        'name': 'Xếp lịch học tập',
        'name_en': 'Schedule Planning',
        'description': 'Tự động sắp xếp lịch học, ôn tập và deadline cho sinh viên',
        'description_en': 'Automatic scheduling for classes, study sessions and deadlines',
        'icon': 'calendar',
        'features': ['Lịch học thông minh', 'Nhắc nhở deadline', 'Sync với Google Calendar']
    },
    'meme': {
        'name': 'Meme Pack',
        'name_en': 'Meme Package',
        'description': 'Bộ sưu tập meme UEH độc quyền cho sinh viên',
        'description_en': 'Exclusive UEH meme collection for students',
        'icon': 'image',
        'features': ['500+ meme UEH', 'Cập nhật hàng tuần', 'Chia sẻ dễ dàng']
    },
    'documents': {
        'name': 'Tài liệu học tập',
        'name_en': 'Study Materials',
        'description': 'Kho tài liệu chất lượng cao từ các khóa trước',
        'description_en': 'High-quality study materials from previous courses',
        'icon': 'book',
        'features': ['Tài liệu được review', 'Phân loại theo môn', 'Download không giới hạn']
    },
    'other': {
        'name': 'Dịch vụ khác',
        'name_en': 'Other Services',
        'description': 'Các dịch vụ hỗ trợ khác cho sinh viên UEH',
        'description_en': 'Other support services for UEH students',
        'icon': 'more-horizontal',
        'features': ['Tư vấn học tập', 'Hỗ trợ kỹ thuật', 'Dịch vụ tùy chỉnh']
    }
}

# Pricing plans
PRICING_PLANS = {
    'free': {
        'name': 'Free',
        'price_monthly': 0,
        'price_yearly': 0,
        'features': [
            'Xem lịch cơ bản',
            '10 meme/tháng',
            'Tài liệu giới hạn',
            'Hỗ trợ email'
        ],
        'recommended': False
    },
    'basic': {
        'name': 'Basic',
        'price_monthly': 99000,
        'price_yearly': 990000,
        'features': [
            'Lịch học thông minh',
            '100 meme/tháng',
            'Tài liệu không giới hạn',
            'Hỗ trợ ưu tiên',
            'Sync Google Calendar'
        ],
        'recommended': True
    },
    'pro': {
        'name': 'Pro',
        'price_monthly': 199000,
        'price_yearly': 1990000,
        'features': [
            'Tất cả tính năng Basic',
            'Meme không giới hạn',
            'Tài liệu premium',
            'Hỗ trợ 24/7',
            'API access',
            'Custom notifications'
        ],
        'recommended': False
    },
    'team': {
        'name': 'Team',
        'price_monthly': 499000,
        'price_yearly': 4990000,
        'features': [
            'Tất cả tính năng Pro',
            'Quản lý team',
            'Shared calendars',
            'Advanced analytics',
            'Priority support',
            'Custom integrations'
        ],
        'recommended': False
    }
}

# FAQ data
FAQ_DATA = [
    {
        'question': 'UEHer đi học là gì?',
        'question_en': 'What is UEHer đi học?',
        'answer': 'UEHer đi học là nền tảng hỗ trợ sinh viên UEH tự động hóa việc học tập, quản lý thời gian và truy cập tài liệu chất lượng.',
        'answer_en': 'UEHer đi học is a platform that helps UEH students automate their learning process, manage time and access quality study materials.'
    },
    {
        'question': 'Làm sao để đăng ký dịch vụ?',
        'question_en': 'How do I register for services?',
        'answer': 'Bạn có thể đăng ký thông qua trang Order, chọn gói phù hợp và điền thông tin. Chúng tôi sẽ xác nhận qua email.',
        'answer_en': 'You can register through the Order page, choose a suitable package and fill in your information. We will confirm via email.'
    },
    {
        'question': 'Có hỗ trợ sinh viên các trường khác không?',
        'question_en': 'Do you support students from other universities?',
        'answer': 'Hiện tại chúng tôi tập trung vào sinh viên UEH, nhưng có thể mở rộng cho các trường khác trong tương lai.',
        'answer_en': 'Currently we focus on UEH students, but may expand to other universities in the future.'
    },
    {
        'question': 'Tài liệu có được cập nhật thường xuyên không?',
        'question_en': 'Are materials updated regularly?',
        'answer': 'Có, chúng tôi cập nhật tài liệu mỗi học kỳ và bổ sung tài liệu mới từ các khóa học gần đây.',
        'answer_en': 'Yes, we update materials every semester and add new materials from recent courses.'
    },
    {
        'question': 'Có thể hủy dịch vụ không?',
        'question_en': 'Can I cancel the service?',
        'answer': 'Có, bạn có thể hủy dịch vụ bất kỳ lúc nào. Chúng tôi sẽ hoàn tiền theo chính sách hoàn tiền.',
        'answer_en': 'Yes, you can cancel the service anytime. We will refund according to our refund policy.'
    },
    {
        'question': 'Dữ liệu cá nhân có được bảo mật không?',
        'question_en': 'Is personal data secure?',
        'answer': 'Chúng tôi cam kết bảo mật thông tin cá nhân theo tiêu chuẩn cao nhất và không chia sẻ với bên thứ ba.',
        'answer_en': 'We are committed to protecting personal information to the highest standards and do not share with third parties.'
    },
    {
        'question': 'Làm sao để liên hệ hỗ trợ?',
        'question_en': 'How to contact support?',
        'answer': 'Bạn có thể liên hệ qua email, form liên hệ trên website, hoặc hotline 24/7.',
        'answer_en': 'You can contact via email, contact form on website, or 24/7 hotline.'
    },
    {
        'question': 'Có app di động không?',
        'question_en': 'Is there a mobile app?',
        'answer': 'Hiện tại chúng tôi chỉ có web app responsive. App di động sẽ được phát triển trong tương lai.',
        'answer_en': 'Currently we only have a responsive web app. Mobile app will be developed in the future.'
    },
    {
        'question': 'Thanh toán như thế nào?',
        'question_en': 'How to make payment?',
        'answer': 'Chúng tôi hỗ trợ thanh toán qua chuyển khoản ngân hàng, ví điện tử và thẻ tín dụng.',
        'answer_en': 'We support payment via bank transfer, e-wallet and credit card.'
    },
    {
        'question': 'Có trial miễn phí không?',
        'question_en': 'Is there a free trial?',
        'answer': 'Có, chúng tôi có gói Free với các tính năng cơ bản để bạn trải nghiệm trước khi nâng cấp.',
        'answer_en': 'Yes, we have a Free package with basic features for you to try before upgrading.'
    }
]

# Sample blog posts
BLOG_POSTS = [
    {
        'id': 1,
        'title': 'Tips học tập hiệu quả cho sinh viên UEH',
        'title_en': 'Effective study tips for UEH students',
        'slug': 'tips-hoc-tap-hieu-qua-sinh-vien-ueh',
        'excerpt': 'Những phương pháp học tập đã được chứng minh hiệu quả dành riêng cho sinh viên kinh tế.',
        'excerpt_en': 'Proven effective study methods specifically for economics students.',
        'content': '# Tips học tập hiệu quả\n\nViệc học tập tại UEH đòi hỏi những phương pháp đặc biệt...',
        'author': 'Team UEHer',
        'created_at': datetime.now() - timedelta(days=7)
    },
    {
        'id': 2,
        'title': 'Cách quản lý thời gian trong mùa thi',
        'title_en': 'Time management during exam season',
        'slug': 'quan-ly-thoi-gian-mua-thi',
        'excerpt': 'Hướng dẫn chi tiết về cách sắp xếp thời gian ôn tập và thi cử hiệu quả.',
        'excerpt_en': 'Detailed guide on how to organize study and exam time effectively.',
        'content': '# Quản lý thời gian mùa thi\n\nMùa thi là thời điểm căng thẳng nhất...',
        'author': 'Team UEHer',
        'created_at': datetime.now() - timedelta(days=14)
    },
    {
        'id': 3,
        'title': 'Xu hướng việc làm cho sinh viên kinh tế 2024',
        'title_en': 'Job trends for economics students 2024',
        'slug': 'xu-huong-viec-lam-sinh-vien-kinh-te-2024',
        'excerpt': 'Phân tích thị trường lao động và cơ hội việc làm dành cho sinh viên UEH.',
        'excerpt_en': 'Labor market analysis and job opportunities for UEH students.',
        'content': '# Xu hướng việc làm 2024\n\nThị trường lao động đang có những thay đổi lớn...',
        'author': 'Team UEHer',
        'created_at': datetime.now() - timedelta(days=21)
    }
]

def generate_order_number():
    """Generate a unique order number"""
    timestamp = datetime.now().strftime("%Y%m%d")
    random_num = random.randint(1000, 9999)
    return f"UEH{timestamp}{random_num}"

def generate_tx_hash():
    """Generate a mock blockchain transaction hash"""
    random_string = f"{datetime.now().isoformat()}{random.randint(10000, 99999)}"
    return "0x" + hashlib.sha256(random_string.encode()).hexdigest()[:64]

def get_order_stats():
    """Get order statistics for dashboard"""
    return {
        'total_orders': 1247,
        'orders_today': 23,
        'pending_orders': 45,
        'completed_orders': 1156,
        'revenue_this_month': 12450000,
        'conversion_rate': 4.2
    }
