# Professional Portfolio Website Generator

A Flask-based web application that converts PDF profiles into beautiful, interactive portfolio websites inspired by professional design standards.

## ✨ Features

- **PDF Profile Import**: Upload your PDF resume/profile and automatically extract structured data
- **Modern Design**: Clean, dark-themed interface with glassmorphism effects and smooth animations
- **Responsive Layout**: Works seamlessly on desktop, tablet, and mobile devices
- **Dynamic Sections**: Hero section with stats, about, expertise categories, experience timeline, projects showcase, services, certifications, speaking engagements, and contact form
- **Interactive Elements**: Smooth scrolling, parallax effects, hover animations, and scroll-to-top button
- **No Database**: Static portfolio generation using JSON data
- **Easy Deployment**: Works with Flask built-in server or any WSGI-compatible host

## 🎯 Sections Included

- **Hero Section**: Your name, professional title, key stats, and call-to-action buttons
- **About Me**: Professional summary with contact information and personal details
- **Expertise**: Categorized skills and technical domains with tag-based visualization
- **Experience**: Timeline of professional roles with company names and descriptions
- **Projects**: Showcase of personal or professional projects with technology stacks
- **Services**: List of services you offer (consulting, development, etc.)
- **Certifications**: Professional credentials and achievements
- **Speaking & Events**: Workshops delivered, audience reached, and event participation
- **Skills**: Technical skills and tools visualization
- **Contact**: Contact form and contact information display

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Windows, macOS, or Linux

### Installation (Windows)

1. **Clone/Download** this repository
2. **Run setup**:
   ```bash
   setup.bat
   ```
   This will create a virtual environment and install dependencies

3. **Start the server**:
   ```bash
   run.bat
   ```

4. **Open your browser** and go to:
   ```
   http://localhost:5000
   ```

### Installation (macOS/Linux)

1. Create virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run the application:
   ```bash
   python app.py
   ```

4. Open `http://localhost:5000` in your browser

## 📄 Using with Your PDF

1. Click **"Upload Your Profile PDF"** button (at the bottom of the page)
2. Select your PDF resume/profile document
3. The system will extract and parse:
   - Contact information (email, phone, LinkedIn)
   - Professional summary
   - Work experience and timeline
   - Education
   - Skills and expertise
   - Languages
   - Certifications
   - Projects

4. Your portfolio will update with the extracted data

## 📋 PDF Structure Recommendations

For best results, structure your PDF profile with clear section headings:

```
[Your Name]

PROFESSIONAL SUMMARY
Your professional overview and background...

EXPERIENCE
Company Name, Position, 2022 – Present
Description of your role and achievements...

EDUCATION
Degree, University Name, 2020

SKILLS / TECHNICAL SKILLS
Python, JavaScript, AWS, Kubernetes, etc.

LANGUAGES
English (Fluent), Spanish (Intermediate)

CERTIFICATIONS
AWS Certified Solutions Architect - Professional, 2024
```

## 🛠️ Customization

### Change Colors
Edit `static/css/style.css` and modify CSS variables at the top:

```css
:root {
    --primary-color: #6366f1;      /* Main color */
    --secondary-color: #8b5cf6;    /* Secondary color */
    --background: #0f172a;         /* Background color */
    /* ... other variables ... */
}
```

### Modify Default Portfolio Data
Edit the `DEFAULT_PORTFOLIO` dictionary in `app.py` to change:
- Name and title
- Professional summary
- Expertise categories
- Example experience entries
- Services offered
- Contact information

### Add/Remove Sections
Edit `templates/index.html` to add or remove sections. Each section uses:

```html
{% if portfolio.section_name %}
<section id="section-id" class="section-class">
    <!-- Your content here -->
</section>
{% endif %}
```

## 🌐 Deployment

### Netlify
1. Connect your GitHub repository
2. Build command: `pip install -r requirements.txt`
3. Publish directory: `.`
4. Add environment variable: `PYTHON_VERSION=3.9`

### Heroku
1. Create `Procfile`:
   ```
   web: gunicorn app:app
   ```

2. Deploy:
   ```bash
   git push heroku main
   ```

### Azure App Service
1. Create App Service (Windows or Linux)
2. Deploy using Git or ZIP
3. Configure startup command in `web.config`

### Self-Hosted Server
1. Install Python 3.8+
2. Clone repository
3. Create virtual environment and install dependencies
4. Use Gunicorn for production:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

## 📚 Technology Stack

- **Backend**: Flask 2.3.3 (Python web framework)
- **PDF Processing**: pdfplumber 0.9.0 (PDF text extraction)
- **Templating**: Jinja2 3.1.2 (HTML templating)
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Styling**: Modern CSS with glassmorphism and animations

## 🔒 Security Considerations

- File uploads limited to 50MB
- Only PDF files accepted
- Secure filename generation
- Input validation on all forms
- No sensitive data storage

## 🐛 Troubleshooting

### "Python not found"
Make sure Python is installed and added to PATH. Verify with:
```bash
python --version
```

### "Module not found" errors
Ensure virtual environment is activated and dependencies installed:
```bash
pip install -r requirements.txt
```

### Port 5000 already in use
Change the port in `app.py`:
```python
app.run(port=5001)  # Use 5001 instead
```

### PDF not parsing correctly
- Ensure PDF has clear section headers (EXPERIENCE, SKILLS, etc.)
- Use standard formatting and fonts
- Avoid scanned images - use text-based PDFs

### Styles not loading
Clear browser cache (Ctrl+Shift+Delete) and refresh page

## 🎨 Design Reference

This template was inspired by professional portfolio designs combining:
- Modern dark theme with accent colors
- Glassmorphism UI elements
- Smooth animations and transitions
- Clear information hierarchy
- Professional typography

## 📝 License

This project is open source and available for personal and professional use.

## 💡 Tips & Best Practices

1. **Keep content concise**: Use bullet points and clear headings
2. **Use consistent formatting**: Helps with PDF parsing
3. **Include metrics**: Add numbers to experience (years, team size, impact)
4. **Optimize images**: If adding custom images, keep file sizes small
5. **Test responsiveness**: Check portfolio on mobile devices
6. **Update regularly**: Keep your profile and skills current

## 🚀 Advanced Customization

### Add Custom Fonts
Edit `static/css/style.css` and add Google Fonts:
```css
@import url('https://fonts.googleapis.com/css2?family=Your+Font@400;700&display=swap');

body {
    font-family: 'Your Font', sans-serif;
}
```

### Add Analytics
Add Google Analytics or Plausible Analytics script to `templates/index.html`

### Add Dark/Light Mode Toggle
Create a custom JavaScript feature to toggle between themes

### Enable Form Backend
Connect contact form to email service (Formspree, SendGrid, etc.)

## 🤝 Contributing

Feel free to fork, modify, and share improvements!

## 📞 Support

For issues or questions:
1. Check the Troubleshooting section
2. Review the PDF structure recommendations
3. Check browser console for JavaScript errors
4. Verify Python and dependencies are correctly installed

## 🎓 Learning Resources

- Flask Documentation: https://flask.palletsprojects.com/
- pdfplumber Guide: https://github.com/jsvine/pdfplumber
- CSS Grid & Flexbox: https://web.dev/learn/css/
- Modern JavaScript: https://javascript.info/

---

**Created with ❤️ for professionals showcasing their expertise**

Built to help you create a stunning, personal portfolio website in minutes.
