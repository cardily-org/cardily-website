// Ensure page starts at the top and stays there - prevent any auto-scrolling
(function() {
    // Immediately set scroll position before anything else
    if (window.scrollY > 0) {
        window.scrollTo(0, 0);
    }
    document.documentElement.scrollTop = 0;
    document.body.scrollTop = 0;
    
    // Prevent hash from scrolling on page load
    const hash = window.location.hash;
    if (hash) {
        window.location.hash = '';
    }
})();

// Page Loader - Fast loading
window.addEventListener('load', () => {
    const loader = document.querySelector('.page-loader');
    if (loader) {
        setTimeout(() => {
            loader.classList.add('hidden');
            // Remove from DOM after animation
            setTimeout(() => {
                loader.remove();
            }, 300);
        }, 150);
    }
    
    window.scrollTo(0, 0);
    document.documentElement.scrollTop = 0;
    document.body.scrollTop = 0;
});

document.addEventListener('DOMContentLoaded', () => {
    // Force immediate scroll to top
    window.scrollTo({ top: 0, left: 0, behavior: 'auto' });
    document.documentElement.scrollTop = 0;
    document.body.scrollTop = 0;
    
    // Only allow hash scrolling if it's from a user click, not initial load
    const hash = window.location.hash;
    if (hash) {
        // Remove hash temporarily to prevent auto-scroll
        history.replaceState(null, null, ' ');
        // Restore hash after a delay if needed for navigation
        setTimeout(() => {
            if (hash) {
                history.replaceState(null, null, hash);
            }
        }, 100);
    }
    
    // Accessibility enhancements
    initAccessibilityFeatures();
    
    // Set active navigation item based on current page
    const currentPage = window.location.pathname.split('/').pop() || 'index.html';
    const navLinks = document.querySelectorAll('.nav-menu a');
    
    navLinks.forEach(link => {
        const linkPage = link.getAttribute('href').split('#')[0];
        if (linkPage === currentPage || (currentPage === '' && linkPage === 'index.html')) {
            link.classList.add('active');
        }
        
        // Also handle hash links on the same page
        if (link.getAttribute('href').startsWith('#')) {
            link.addEventListener('click', () => {
                navLinks.forEach(l => l.classList.remove('active'));
                if (currentPage === 'index.html' || currentPage === '') {
                    link.classList.add('active');
                }
            });
        }
    });
});

// Mobile Menu Toggle
const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
const navMenu = document.querySelector('.nav-menu');

if (mobileMenuToggle) {
    mobileMenuToggle.addEventListener('click', () => {
        navMenu.classList.toggle('active');
        
        // Animate hamburger icon
        const spans = mobileMenuToggle.querySelectorAll('span');
        if (navMenu.classList.contains('active')) {
            spans[0].style.transform = 'rotate(45deg) translate(5px, 5px)';
            spans[1].style.opacity = '0';
            spans[2].style.transform = 'rotate(-45deg) translate(7px, -6px)';
        } else {
            spans[0].style.transform = 'none';
            spans[1].style.opacity = '1';
            spans[2].style.transform = 'none';
        }
    });
}

// Close mobile menu when clicking on a link
const navLinks = document.querySelectorAll('.nav-menu a');
navLinks.forEach(link => {
    link.addEventListener('click', () => {
        navMenu.classList.remove('active');
        const spans = mobileMenuToggle.querySelectorAll('span');
        spans[0].style.transform = 'none';
        spans[1].style.opacity = '1';
        spans[2].style.transform = 'none';
    });
});

// Smooth scroll for anchor links (only on click, not on page load) - Optimized
document.addEventListener('DOMContentLoaded', function() {
    // Add smooth scroll class only for anchor link clicks
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                const offsetTop = target.offsetTop - 80; // Account for sticky navbar
                
                // Use native smooth scroll with optimized behavior
                document.documentElement.classList.add('smooth-scroll');
                window.scrollTo({
                    top: offsetTop,
                    behavior: 'smooth'
                });
                
                // Remove smooth scroll class after animation
                setTimeout(() => {
                    document.documentElement.classList.remove('smooth-scroll');
                }, 500);
            }
        });
    });
});

// Prevent automatic scrolling on page load
if (window.location.hash) {
    // Only scroll to hash if it's from a click, not initial page load
    const hash = window.location.hash;
    window.location.hash = '';
    setTimeout(() => {
        window.location.hash = hash;
    }, 100);
}

// Add scroll animation to elements
const observerOptions = {
    threshold: 0.1,
    rootMargin: '0px 0px -50px 0px'
};

