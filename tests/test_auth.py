import unittest
from flask import Flask
from app import create_app
from app.auth.models import db, User

class AuthTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost:5432/db_ppks_test'
        self.app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
        self.client = self.app.test_client()
        
        with self.app.app_context():
            db.create_all()
            
            # Create a test user
            test_user = User(
                full_name='Test Admin',
                nomor_identitas='12345',
                email='test@admin.com',
                roles='admin',
                phone='08123456789',
                jurusan='IT',
                prodi='Teknik Informatika'
            )
            test_user.set_password('password123')
            db.session.add(test_user)
            db.session.commit()
    
    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()
    
    def test_login_page(self):
        """Test login page loads correctly"""
        response = self.client.get('/auth/login')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Masuk', response.data)
    
    def test_login_with_email(self):
        """Test login with email"""
        response = self.client.post('/auth/login', data={
            'identity': 'test@admin.com',
            'password': 'password123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Dashboard', response.data)  # Assuming 'Dashboard' appears on the dashboard page
    
    def test_login_with_nomor_identitas(self):
        """Test login with nomor_identitas"""
        response = self.client.post('/auth/login', data={
            'identity': '12345',
            'password': 'password123'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Dashboard', response.data)
    
    def test_login_incorrect_password(self):
        """Test login with incorrect password"""
        response = self.client.post('/auth/login', data={
            'identity': 'test@admin.com',
            'password': 'wrongpassword'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Email/NIP atau password tidak valid', response.data)
    
    def test_api_login(self):
        """Test API login endpoint"""
        response = self.client.post('/auth/api/login', json={
            'identity': 'test@admin.com',
            'password': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['message'], 'Login berhasil')
        self.assertEqual(data['user']['email'], 'test@admin.com')

if __name__ == '__main__':
    unittest.main()