# Getting Started Guide

Welcome! This guide will help you get your portfolio website up and running in minutes.

## ⚡ Quick Start (5 minutes)

### Step 1: Run Setup (Windows)
Double-click `setup.bat` in the project folder. This will:
- Check if Python is installed
- Create a virtual environment
- Install all dependencies

### Step 2: Start the Server
Double-click `run.bat`. You should see:
```
Server is running!
Open your browser and navigate to: http://localhost:5000
```

### Step 3: View Your Portfolio
Open your web browser and go to:
```
http://localhost:5000
```

You'll see a beautiful portfolio website with default profile data!

## 📄 Step 4: Upload Your PDF (Optional)

1. Scroll to the bottom of the page
2. Look for "Upload Your Profile PDF" section
3. Click the upload box or drag-drop your PDF file
4. Click "Process PDF"
5. Your portfolio will update with your profile data!

## 🖥️ macOS/Linux Setup

Open terminal and run:

```bash
# Navigate to project directory
cd "path/to/My website"

# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the server
python app.py
```

Then open `http://localhost:5000` in your browser.

## 📝 Portfolio Structure

Your portfolio website displays these sections:

1. **Hero Section** - Your name, title, and key stats
2. **About Me** - Professional summary and contact info
3. **Expertise** - Skills organized by category
4. **Experience** - Timeline of your roles
5. **Projects** - Personal/professional projects
6. **Services** - What you offer
7. **Certifications** - Your credentials
8. **Speaking** - Workshop and event participation
9. **Skills** - Technology stack
10. **Contact** - Get in touch section

## 🎯 Customization Tips

### Change Your Name & Title
1. Open `app.py` in a text editor
2. Find `DEFAULT_PORTFOLIO = {`
3. Update `'name'` and `'title'` fields
4. Save and refresh your browser

### Change Colors
1. Open `static/css/style.css`
2. Find the `:root {` section at the top
3. Edit color values:
   - `--primary-color: #6366f1;` (main blue)
   - `--secondary-color: #8b5cf6;` (purple)
   - `--background: #0f172a;` (dark background)
4. Save and refresh browser

### Update Default Content
Edit these sections in `app.py`:
- `DEFAULT_PORTFOLIO['summary']` - Professional summary
- `DEFAULT_PORTFOLIO['expertise']` - Skills & expertise
- `DEFAULT_PORTFOLIO['services']` - Services offered
- `DEFAULT_PORTFOLIO['projects']` - Your projects

## 📄 PDF Upload Guide

### Supported PDF Types
- Text-based PDFs (preferred)
- Resumes and CVs
- Professional profiles
- Any document with structured text

### NOT Supported
- Scanned/image-based PDFs (no text layer)
- Very small text (hard to read)
- Non-English PDFs (may parse incorrectly)

### PDF Structure for Best Results

Your PDF should have clear section headings like:

```
YOUR NAME

OBJECTIVE / PROFESSIONAL SUMMARY
Your professional background and goals...

WORK EXPERIENCE / EXPERIENCE
Job Title
Company Name, Location, 2020 – Present
Description of your role and achievements...

EDUCATION
Degree, University Name, Graduation Year

TECHNICAL SKILLS / SKILLS
Skill 1, Skill 2, Skill 3, Skill 4...

LANGUAGES
English (Native), Spanish (Fluent)...

CERTIFICATIONS
Certification Name, Issuer, Year

PROJECTS / PORTFOLIO
Project Name - Description...
```

## 🌐 Browser Compatibility

Works on:
- Chrome/Chromium (recommended)
- Firefox
- Safari
- Edge
- Mobile browsers (iOS Safari, Android Chrome)

## 🔧 Troubleshooting

### "setup.bat not working"
**Problem**: Command not recognized or Python not found

**Solution**:
1. Ensure Python 3.8+ is installed
2. Use command prompt (not PowerShell if possible)
3. Run as Administrator (right-click → Run as administrator)

### "Can't access http://localhost:5000"
**Problem**: Connection refused

**Solution**:
1. Ensure run.bat is still running (terminal window open)
2. Check if port 5000 is available
3. Wait 10 seconds after starting, servers take a moment to start
4. Try http://127.0.0.1:5000 instead

