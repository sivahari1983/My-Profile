/**
 * Portfolio Website - Interactive Features & Animations
 */

// ============================================================================
// NAVIGATION & SMOOTH SCROLLING
// ============================================================================

document.addEventListener('DOMContentLoaded', function() {
    // Smooth scroll for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href !== '#' && document.querySelector(href)) {
                e.preventDefault();
                const target = document.querySelector(href);
                const offset = 70; // navbar height
                const targetPosition = target.offsetTop - offset;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
                
                // Close mobile menu if open
                closeMobileMenu();
            }
        });
    });
    
    // Mobile menu toggle
    const navToggle = document.querySelector('.nav-toggle');
    if (navToggle) {
        navToggle.addEventListener('click', function() {
            this.classList.toggle('active');
            const navMenu = document.querySelector('.nav-menu');
            if (navMenu) {
                navMenu.classList.toggle('active');
            }
        });
    }
});

function closeMobileMenu() {
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('.nav-menu');
    if (navToggle && navMenu) {
        navToggle.classList.remove('active');
        navMenu.classList.remove('active');
    }
}

// ============================================================================
// NAVBAR SCROLL EFFECTS
// ============================================================================

window.addEventListener('scroll', function() {
    const navbar = document.querySelector('.navbar');
    if (navbar) {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    }
    updateScrollToTopButton();
});

// ============================================================================
// SCROLL-TO-TOP BUTTON
// ============================================================================

let scrollToTopBtn = null;

function createScrollToTopButton() {
    if (scrollToTopBtn) return;
    
    scrollToTopBtn = document.createElement('button');
    scrollToTopBtn.id = 'scrollToTopBtn';
    scrollToTopBtn.innerHTML = '↑';
    scrollToTopBtn.style.cssText = `
        position: fixed;
        bottom: 2rem;
        right: 2rem;
        width: 50px;
        height: 50px;
        padding: 0;
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        color: white;
        border: none;
        border-radius: 50%;
        font-size: 1.5rem;
        font-weight: bold;
        cursor: pointer;
        display: none;
        z-index: 999;
        box-shadow: 0 10px 15px rgba(0, 0, 0, 0.3);
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        align-items: center;
        justify-content: center;
    `;
    
    scrollToTopBtn.addEventListener('click', function() {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
    
    scrollToTopBtn.addEventListener('mouseenter', function() {
        this.style.transform = 'translateY(-5px)';
        this.style.boxShadow = '0 15px 25px rgba(0, 0, 0, 0.4)';
    });
    
    scrollToTopBtn.addEventListener('mouseleave', function() {
        this.style.transform = 'translateY(0)';
        this.style.boxShadow = '0 10px 15px rgba(0, 0, 0, 0.3)';
    });
    
    document.body.appendChild(scrollToTopBtn);
}

function updateScrollToTopButton() {
    if (!scrollToTopBtn) {
        createScrollToTopButton();
    }
    
    if (window.scrollY > 300) {
        scrollToTopBtn.style.display = 'flex';
    } else {
        scrollToTopBtn.style.display = 'none';
    }
}

// ============================================================================
// INTERSECTION OBSERVER FOR ANIMATIONS
// ============================================================================

const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -100px 0px'
};

const observer = new IntersectionObserver(function(entries) {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.classList.add('animated');
            observer.unobserve(entry.target);
        }
    });
}, observerOptions);

// Observe cards for animation
document.addEventListener('DOMContentLoaded', function() {
    document.querySelectorAll('.expertise-card, .project-card, .service-card, .cert-item, .about-card').forEach(element => {
        observer.observe(element);
        element.style.opacity = '0';
        element.style.animation = 'fadeInUp 0.6s ease-out forwards';
    });
});

// ============================================================================
// PARALLAX EFFECT FOR HERO SECTION
// ============================================================================

window.addEventListener('scroll', function() {
    const blobs = document.querySelectorAll('.blob');
    const scrollY = window.scrollY;
    
    blobs.forEach((blob, index) => {
        const speed = 0.5 + (index * 0.1);
        blob.style.transform = `translateY(${scrollY * speed}px)`;
    });
});

// ============================================================================
// PDF UPLOAD FUNCTIONALITY
// ============================================================================