const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
        }
    });
}, observerOptions);

// Enhanced scroll animations with stagger effect
document.addEventListener('DOMContentLoaded', () => {
    // Animate cards with stagger
    const cardElements = document.querySelectorAll('.feature-card, .highlight-box, .contact-card, .project-card, .newsletter-card, .research-card');
    cardElements.forEach((el, index) => {
        el.style.opacity = '0';
        el.style.transform = 'translateY(30px)';
        el.style.transition = `opacity 0.8s ease ${index * 0.1}s, transform 0.8s ease ${index * 0.1}s`;
        observer.observe(el);
    });

    // Animate sections
    const sections = document.querySelectorAll('section');
    sections.forEach((section, index) => {
        if (!section.classList.contains('hero')) {
            section.style.opacity = '0';
            section.style.transform = 'translateY(20px)';
            section.style.transition = `opacity 0.8s ease ${index * 0.15}s, transform 0.8s ease ${index * 0.15}s`;
            observer.observe(section);
        }
    });

    // Animate navigation items
    const navItems = document.querySelectorAll('.nav-menu li');
    navItems.forEach((item, index) => {
        item.style.opacity = '0';
        item.style.transform = 'translateY(-10px)';
        item.style.transition = `opacity 0.5s ease ${index * 0.1 + 0.3}s, transform 0.5s ease ${index * 0.1 + 0.3}s`;
        setTimeout(() => {
            item.style.opacity = '1';
            item.style.transform = 'translateY(0)';
        }, 100);
    });
});

// Enhanced navbar scroll effects - hide on scroll down, show on scroll up
let lastScroll = 0;
const navbar = document.querySelector('.navbar');
let ticking = false;

window.addEventListener('scroll', () => {
    if (!ticking) {
        window.requestAnimationFrame(() => {
            const currentScroll = window.pageYOffset;
            
            // Back to top button visibility
            const backToTop = document.getElementById('back-to-top');
            if (backToTop) {
                if (currentScroll > 300) {
                    backToTop.classList.add('visible');
                } else {
                    backToTop.classList.remove('visible');
                }
            }
            
            if (currentScroll <= 0) {
                // At the top of the page
                navbar.style.transform = 'translateY(0)';
                navbar.style.boxShadow = '0 1px 3px rgba(0, 0, 0, 0.1)';
            } else if (currentScroll > lastScroll && currentScroll > 100) {
                // Scrolling down - hide navbar
                navbar.style.transform = 'translateY(-100%)';
                navbar.style.transition = 'transform 0.3s ease-in-out';
            } else {
                // Scrolling up - show navbar
                navbar.style.transform = 'translateY(0)';
                navbar.style.transition = 'transform 0.3s ease-in-out';
                if (currentScroll > 100) {
                    navbar.style.boxShadow = '0 4px 6px rgba(0, 0, 0, 0.1)';
                }
            }
            
            lastScroll = currentScroll;
            ticking = false;
        });
        ticking = true;
    }
});

// Back to Top Button
const backToTopBtn = document.getElementById('back-to-top');
if (backToTopBtn) {
    backToTopBtn.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
}

// Parallax effect for hero image
window.addEventListener('scroll', () => {
    const heroImage = document.querySelector('.hero-image img');
    if (heroImage) {
        const scrolled = window.pageYOffset;
        const rate = scrolled * 0.3;
        heroImage.style.transform = `translateY(${rate}px) scale(1.05)`;
    }
});

// Animated Counter for Stats
function animateCounter(element) {
    const target = parseInt(element.getAttribute('data-target'));
    const duration = 2000; // 2 seconds
    const steps = 60;
    const increment = target / steps;
    let current = 0;
    
    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            element.textContent = target.toLocaleString() + '+';
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(current).toLocaleString();
        }
    }, duration / steps);
}

// Observe stats section for counter animation
const statsObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting && !entry.target.classList.contains('counted')) {
            entry.target.classList.add('counted');
            const statNumbers = entry.target.querySelectorAll('.stat-number');
            statNumbers.forEach(num => {
                animateCounter(num);
            });
            statsObserver.unobserve(entry.target);
        }
    });
}, {
    threshold: 0.5
});

document.addEventListener('DOMContentLoaded', () => {
    const statsSection = document.querySelector('.stats-section');
    if (statsSection) {
        statsObserver.observe(statsSection);
    }
});

