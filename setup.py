#!/usr/bin/env python3
"""
Setup script for Tử Vi Bot
"""

import os
import subprocess
import sys

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error in {description}: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required!")
        return False
    print(f"✅ Python {sys.version.split()[0]} detected")
    return True

def create_env_file():
    """Create .env file if it doesn't exist"""
    if not os.path.exists('.env'):
        print("📝 Creating .env file...")
        with open('.env', 'w') as f:
            f.write("OPENAI_API_KEY=your_openai_api_key_here\n")
        print("✅ .env file created! Please add your OpenAI API key.")
        return True
    else:
        print("✅ .env file already exists")
        return True

def setup_backend():
    """Setup backend dependencies and database"""
    print("\n🚀 Setting up Backend...")
    
    # Install Python dependencies
    if not run_command("pip install -r requirements.txt", "Installing Python dependencies"):
        return False
    
    # Initialize database
    if not run_command("python -c \"from models import Base, engine; Base.metadata.create_all(engine); print('Database initialized!')\"", "Initializing database"):
        return False
    
    print("✅ Backend setup completed!")
    return True

def setup_frontend():
    """Setup frontend dependencies"""
    print("\n🎨 Setting up Frontend...")
    
    if not os.path.exists('frontend'):
        print("❌ Frontend directory not found!")
        return False
    
    # Change to frontend directory
    os.chdir('frontend')
    
    # Install Node.js dependencies
    if not run_command("npm install", "Installing Node.js dependencies"):
        os.chdir('..')
        return False
    
    # Go back to root directory
    os.chdir('..')
    
    print("✅ Frontend setup completed!")
    return True

def main():
    """Main setup function"""
    print("🔮 Tử Vi Bot Setup Script")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Create .env file
    if not create_env_file():
        sys.exit(1)
    
    # Setup backend
    if not setup_backend():
        print("❌ Backend setup failed!")
        sys.exit(1)
    
    # Setup frontend
    if not setup_frontend():
        print("❌ Frontend setup failed!")
        sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("\n📋 Next steps:")
    print("1. Add your OpenAI API key to .env file")
    print("2. Run backend: python app.py")
    print("3. Run frontend: cd frontend && npm run dev")
    print("\n🌐 Access the application:")
    print("- Backend API: http://localhost:5000")
    print("- Frontend: http://localhost:3000")

if __name__ == "__main__":
    main()