document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('uploadForm');
    const dropZone = document.getElementById('dropZone');
    const fileInput = document.getElementById('pdf_file');
    const uploadStatus = document.getElementById('uploadStatus');
    const submitBtn = document.getElementById('submitBtn');
    
    if (!uploadForm) return;
    
    // Drag and drop events
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, preventDefaults, false);
    });
    
    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }
    
    ['dragenter', 'dragover'].forEach(eventName => {
        dropZone.addEventListener(eventName, function() {
            dropZone.classList.add('drag-over');
        });
    });
    
    ['dragleave', 'drop'].forEach(eventName => {
        dropZone.addEventListener(eventName, function() {
            dropZone.classList.remove('drag-over');
        });
    });
    
    // Handle dropped files
    dropZone.addEventListener('drop', function(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        
        if (files.length > 0) {
            handleFileSelection(files[0]);
        }
    });
    
    // Handle file input change
    if (fileInput) {
        fileInput.addEventListener('change', function() {
            if (this.files.length > 0) {
                handleFileSelection(this.files[0]);
            }
        });
    }
    
    function handleFileSelection(file) {
        // Validate file
        if (!file.name.toLowerCase().endsWith('.pdf')) {
            showError('Please select a PDF file');
            return;
        }
        
        if (file.size > 50 * 1024 * 1024) {
            showError('File is too large (max 50MB)');
            return;
        }
        
        // Show submit button
        if (submitBtn) {
            submitBtn.style.display = 'inline-block';
        }
        
        uploadStatus.innerHTML = `✓ File selected: ${file.name}`;
        uploadStatus.className = 'upload-status success';
    }
    
    // Handle form submission
    uploadForm.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        const file = fileInput?.files[0];
        if (!file) {
            showError('No file selected');
            return;
        }
        
        if (submitBtn) {
            submitBtn.disabled = true;
            submitBtn.textContent = 'Processing...';
        }
        
        try {
            const formData = new FormData();
            formData.append('pdf_file', file);
            
            const response = await fetch('/upload', {
                method: 'POST',
                body: formData
            });
            
            const data = await response.json();
            
            if (response.ok && data.success) {
                showSuccess('PDF processed successfully! Portfolio updated.');
                // Reset form after 2 seconds
                setTimeout(() => {
                    uploadForm.reset();
                    if (submitBtn) {
                        submitBtn.style.display = 'none';
                        submitBtn.disabled = false;
                        submitBtn.textContent = 'Process PDF';
                    }
                    uploadStatus.innerHTML = '';
                    uploadStatus.className = 'upload-status';
                }, 2000);
            } else {
                showError(data.error || 'Failed to process PDF');
            }
        } catch (error) {
            showError('Error uploading file: ' + error.message);
        } finally {
            if (submitBtn) {
                submitBtn.disabled = false;
                submitBtn.textContent = 'Process PDF';
            }
        }
    });
    
    function showError(message) {
        uploadStatus.innerHTML = '✗ ' + message;
        uploadStatus.className = 'upload-status error';
    }
    
    function showSuccess(message) {
        uploadStatus.innerHTML = '✓ ' + message;
        uploadStatus.className = 'upload-status success';
    }
});

// ============================================================================
// CONTACT FORM HANDLING
// ============================================================================

document.addEventListener('DOMContentLoaded', function() {
    const contactForm = document.getElementById('contactForm');
    
    if (contactForm) {
        contactForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const data = {
                name: formData.get('name') || this.querySelector('input[type="text"]').value,
                email: formData.get('email') || this.querySelector('input[type="email"]').value,
                subject: formData.get('subject') || this.querySelectorAll('input[type="text"]')[1].value,
                message: formData.get('message') || this.querySelector('textarea').value
            };
            
            // Simple validation
            if (!data.name || !data.email || !data.message) {
                alert('Please fill in all fields');
                return;
            }
            
            // Show feedback
            const submitBtn = this.querySelector('button[type="submit"]');
            const originalText = submitBtn.textContent;
            submitBtn.textContent = 'Sending...';
            submitBtn.disabled = true;
            
            // Simulate sending (replace with actual backend endpoint)
            setTimeout(() => {
                alert('Thank you for your message! I will get back to you soon.');
                this.reset();
                submitBtn.textContent = originalText;
                submitBtn.disabled = false;
            }, 1000);
        });
    }
});

// ============================================================================
// RESPONSIVE MOBILE MENU HANDLING
// ============================================================================

window.addEventListener('resize', function() {
    if (window.innerWidth > 768) {
        closeMobileMenu();
    }
});

// Close mobile menu when window is resized to larger sizes
if (window.innerWidth > 768) {
    closeMobileMenu();
}

// ============================================================================
// ANIMATION TRIGGERS ON SCROLL
// ============================================================================

document.addEventListener('DOMContentLoaded', function() {
    // Add animation classes to elements
    const style = document.createElement('style');
    style.textContent = `
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        .animated {
            animation: fadeInUp 0.6s ease-out forwards !important;
        }
    `;
    document.head.appendChild(style);
});

// ============================================================================
// ACCESSIBILITY ENHANCEMENTS
// ============================================================================

// Keyboard navigation for links
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeMobileMenu();
    }
});

// ============================================================================
// INITIALIZE
// ============================================================================

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all interactive elements
    console.log('Portfolio website loaded and initialized');
});