// Smooth reveal animations on scroll
const revealObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            entry.target.style.opacity = '1';
            entry.target.style.transform = 'translateY(0)';
            entry.target.classList.add('animated');
        }
    });
}, {
    threshold: 0.01,
    rootMargin: '0px 0px 300px 0px'
});

// Observe all animatable elements
document.addEventListener('DOMContentLoaded', () => {
    const elementsToAnimate = document.querySelectorAll('.section-header, .mission-content > p, .vision-text, .page-content h2, .page-content p, .career-item, .research-card, .active-project-card, .project-card, .involvement-card, .feature-card, .stat-item');
    elementsToAnimate.forEach(el => {
        if (!el.classList.contains('animated')) {
            el.style.opacity = '0';
            el.style.transform = 'translateY(20px)';
            el.style.transition = 'opacity 0.8s ease, transform 0.8s ease';
            revealObserver.observe(el);
        }
    });
});

// Careers page search and filter functionality
document.addEventListener('DOMContentLoaded', () => {
    const searchInput = document.querySelector('.search-input');
    const locationFilter = document.querySelectorAll('.filter-select')[0];
    const departmentFilter = document.querySelectorAll('.filter-select')[1];
    const typeFilter = document.querySelectorAll('.filter-select')[2];
    const careerItems = document.querySelectorAll('.career-item');
    const resultsCount = document.querySelector('.results-count');

    // Only run if we're on the careers page
    if (!searchInput || !careerItems.length) return;

    function filterJobs() {
        const searchTerm = searchInput.value.toLowerCase();
        const selectedLocation = locationFilter.value;
        const selectedDepartment = departmentFilter.value;
        const selectedType = typeFilter.value;
        
        let visibleCount = 0;

        careerItems.forEach(item => {
            const title = item.querySelector('h3').textContent.toLowerCase();
            const description = item.querySelector('.career-item-description').textContent.toLowerCase();
            const location = item.getAttribute('data-location');
            const department = item.getAttribute('data-department');
            const type = item.getAttribute('data-type');
            const locationText = item.querySelector('.meta-item').textContent.toLowerCase();

            // Check if item matches all filters
            const matchesSearch = title.includes(searchTerm) || 
                                  description.includes(searchTerm) || 
                                  locationText.includes(searchTerm);
            const matchesLocation = !selectedLocation || location === selectedLocation;
            const matchesDepartment = !selectedDepartment || department === selectedDepartment;
            const matchesType = !selectedType || type === selectedType;

            if (matchesSearch && matchesLocation && matchesDepartment && matchesType) {
                item.style.display = 'flex';
                visibleCount++;
            } else {
                item.style.display = 'none';
            }
        });

        // Update results count
        const positionText = visibleCount === 1 ? 'position' : 'positions';
        resultsCount.textContent = `${visibleCount} ${positionText} available`;
    }

    // Add event listeners
    if (searchInput) searchInput.addEventListener('input', filterJobs);
    if (locationFilter) locationFilter.addEventListener('change', filterJobs);
    if (departmentFilter) departmentFilter.addEventListener('change', filterJobs);
    if (typeFilter) typeFilter.addEventListener('change', filterJobs);
});

