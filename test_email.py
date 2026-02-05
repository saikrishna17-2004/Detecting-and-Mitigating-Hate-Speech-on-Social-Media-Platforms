"""
Test Email Notification System
"""
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from backend.utils.email_service import email_service

def main():
    print("\n" + "="*60)
    print("  EMAIL NOTIFICATION SYSTEM TEST")
    print("="*60 + "\n")
    
    # Check configuration
    if not email_service.enabled:
        print("❌ Email service is NOT configured\n")
        print("To enable email notifications:")
        print("1. Edit the .env file")
        print("2. Add your SMTP settings:")
        print("   SMTP_SERVER=smtp.gmail.com")
        print("   SMTP_PORT=587")
        print("   SENDER_EMAIL=your-email@gmail.com")
        print("   SENDER_PASSWORD=your-app-password")
        print("\nSee EMAIL_SETUP_GUIDE.md for detailed instructions.\n")
        return
    
    print("✅ Email service is CONFIGURED\n")
    print(f"SMTP Server: {email_service.smtp_server}")
    print(f"SMTP Port: {email_service.smtp_port}")
    print(f"Sender Email: {email_service.sender_email}\n")
    print("-" * 60)
    
    # Get test email
    test_email = input("\nEnter email address to test: ").strip()
    
    if not test_email or '@' not in test_email:
        print("❌ Invalid email address")
        return
    
    print(f"\nSending test email to: {test_email}")
    print("Please wait...\n")
    
    # Send test email
    success = email_service.send_test_email(test_email)
    
    if success:
        print("✅ Test email sent successfully!")
        print(f"\nCheck your inbox at: {test_email}")
        print("(Don't forget to check spam/junk folder)\n")
        
        # Ask if user wants to test warning/suspension emails
        print("-" * 60)
        test_more = input("\nWould you like to test warning/suspension emails? (y/n): ").strip().lower()
        
        if test_more == 'y':
            print("\n1. Testing Warning Email...")
            email_service.send_warning_email(
                user_email=test_email,
                username="TestUser",
                warning_count=2,
                max_warnings=3,
                violation_content="This is a test violation content for demonstration purposes.",
                category="test"
            )
            
            print("2. Testing Suspension Email...")
            email_service.send_suspension_email(
                user_email=test_email,
                username="TestUser",
                violation_count=3,
                final_violation_content="This is a test suspension content for demonstration purposes.",
                category="test"
            )
            
            print("\n✅ All test emails sent!")
            print(f"Check your inbox at: {test_email}\n")
    else:
        print("❌ Failed to send test email")
        print("\nTroubleshooting:")
        print("1. Check your SMTP credentials in .env file")
        print("2. For Gmail: Use App Password, not regular password")
        print("3. Make sure 2FA is enabled for Gmail/Yahoo")
        print("4. Check firewall settings")
        print("\nSee EMAIL_SETUP_GUIDE.md for help.\n")

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nTest cancelled by user.\n")
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