### "PDF not parsing correctly"
**Problem**: Portfolio data not updating from PDF

**Solution**:
1. Ensure it's a text-based PDF (not scanned image)
2. Use clear section headings (EXPERIENCE, SKILLS, etc.)
3. Keep text reasonably sized and readable
4. Try with the sample data first to verify upload works

### "CSS/images not loading"
**Problem**: Page looks unstyled or broken

**Solution**:
1. Force refresh: Ctrl+Shift+R (or Cmd+Shift+R on Mac)
2. Clear browser cache
3. Check browser console for error messages (F12)

### "Port 5000 already in use"
**Problem**: Error about port already in use

**Solution**:
1. Close other instances of run.bat
2. Edit app.py, change `port=5000` to `port=5001`
3. Restart the server

## 📚 File Structure

```
My website/
├── app.py                    # Flask application
├── generate_portfolio.py     # PDF parsing logic
├── requirements.txt          # Python dependencies
├── setup.bat                 # Windows setup script
├── run.bat                   # Windows run script
├── README.md                 # Full documentation
├── GETTING_STARTED.md        # This file
├── .gitignore               # Git ignore rules
├── templates/
│   └── index.html           # Portfolio HTML template
├── static/
│   ├── css/
│   │   └── style.css        # All styling
│   └── js/
│       └── main.js          # Interactive features
└── uploads/                 # Uploaded PDFs stored here
```

## 🎨 Design Features

- **Dark Theme**: Easy on the eyes, professional look
- **Glassmorphism**: Modern frosted glass effect cards
- **Animations**: Smooth scrolling and hover effects
- **Responsive**: Looks great on all device sizes
- **Accessibility**: Keyboard navigation support

## 🚀 What's Next?

1. **Customize Your Portfolio**:
   - Edit colors and fonts
   - Update profile information
   - Add your own images

2. **Upload Your PDF**:
   - Prepare your resume/profile PDF
   - Upload it for automatic parsing

3. **Deploy Online**:
   - Share your portfolio with the world
   - Deploy to Netlify, GitHub Pages, or your server

4. **Share Your Portfolio**:
   - Get the link and share with recruiters
   - Include in job applications
   - Use in networking

## 💡 Pro Tips

### Tip 1: Mobile Preview
Open your portfolio on your phone to see how it looks on mobile devices.

### Tip 2: Test PDF Parsing
Before uploading your actual resume, test with a simple PDF to see what gets extracted.

### Tip 3: Keep Data Updated
Regularly update your portfolio information to reflect your latest experience and skills.

### Tip 4: Custom Domain
When deployed, get a custom domain like `yourname.com` for a professional look.

### Tip 5: Analytics
Add Google Analytics to track who visits your portfolio.

## 📞 Need Help?

### Check These First:
1. The README.md for full documentation
2. Browser console for errors (F12)
3. The app.py file for configuration options

### Common Questions:

**Q: Can I modify the design?**
A: Yes! Edit `static/css/style.css` for styling and `templates/index.html` for layout.

**Q: Can I add more sections?**
A: Yes! Add new `<section>` elements to `index.html` and style them with CSS.

**Q: How do I deploy this online?**
A: See the README.md Deployment section for Netlify, Heroku, Azure, and self-hosted options.

**Q: Can I use my own domain?**
A: Yes! When deployed on Netlify or other hosting, you can connect a custom domain.

**Q: Is this free?**
A: Yes! The code is open source and free to use.

## 🎓 Learning Resources

- **Flask**: https://flask.palletsprojects.com/
- **CSS**: https://developer.mozilla.org/en-US/docs/Web/CSS/
- **JavaScript**: https://developer.mozilla.org/en-US/docs/Web/JavaScript/
- **HTML**: https://developer.mozilla.org/en-US/docs/Web/HTML/

## ✨ You're All Set!

Your portfolio website is ready to showcase your professional profile. Start by:

1. Opening `http://localhost:5000`
2. Uploading your PDF (optional)
3. Customizing the design to your liking
4. Sharing with the world!

Enjoy your beautiful new portfolio! 🚀

---

*Happy coding and best of luck with your career!*