// Application Modal Functionality
document.addEventListener('DOMContentLoaded', function() {
    const modal = document.getElementById('application-modal');
    const closeButtons = document.querySelectorAll('.modal-close');
    const form = document.getElementById('application-form');
    
    if (!modal) return; // Only run on careers page
    
    // Handle Apply Now clicks
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('career-item-apply') || 
            e.target.closest('.career-item-apply')) {
            e.preventDefault();
            
            // Get position title
            const careerItem = e.target.closest('.career-item');
            const positionTitle = careerItem.querySelector('h3').textContent;
            
            // Set position in form
            document.getElementById('position-title').value = positionTitle;
            document.querySelector('.modal-header h3').textContent = `Apply for ${positionTitle}`;
            
            // Show modal
            modal.style.display = 'flex';
            document.body.style.overflow = 'hidden';
        }
    });
    
    // Close modal
    closeButtons.forEach(button => {
        button.addEventListener('click', function() {
            closeModal();
        });
    });
    
    // Close on outside click
    modal.addEventListener('click', function(e) {
        if (e.target === modal) {
            closeModal();
        }
    });
    
    function closeModal() {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
        form.reset();
        // Reset file upload displays
        document.querySelectorAll('.file-text').forEach(text => {
            text.textContent = text.closest('.file-upload-group').querySelector('label').textContent.includes('Resume') ? 'Choose Resume File' : 'Choose Cover Letter';
        });
    }
    
    // Handle file uploads
    document.querySelectorAll('input[type="file"]').forEach(input => {
        input.addEventListener('change', function() {
            const fileText = this.closest('.file-upload-wrapper').querySelector('.file-text');
            if (this.files.length > 0) {
                fileText.textContent = this.files[0].name;
            } else {
                fileText.textContent = this.id.includes('resume') ? 'Choose Resume File' : 'Choose Cover Letter';
            }
        });
    });
    
    // Handle form submission
    form.addEventListener('submit', function(e) {
        e.preventDefault();
        
        const formData = new FormData(this);
        const data = Object.fromEntries(formData);
        
        // Validate required compliance checkboxes
        const dataProcessingConsent = document.getElementById('data-processing-consent');
        const termsAgreement = document.getElementById('terms-agreement');
        
        if (!dataProcessingConsent.checked) {
            alert('You must consent to data processing for recruitment purposes to submit your application.');
            dataProcessingConsent.focus();
            return;
        }
        
        if (!termsAgreement.checked) {
            alert('You must agree to the Terms of Service to submit your application.');
            termsAgreement.focus();
            return;
        }
        
        // Collect compliance preferences
        const backgroundCheckConsent = document.getElementById('background-check-consent').checked;
        const marketingConsent = document.getElementById('marketing-consent').checked;
        
        // Create comprehensive email content
        const subject = `Job Application: ${data.position} - ${data.name}`;
        const body = `
New job application received:

Position: ${data.position}
Name: ${data.name}
Email: ${data.email}
Phone: ${data.phone || 'Not provided'}
LinkedIn: ${data.linkedin || 'Not provided'}
Portfolio: ${data.portfolio || 'Not provided'}

Cover Letter/Interest:
${data.coverLetterText}

COMPLIANCE INFORMATION:
✅ Data Processing Consent: Granted
✅ Terms of Service: Accepted
${backgroundCheckConsent ? '✅' : '❌'} Background Check Authorization: ${backgroundCheckConsent ? 'Authorized' : 'Not authorized'}
${marketingConsent ? '✅' : '❌'} Marketing Communications: ${marketingConsent ? 'Consented' : 'Declined'}

Note: Resume and additional documents need to be manually attached to this email from the application files.

Application submitted on: ${new Date().toLocaleDateString()} at ${new Date().toLocaleTimeString()}
Compliance verified: Yes
`;
        
        // Create mailto link
        const mailtoLink = `mailto:support@cardily.org?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;
        
        // Show success message
        showSuccessMessage(data.position);
        
        // Open email client
        window.location.href = mailtoLink;
        
        // Close modal
        closeModal();
    });
    
    function showSuccessMessage(position) {
        // Create success notification
        const notification = document.createElement('div');
        notification.className = 'success-notification';
        notification.innerHTML = `
            <div class="notification-content">
                <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                    <polyline points="22 4 12 14.01 9 11.01"></polyline>
                </svg>
                <div>
                    <h4>Application Submitted!</h4>
                    <p>Your application for ${position} has been prepared. Please send the email that opened in your email client.</p>
                </div>
            </div>
        `;
        
        document.body.appendChild(notification);
        
        // Auto remove after 5 seconds
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, 5000);
        
        // Click to dismiss
        notification.addEventListener('click', () => {
            notification.remove();
        });
    }
});

// Accessibility Features
function initAccessibilityFeatures() {
    // Enhanced keyboard navigation for filters
    const filterTabs = document.querySelectorAll('.filter-tab');
    if (filterTabs.length > 0) {
        filterTabs.forEach((tab, index) => {
            tab.addEventListener('keydown', function(e) {
                let newIndex;
                switch(e.key) {
                    case 'ArrowRight':
                        e.preventDefault();
                        newIndex = (index + 1) % filterTabs.length;
                        filterTabs[newIndex].focus();
                        break;
                    case 'ArrowLeft':
                        e.preventDefault();
                        newIndex = (index - 1 + filterTabs.length) % filterTabs.length;
                        filterTabs[newIndex].focus();
                        break;
                    case 'Home':
                        e.preventDefault();
                        filterTabs[0].focus();
                        break;
                    case 'End':
                        e.preventDefault();
                        filterTabs[filterTabs.length - 1].focus();
                        break;
                }
            });
            
            // Update ARIA attributes when filter is activated
            tab.addEventListener('click', function() {
                filterTabs.forEach(t => t.setAttribute('aria-selected', 'false'));
                this.setAttribute('aria-selected', 'true');
            });
        });
    }
    
    // Enhanced mobile menu accessibility
    const mobileToggle = document.querySelector('.mobile-menu-toggle');
    if (mobileToggle) {
        mobileToggle.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                this.click();
            }
        });
    }
    
    // Skip to main content link (add at top of page)
    const skipLink = document.createElement('a');
    skipLink.href = '#main-content';
    skipLink.textContent = 'Skip to main content';
    skipLink.className = 'skip-link';
    skipLink.style.cssText = `
        position: absolute;
        top: -40px;
        left: 6px;
        background: var(--primary-color);
        color: white;
        padding: 8px;
        text-decoration: none;
        border-radius: 4px;
        z-index: 1000;
        transition: top 0.3s;
    `;
    skipLink.addEventListener('focus', () => {
        skipLink.style.top = '6px';
    });
    skipLink.addEventListener('blur', () => {
        skipLink.style.top = '-40px';
    });
    document.body.insertBefore(skipLink, document.body.firstChild);
    
    // Ensure main content has ID
    const mainContent = document.querySelector('main, .main-content, .page-hero');
    if (mainContent && !mainContent.id) {
        mainContent.id = 'main-content';
    }
    
    // High contrast mode detection
    if (window.matchMedia && window.matchMedia('(prefers-contrast: high)').matches) {
        document.documentElement.classList.add('high-contrast');
    }
    
    // Reduced motion support
    if (window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches) {
        document.documentElement.classList.add('reduced-motion');
    }
}

// Cookie Consent Management
function initCookieConsent() {
    const cookieConsent = localStorage.getItem('cookieConsent');
    
    if (!cookieConsent) {
        showCookieBanner();
    }
    
    function showCookieBanner() {
        const banner = document.createElement('div');
        banner.className = 'cookie-banner';
        banner.setAttribute('role', 'dialog');
        banner.setAttribute('aria-labelledby', 'cookie-banner-title');
        banner.setAttribute('aria-describedby', 'cookie-banner-description');
        banner.innerHTML = `
            <div class="cookie-banner-content">
                <div class="cookie-banner-text">
                    <h3 id="cookie-banner-title">Cookie Notice</h3>
                    <p id="cookie-banner-description">
                        We use essential cookies to ensure our website functions properly. We also use analytics cookies to understand how you interact with our site. 
                        <a href="privacy-policy.html" target="_blank" rel="noopener">Learn more in our Privacy Policy</a>
                    </p>
                </div>
                <div class="cookie-banner-actions">
                    <button class="btn btn-secondary" id="cookie-essential">Essential Only</button>
                    <button class="btn btn-primary" id="cookie-accept-all">Accept All</button>
                </div>
            </div>
        `;
        
        banner.style.cssText = `
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            background: #fff;
            border-top: 4px solid var(--primary-color);
            box-shadow: 0 -8px 25px rgba(0,0,0,0.15);
            z-index: 10000;
            padding: 20px 0;
        `;
        
        // Add cookie banner specific styles
        const style = document.createElement('style');
        style.textContent = `
            .cookie-banner-content {
                max-width: 1200px;
                margin: 0 auto;
                padding: 0 20px;
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 30px;
            }
            .cookie-banner-content h3 {
                margin: 0 0 8px;
                color: var(--primary-color);
                font-size: 1.1rem;
                font-weight: 600;
            }
            .cookie-banner-content p {
                margin: 0;
                color: #374151;
                font-size: 0.9rem;
                line-height: 1.5;
                flex: 1;
            }
            .cookie-banner-content a {
                color: var(--primary-color);
                text-decoration: underline;
            }
            .cookie-banner-actions {
                display: flex;
                gap: 12px;
                flex-shrink: 0;
            }
            .cookie-banner .btn {
                padding: 10px 20px;
                border: none;
                border-radius: 6px;
                font-size: 0.9rem;
                font-weight: 500;
                cursor: pointer;
                transition: all 0.2s ease;
                white-space: nowrap;
            }
            .cookie-banner .btn-secondary {
                background: #f3f4f6;
                color: #374151;
                border: 1px solid #d1d5db;
            }
            .cookie-banner .btn-secondary:hover {
                background: #e5e7eb;
            }
            .cookie-banner .btn-primary {
                background: var(--primary-color);
                color: white;
            }
            .cookie-banner .btn-primary:hover {
                background: var(--primary-dark);
            }
            @media (max-width: 768px) {
                .cookie-banner-content {
                    flex-direction: column;
                    align-items: flex-start;
                    gap: 16px;
                }
                .cookie-banner-actions {
                    width: 100%;
                    justify-content: stretch;
                }
                .cookie-banner .btn {
                    flex: 1;
                }
            }
        `;
        document.head.appendChild(style);
        
        document.body.appendChild(banner);
        
        // Focus management
        banner.querySelector('#cookie-accept-all').focus();
        
        document.getElementById('cookie-essential').addEventListener('click', () => {
            localStorage.setItem('cookieConsent', 'essential');
            banner.remove();
        });
        
        document.getElementById('cookie-accept-all').addEventListener('click', () => {
            localStorage.setItem('cookieConsent', 'all');
            banner.remove();
        });
    }
}

// Initialize cookie consent on page load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initCookieConsent);
} else {
    initCookieConsent();
}

// Newsletter Functionality
document.addEventListener('DOMContentLoaded', function() {
    // Newsletter subscription form
    const newsletterForm = document.getElementById('newsletter-subscribe-form');
    if (newsletterForm) {
        newsletterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const email = document.getElementById('newsletter-email').value;
            
            if (email) {
                // Create mailto link for newsletter subscription
                const subject = encodeURIComponent('Newsletter Subscription Request');
                const body = encodeURIComponent(`Hello,\n\nI would like to subscribe to the Cardily newsletter.\n\nEmail: ${email}\n\nThank you!`);
                const mailtoLink = `mailto:newsletter@cardily.org?subject=${subject}&body=${body}`;
                
                // Open email client
                window.location.href = mailtoLink;
                
                // Show success message
                showNotification('Thank you! Please send the email to complete your subscription.', 'success');
                newsletterForm.reset();
            }
        });
    }
    
    // Content submission form
    const contentForm = document.getElementById('content-submission-form');
    if (contentForm) {
        contentForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(contentForm);
            const contentType = formData.get('contentType');
            const contributorName = formData.get('contributorName');
            const contributorEmail = formData.get('contributorEmail');
            const contentTitle = formData.get('contentTitle');
            const contentDescription = formData.get('contentDescription');
            const contentDetails = formData.get('contentDetails');
            
            // Create email content
            const subject = encodeURIComponent(`Newsletter Content Submission - ${contentType}`);
            let emailBody = `Hello,\n\nI would like to submit content for the Cardily newsletter.\n\n`;
            emailBody += `Content Type: ${contentType}\n`;
            emailBody += `Contributor: ${contributorName}\n`;
            emailBody += `Email: ${contributorEmail}\n`;
            emailBody += `Title: ${contentTitle}\n\n`;
            emailBody += `Description:\n${contentDescription}\n\n`;
            if (contentDetails) {
                emailBody += `Full Content:\n${contentDetails}\n\n`;
            }
            emailBody += `Please find any attached materials in a separate email if applicable.\n\nThank you!`;
            
            const mailtoLink = `mailto:submissions@cardily.org?subject=${subject}&body=${encodeURIComponent(emailBody)}`;
            
            // Open email client
            window.location.href = mailtoLink;
            
            // Show success message and close modal
            showNotification('Thank you! Please send the email to submit your content.', 'success');
            closeContentSubmissionModal();
            contentForm.reset();
        });
    }
});

// Open content submission modal
function openContentSubmissionModal() {
    const modal = document.getElementById('content-submission-modal');
    if (modal) {
        modal.style.display = 'flex';
        document.body.style.overflow = 'hidden';
    }
}

// Close content submission modal
function closeContentSubmissionModal() {
    const modal = document.getElementById('content-submission-modal');
    if (modal) {
        modal.style.display = 'none';
        document.body.style.overflow = 'auto';
    }
}

// Close modal when clicking outside
document.addEventListener('click', function(e) {
    const modal = document.getElementById('content-submission-modal');
    if (modal && e.target === modal) {
        closeContentSubmissionModal();
    }
});

// Show notification function
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <span>${message}</span>
        <button onclick="this.parentElement.remove()" style="background: none; border: none; color: inherit; margin-left: 10px; cursor: pointer;">&times;</button>
    `;
    
    // Add to page
    document.body.appendChild(notification);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentElement) {
            notification.remove();
        }
    }, 5000);
}

