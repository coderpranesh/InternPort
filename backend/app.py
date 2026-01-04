from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime
from models import db, User, StudentProfile, CompanyProfile, Internship, Application
from auth import token_required, role_required, create_token
import uuid

app = Flask(__name__)
app.config.from_object('config.Config')
CORS(app)

db.init_app(app)

UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

@app.route('/register', methods=['POST'])
def register():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    role = data.get('role')
    full_name = data.get('full_name')
    
    if not email or not password or not role:
        return jsonify({'error': 'Missing required fields'}), 400
    
    if role not in ['student', 'company', 'admin']:
        return jsonify({'error': 'Invalid role'}), 400
    
    if User.query.filter_by(email=email).first():
        return jsonify({'error': 'Email already registered'}), 400
    
    user = User(email=email, role=role)
    user.set_password(password)
    
    try:
        db.session.add(user)
        db.session.commit()
        
        if role == 'student':
            student_profile = StudentProfile(
                user_id=user.id,
                full_name=full_name
            )
            db.session.add(student_profile)
        elif role == 'company':
            company_name = data.get('company_name')
            if not company_name:
                return jsonify({'error': 'Company name required'}), 400
            company_profile = CompanyProfile(
                user_id=user.id,
                company_name=company_name,
                description=data.get('description', '')
            )
            db.session.add(company_profile)
        
        db.session.commit()
        
        token = create_token(user.id, user.email, user.role)
        return jsonify({
            'message': 'Registration successful',
            'token': token,
            'user': {
                'id': user.id,
                'email': user.email,
                'role': user.role,
                'full_name': full_name if role == 'student' else None,
                'company_name': data.get('company_name') if role == 'company' else None
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'error': 'Email and password required'}), 400
    
    user = User.query.filter_by(email=email, is_active=True).first()
    if not user or not user.check_password(password):
        return jsonify({'error': 'Invalid credentials'}), 401
    
    token = create_token(user.id, user.email, user.role)
    
    user_data = {
        'id': user.id,
        'email': user.email,
        'role': user.role
    }
    
    if user.role == 'student' and user.student_profile:
        user_data['full_name'] = user.student_profile.full_name
    elif user.role == 'company' and user.company_profile:
        user_data['company_name'] = user.company_profile.company_name
    
    return jsonify({
        'message': 'Login successful',
        'token': token,
        'user': user_data
    })

@app.route('/api/profile', methods=['GET'])
@token_required
def get_profile():
    user_id = request.current_user['user_id']
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    profile_data = {
        'email': user.email,
        'role': user.role,
        'created_at': user.created_at.isoformat()
    }
    
    if user.role == 'student' and user.student_profile:
        student = user.student_profile
        profile_data.update({
            'full_name': student.full_name,
            'university': student.university,
            'major': student.major,
            'year_of_study': student.year_of_study,
            'phone': student.phone
        })
    elif user.role == 'company' and user.company_profile:
        company = user.company_profile
        profile_data.update({
            'company_name': company.company_name,
            'description': company.description,
            'website': company.website,
            'location': company.location
        })
    
    return jsonify(profile_data)

@app.route('/api/profile', methods=['PUT'])
@token_required
def update_profile():
    user_id = request.current_user['user_id']
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    data = request.json
    
    if user.role == 'student' and user.student_profile:
        student = user.student_profile
        student.full_name = data.get('full_name', student.full_name)
        student.university = data.get('university', student.university)
        student.major = data.get('major', student.major)
        student.year_of_study = data.get('year_of_study', student.year_of_study)
        student.phone = data.get('phone', student.phone)
    elif user.role == 'company' and user.company_profile:
        company = user.company_profile
        company.company_name = data.get('company_name', company.company_name)
        company.description = data.get('description', company.description)
        company.website = data.get('website', company.website)
        company.location = data.get('location', company.location)
    
    try:
        db.session.commit()
        return jsonify({'message': 'Profile updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/internships', methods=['POST'])
@token_required
@role_required('company')
def create_internship():
    data = request.json
    user_id = request.current_user['user_id']
    
    user = User.query.get(user_id)
    if not user or not user.company_profile:
        return jsonify({'error': 'Company profile not found'}), 404
    
    required_fields = ['title', 'description', 'last_date']
    for field in required_fields:
        if not data.get(field):
            return jsonify({'error': f'{field} is required'}), 400
    
    try:
        last_date = datetime.fromisoformat(data['last_date'])
    except:
        return jsonify({'error': 'Invalid date format'}), 400
    
    internship = Internship(
        company_id=user.company_profile.id,
        title=data['title'],
        description=data['description'],
        requirements=data.get('requirements', ''),
        location=data.get('location', ''),
        stipend=data.get('stipend'),
        last_date=last_date
    )
    
    try:
        db.session.add(internship)
        db.session.commit()
        return jsonify({
            'message': 'Internship created successfully',
            'internship': {
                'id': internship.id,
                'title': internship.title,
                'company_name': user.company_profile.company_name
            }
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/internships', methods=['GET'])
@token_required
def get_internships():
    user_role = request.current_user['role']
    user_id = request.current_user['user_id']
    
    query = Internship.query.filter_by(is_active=True)
    
    if user_role == 'company':
        user = User.query.get(user_id)
        if user and user.company_profile:
            query = query.filter_by(company_id=user.company_profile.id)
    
    internships = query.order_by(Internship.created_at.desc()).all()
    
    result = []
    for internship in internships:
        company = CompanyProfile.query.get(internship.company_id)
        result.append({
            'id': internship.id,
            'title': internship.title,
            'description': internship.description,
            'requirements': internship.requirements,
            'location': internship.location,
            'stipend': internship.stipend,
            'last_date': internship.last_date.isoformat(),
            'created_at': internship.created_at.isoformat(),
            'company_name': company.company_name if company else 'Unknown',
            'company_id': internship.company_id
        })
    
    return jsonify(result)

@app.route('/api/internships/<int:internship_id>', methods=['GET'])
@token_required
def get_internship(internship_id):
    internship = Internship.query.get(internship_id)
    
    if not internship or not internship.is_active:
        return jsonify({'error': 'Internship not found'}), 404
    
    company = CompanyProfile.query.get(internship.company_id)
    
    return jsonify({
        'id': internship.id,
        'title': internship.title,
        'description': internship.description,
        'requirements': internship.requirements,
        'location': internship.location,
        'stipend': internship.stipend,
        'last_date': internship.last_date.isoformat(),
        'created_at': internship.created_at.isoformat(),
        'company_name': company.company_name if company else 'Unknown',
        'company_description': company.description if company else ''
    })

@app.route('/api/internships/<int:internship_id>', methods=['PUT'])
@token_required
@role_required('company')
def update_internship(internship_id):
    user_id = request.current_user['user_id']
    data = request.json
    
    user = User.query.get(user_id)
    if not user or not user.company_profile:
        return jsonify({'error': 'Company profile not found'}), 404
    
    internship = Internship.query.get(internship_id)
    if not internship:
        return jsonify({'error': 'Internship not found'}), 404
    
    if internship.company_id != user.company_profile.id:
        return jsonify({'error': 'Not authorized'}), 403
    
    internship.title = data.get('title', internship.title)
    internship.description = data.get('description', internship.description)
    internship.requirements = data.get('requirements', internship.requirements)
    internship.location = data.get('location', internship.location)
    internship.stipend = data.get('stipend', internship.stipend)
    
    if data.get('last_date'):
        try:
            internship.last_date = datetime.fromisoformat(data['last_date'])
        except:
            return jsonify({'error': 'Invalid date format'}), 400
    
    try:
        db.session.commit()
        return jsonify({'message': 'Internship updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/internships/<int:internship_id>', methods=['DELETE'])
@token_required
@role_required('company')
def delete_internship(internship_id):
    user_id = request.current_user['user_id']
    
    user = User.query.get(user_id)
    if not user or not user.company_profile:
        return jsonify({'error': 'Company profile not found'}), 404
    
    internship = Internship.query.get(internship_id)
    if not internship:
        return jsonify({'error': 'Internship not found'}), 404
    
    if internship.company_id != user.company_profile.id:
        return jsonify({'error': 'Not authorized'}), 403
    
    internship.is_active = False
    
    try:
        db.session.commit()
        return jsonify({'message': 'Internship deleted successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/apply/<int:internship_id>', methods=['POST'])
@token_required
@role_required('student')
def apply_internship(internship_id):
    user_id = request.current_user['user_id']
    
    user = User.query.get(user_id)
    if not user or not user.student_profile:
        return jsonify({'error': 'Student profile not found'}), 404
    
    internship = Internship.query.get(internship_id)
    if not internship or not internship.is_active:
        return jsonify({'error': 'Internship not found'}), 404
    
    if datetime.utcnow() > internship.last_date:
        return jsonify({'error': 'Application deadline has passed'}), 400
    
    existing_application = Application.query.filter_by(
        internship_id=internship_id,
        student_id=user.student_profile.id
    ).first()
    
    if existing_application:
        return jsonify({'error': 'Already applied to this internship'}), 400
    
    data = request.json
    cover_letter = data.get('cover_letter', '')
    
    application = Application(
        internship_id=internship_id,
        student_id=user.student_profile.id,
        cover_letter=cover_letter,
        resume_path=user.student_profile.resume_path
    )
    
    try:
        db.session.add(application)
        db.session.commit()
        return jsonify({
            'message': 'Application submitted successfully',
            'application_id': application.id
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/my-applications', methods=['GET'])
@token_required
@role_required('student')
def get_my_applications():
    user_id = request.current_user['user_id']
    
    user = User.query.get(user_id)
    if not user or not user.student_profile:
        return jsonify({'error': 'Student profile not found'}), 404
    
    applications = Application.query.filter_by(
        student_id=user.student_profile.id
    ).order_by(Application.applied_at.desc()).all()
    
    result = []
    for app in applications:
        internship = Internship.query.get(app.internship_id)
        company = CompanyProfile.query.get(internship.company_id) if internship else None
        
        result.append({
            'id': app.id,
            'internship_id': app.internship_id,
            'internship_title': internship.title if internship else 'Unknown',
            'company_name': company.company_name if company else 'Unknown',
            'status': app.status,
            'applied_at': app.applied_at.isoformat(),
            'cover_letter': app.cover_letter
        })
    
    return jsonify(result)

@app.route('/api/applications/<int:internship_id>', methods=['GET'])
@token_required
@role_required('company')
def get_internship_applications(internship_id):
    user_id = request.current_user['user_id']
    
    user = User.query.get(user_id)
    if not user or not user.company_profile:
        return jsonify({'error': 'Company profile not found'}), 404
    
    internship = Internship.query.get(internship_id)
    if not internship:
        return jsonify({'error': 'Internship not found'}), 404
    
    if internship.company_id != user.company_profile.id:
        return jsonify({'error': 'Not authorized'}), 403
    
    applications = Application.query.filter_by(
        internship_id=internship_id
    ).order_by(Application.applied_at.desc()).all()
    
    result = []
    for app in applications:
        student = StudentProfile.query.get(app.student_id)
        
        result.append({
            'id': app.id,
            'student_id': app.student_id,
            'student_name': student.full_name if student else 'Unknown',
            'student_university': student.university if student else '',
            'student_major': student.major if student else '',
            'status': app.status,
            'applied_at': app.applied_at.isoformat(),
            'cover_letter': app.cover_letter,
            'resume_path': app.resume_path
        })
    
    return jsonify(result)

@app.route('/api/application/<int:application_id>/status', methods=['PUT'])
@token_required
@role_required('company')
def update_application_status(application_id):
    user_id = request.current_user['user_id']
    data = request.json
    
    new_status = data.get('status')
    if not new_status:
        return jsonify({'error': 'Status is required'}), 400
    
    valid_statuses = ['APPLIED', 'SHORTLISTED', 'REJECTED', 'SELECTED']
    if new_status not in valid_statuses:
        return jsonify({'error': 'Invalid status'}), 400
    
    user = User.query.get(user_id)
    if not user or not user.company_profile:
        return jsonify({'error': 'Company profile not found'}), 404
    
    application = Application.query.get(application_id)
    if not application:
        return jsonify({'error': 'Application not found'}), 404
    
    internship = Internship.query.get(application.internship_id)
    if not internship or internship.company_id != user.company_profile.id:
        return jsonify({'error': 'Not authorized'}), 403
    
    application.status = new_status
    
    try:
        db.session.commit()
        return jsonify({'message': 'Application status updated successfully'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@app.route('/api/upload-resume', methods=['POST'])
@token_required
@role_required('student')
def upload_resume():
    user_id = request.current_user['user_id']
    
    if 'resume' not in request.files:
        return jsonify({'error': 'No file uploaded'}), 400
    
    file = request.files['resume']
    if file.filename == '':
        return jsonify({'error': 'No file selected'}), 400
    
    if not file.filename.lower().endswith(('.pdf', '.doc', '.docx')):
        return jsonify({'error': 'Only PDF, DOC, and DOCX files are allowed'}), 400
    
    user = User.query.get(user_id)
    if not user or not user.student_profile:
        return jsonify({'error': 'Student profile not found'}), 404
    
    filename = f"resume_{user_id}_{uuid.uuid4().hex}_{file.filename}"
    filepath = os.path.join(UPLOAD_FOLDER, filename)
    
    try:
        file.save(filepath)
        user.student_profile.resume_path = filename
        
        db.session.commit()
        return jsonify({
            'message': 'Resume uploaded successfully',
            'filename': filename
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/uploads/<filename>')
def serve_upload(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@app.route('/api/admin/users', methods=['GET'])
@token_required
@role_required('admin')
def get_all_users():
    users = User.query.all()
    result = []
    
    for user in users:
        user_data = {
            'id': user.id,
            'email': user.email,
            'role': user.role,
            'is_active': user.is_active,
            'created_at': user.created_at.isoformat()
        }
        
        if user.role == 'student' and user.student_profile:
            user_data['full_name'] = user.student_profile.full_name
        elif user.role == 'company' and user.company_profile:
            user_data['company_name'] = user.company_profile.company_name
        
        result.append(user_data)
    
    return jsonify(result)

@app.route('/api/admin/internships', methods=['GET'])
@token_required
@role_required('admin')
def get_all_internships():
    internships = Internship.query.order_by(Internship.created_at.desc()).all()
    result = []
    
    for internship in internships:
        company = CompanyProfile.query.get(internship.company_id)
        result.append({
            'id': internship.id,
            'title': internship.title,
            'company_name': company.company_name if company else 'Unknown',
            'location': internship.location,
            'stipend': internship.stipend,
            'last_date': internship.last_date.isoformat(),
            'created_at': internship.created_at.isoformat(),
            'is_active': internship.is_active,
            'application_count': len(internship.applications)
        })
    
    return jsonify(result)

@app.route('/api/admin/applications', methods=['GET'])
@token_required
@role_required('admin')
def get_all_applications():
    applications = Application.query.order_by(Application.applied_at.desc()).all()
    result = []
    
    for app in applications:
        internship = Internship.query.get(app.internship_id)
        company = CompanyProfile.query.get(internship.company_id) if internship else None
        student = StudentProfile.query.get(app.student_id)
        
        result.append({
            'id': app.id,
            'internship_title': internship.title if internship else 'Unknown',
            'company_name': company.company_name if company else 'Unknown',
            'student_name': student.full_name if student else 'Unknown',
            'status': app.status,
            'applied_at': app.applied_at.isoformat()
        })
    
    return jsonify(result)

def create_admin_user():
    admin_email = 'admin@internport.com'
    admin_password = 'admin123'
    
    if not User.query.filter_by(email=admin_email).first():
        admin = User(email=admin_email, role='admin')
        admin.set_password(admin_password)
        db.session.add(admin)
        
        demo_student = User(email='student@internport.com', role='student')
        demo_student.set_password('student123')
        db.session.add(demo_student)
        
        demo_company = User(email='company@internport.com', role='company')
        demo_company.set_password('company123')
        db.session.add(demo_company)
        
        db.session.commit()
        
        student_profile = StudentProfile(
            user_id=demo_student.id,
            full_name='Demo Student',
            university='Demo University',
            major='Computer Science',
            year_of_study='3rd Year'
        )
        db.session.add(student_profile)
        
        company_profile = CompanyProfile(
            user_id=demo_company.id,
            company_name='Demo Corp',
            description='A demo company for testing',
            website='https://democorp.com',
            location='Demo City'
        )
        db.session.add(company_profile)
        
        db.session.commit()
        print("Demo users created successfully")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        create_admin_user()
    app.run(debug=True, port=5000)