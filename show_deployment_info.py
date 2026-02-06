#!/usr/bin/env python3
"""
Deployment Information Display
Shows all the information needed to deploy the project
"""

print("\n" + "="*70)
print("🚀 DEPLOYMENT INFORMATION")
print("="*70 + "\n")

print("✅ Your project is READY TO DEPLOY!")
print("\n📖 Read these files for instructions:")
print("   1. DEPLOY_NOW.md - Quick start guide (recommended)")
print("   2. DEPLOYMENT_CHECKLIST.md - Detailed checklist")
print("   3. DEPLOYMENT_GUIDE.md - Complete documentation")

print("\n🔐 Environment Variables for Render:")
print("-" * 70)
print("DATABASE_URL=mongodb+srv://SAIKRISHNA:YadavNakkala@cluster0.osgwmcy.mongodb.net/hate_speech_db?retryWrites=true&w=majority")
print("SECRET_KEY=ib90onHydhLh8cpoAUYLIyA0bAVQrKb7BVSYcRMISsg")
print("JWT_SECRET_KEY=JJFEZ6Cvc1YhQ45nRsm2mMaqyPURX-sFrGMHfBohr9A")
print("FLASK_ENV=production")
print("FRONTEND_URL=https://your-netlify-site.netlify.app")
print("-" * 70)

print("\n📝 Deployment Steps:")
print("   1. Push to GitHub:")
print("      git add .")
print('      git commit -m "Ready for deployment"')
print("      git push origin main")
print()
print("   2. Deploy Backend on Render.com")
print("      - Sign up at https://render.com")
print("      - Create new Web Service from GitHub repo")
print("      - Add environment variables above")
print()
print("   3. Deploy Frontend on Netlify.com")
print("      - Sign up at https://netlify.com")
print("      - Import project from GitHub")
print("      - Set base directory: frontend-react")
print("      - Add env var: REACT_APP_API_BASE_URL=https://your-render-url.onrender.com/api")
print()

print("🌐 Deployment Platforms:")
print("   Backend:  https://render.com")
print("   Frontend: https://netlify.com")
print("   Database: https://cloud.mongodb.com (already configured)")

print("\n" + "="*70)
print("📚 For complete instructions, open: DEPLOY_NOW.md")
print("="*70 + "\n")