// Project Learn More Modal Functions
function openProjectLearnMoreModal(projectName) {
    // Prevent default behavior and stop event propagation
    event?.preventDefault();
    event?.stopPropagation();
    
    console.log('Opening modal for:', projectName);
    
    const modal = document.getElementById('project-learn-more-modal');
    const title = document.getElementById('project-modal-title');
    const projectInput = document.getElementById('selected-project');
    
    if (modal && title && projectInput) {
        // Store current scroll position
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        // Set project information
        title.textContent = `Learn More About ${projectName}`;
        projectInput.value = projectName;
        
        // Show modal
        modal.style.display = 'flex';
        document.body.style.overflow = 'hidden';
        document.body.style.position = 'fixed';
        document.body.style.top = `-${scrollTop}px`;
        document.body.style.width = '100%';
        
        // Store scroll position for restoration
        modal.dataset.scrollTop = scrollTop;
        
        console.log('Modal opened for:', projectName);
        
        // Focus the first input
        setTimeout(() => {
            const firstInput = modal.querySelector('input[type="text"]');
            if (firstInput) {
                firstInput.focus();
            }
        }, 100);
    } else {
        alert(`To learn more about ${projectName}, please contact us at support@cardily.org`);
    }
}

function closeProjectLearnMoreModal() {
    const modal = document.getElementById('project-learn-more-modal');
    const form = document.getElementById('project-learn-more-form');
    
    if (modal) {
        // Restore scroll position
        const scrollTop = modal.dataset.scrollTop || 0;
        
        modal.style.display = 'none';
        document.body.style.overflow = '';
        document.body.style.position = '';
        document.body.style.top = '';
        document.body.style.width = '';
        
        // Restore scroll position
        window.scrollTo(0, parseInt(scrollTop));
        
        if (form) {
            form.reset();
        }
    }
}

// Project Proposal Modal Functions
function openProjectProposalModal() {
    // Prevent default behavior
    event?.preventDefault();
    event?.stopPropagation();
    
    const modal = document.getElementById('project-proposal-modal');
    
    if (modal) {
        // Store current scroll position
        const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
        
        // Show modal
        modal.style.display = 'flex';
        document.body.style.overflow = 'hidden';
        document.body.style.position = 'fixed';
        document.body.style.top = `-${scrollTop}px`;
        document.body.style.width = '100%';
        
        // Store scroll position for restoration
        modal.dataset.scrollTop = scrollTop;
        
        // Focus the first input
        setTimeout(() => {
            const firstInput = modal.querySelector('input[type="text"]');
            if (firstInput) {
                firstInput.focus();
            }
        }, 100);
    } else {
        alert('To submit your project proposal, please contact us at support@cardily.org');
    }
}

function closeProjectProposalModal() {
    const modal = document.getElementById('project-proposal-modal');
    const form = document.getElementById('project-proposal-form');
    
    if (modal) {
        // Restore scroll position
        const scrollTop = modal.dataset.scrollTop || 0;
        
        modal.style.display = 'none';
        document.body.style.overflow = '';
        document.body.style.position = '';
        document.body.style.top = '';
        document.body.style.width = '';
        
        // Restore scroll position
        window.scrollTo(0, parseInt(scrollTop));
        
        if (form) {
            form.reset();
        }
    }
}

// Initialize project forms
document.addEventListener('DOMContentLoaded', function() {
    // Project Learn More form submission
    const learnMoreForm = document.getElementById('project-learn-more-form');
    if (learnMoreForm) {
        learnMoreForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const projectName = formData.get('project');
            const name = formData.get('name');
            const email = formData.get('email');
            const affiliation = formData.get('affiliation');
            const background = formData.get('background');
            const interest = formData.get('interest');
            const questions = formData.get('questions');
            
            // Create email content
            const subject = encodeURIComponent(`Project Inquiry: ${projectName}`);
            let emailBody = `Hello,\n\nI am interested in learning more about the ${projectName} project.\n\n`;
            emailBody += `Contact Information:\n`;
            emailBody += `Name: ${name}\n`;
            emailBody += `Email: ${email}\n`;
            if (affiliation) emailBody += `Affiliation: ${affiliation}\n`;
            emailBody += `Background: ${background}\n\n`;
            if (interest) emailBody += `My Interests:\n${interest}\n\n`;
            if (questions) emailBody += `Questions:\n${questions}\n\n`;
            emailBody += `Thank you for your time. I look forward to hearing from you.\n\nBest regards,\n${name}`;
            
            const mailtoLink = `mailto:support@cardily.org?subject=${subject}&body=${encodeURIComponent(emailBody)}`;
            
            // Open email client
            window.location.href = mailtoLink;
            
            // Show success message and close modal
            showNotification('Thank you! Please send the email to submit your inquiry.', 'success');
            closeProjectLearnMoreModal();
        });
    }
    
    // Project Proposal form submission
    const proposalForm = document.getElementById('project-proposal-form');
    if (proposalForm) {
        proposalForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const formData = new FormData(this);
            const name = formData.get('name');
            const email = formData.get('email');
            const title = formData.get('title');
            const category = formData.get('category');
            const summary = formData.get('summary');
            const objectives = formData.get('objectives');
            const impact = formData.get('impact');
            const timeline = formData.get('timeline');
            const resources = formData.get('resources');
            
            // Create email content
            const subject = encodeURIComponent(`Project Proposal: ${title}`);
            let emailBody = `Hello,\n\nI would like to propose a new project for Cardily.\n\n`;
            emailBody += `Proposer Information:\n`;
            emailBody += `Name: ${name}\n`;
            emailBody += `Email: ${email}\n\n`;
            emailBody += `Project Details:\n`;
            emailBody += `Title: ${title}\n`;
            emailBody += `Category: ${category}\n\n`;
            emailBody += `Summary:\n${summary}\n\n`;
            if (objectives) emailBody += `Objectives:\n${objectives}\n\n`;
            if (impact) emailBody += `Expected Impact:\n${impact}\n\n`;
            if (timeline) emailBody += `Timeline: ${timeline}\n\n`;
            if (resources) emailBody += `Resources Needed:\n${resources}\n\n`;
            emailBody += `I would appreciate the opportunity to discuss this proposal further.\n\nBest regards,\n${name}`;
            
            const mailtoLink = `mailto:support@cardily.org?subject=${subject}&body=${encodeURIComponent(emailBody)}`;
            
            // Open email client
            window.location.href = mailtoLink;
            
            // Show success message and close modal
            showNotification('Thank you! Please send the email to submit your proposal.', 'success');
            closeProjectProposalModal();
        });
    }
});

// Close modals with escape key
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        const learnMoreModal = document.getElementById('project-learn-more-modal');
        const proposalModal = document.getElementById('project-proposal-modal');
        
        if (learnMoreModal && learnMoreModal.style.display === 'flex') {
            closeProjectLearnMoreModal();
        }
        
        if (proposalModal && proposalModal.style.display === 'flex') {
            closeProjectProposalModal();
        }
    }
});

// Close modals when clicking outside
document.addEventListener('click', function(e) {
    const learnMoreModal = document.getElementById('project-learn-more-modal');
    const proposalModal = document.getElementById('project-proposal-modal');
    
    if (learnMoreModal && e.target === learnMoreModal) {
        closeProjectLearnMoreModal();
    }
    
    if (proposalModal && e.target === proposalModal) {
        closeProjectProposalModal();
    }
});

// Ensure functions are available globally
window.openProjectLearnMoreModal = openProjectLearnMoreModal;
window.closeProjectLearnMoreModal = closeProjectLearnMoreModal;
window.openProjectProposalModal = openProjectProposalModal;
window.closeProjectProposalModal = closeProjectProposalModal;

// Add click event listeners as backup
document.addEventListener('DOMContentLoaded', function() {
    console.log('DOM loaded, checking for all modal buttons');
    
    // Find all Learn More buttons and add debug logging
    const learnMoreButtons = document.querySelectorAll('button[onclick*="openProjectLearnMoreModal"]');
    console.log('Found', learnMoreButtons.length, 'Learn More buttons');
    
    learnMoreButtons.forEach(button => {
        console.log('Learn More button onclick:', button.getAttribute('onclick'));
    });
    
    // Find Submit Your Idea button
    const submitIdeaButton = document.querySelector('button[onclick*="openProjectProposalModal"]');
    if (submitIdeaButton) {
        console.log('Found Submit Your Idea button with onclick:', submitIdeaButton.getAttribute('onclick'));
    } else {
        console.error('Submit Your Idea button not found');
    }
    
    // Test if functions are available
    console.log('Functions available:', {
        openProjectLearnMoreModal: typeof window.openProjectLearnMoreModal,
        closeProjectLearnMoreModal: typeof window.closeProjectLearnMoreModal,
        openProjectProposalModal: typeof window.openProjectProposalModal,
        closeProjectProposalModal: typeof window.closeProjectProposalModal
    });
    
    // Check if buttons have onclick attributes working
    const allLearnMoreButtons = document.querySelectorAll('button[onclick*="openProjectLearnMoreModal"]');
    console.log('Found', allLearnMoreButtons.length, 'Learn More buttons with onclick attributes');
    
    allLearnMoreButtons.forEach((button, index) => {
        console.log(`Button ${index + 1} onclick:`, button.getAttribute('onclick'));
    });
});
