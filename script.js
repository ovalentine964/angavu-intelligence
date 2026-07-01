/* ============================================
   BIASHARA INTELLIGENCE — Script
   ============================================ */

document.addEventListener('DOMContentLoaded', () => {
    // --- Navbar scroll effect ---
    const navbar = document.getElementById('navbar');
    const handleScroll = () => {
        if (window.scrollY > 50) {
            navbar.classList.add('scrolled');
        } else {
            navbar.classList.remove('scrolled');
        }
    };
    window.addEventListener('scroll', handleScroll, { passive: true });
    handleScroll();

    // --- Mobile nav toggle ---
    const navToggle = document.getElementById('navToggle');
    const navMenu = document.getElementById('navMenu');

    navToggle.addEventListener('click', () => {
        navToggle.classList.toggle('active');
        navMenu.classList.toggle('active');
        document.body.style.overflow = navMenu.classList.contains('active') ? 'hidden' : '';
    });

    // Close mobile menu on link click
    navMenu.querySelectorAll('a[href^="#"]').forEach(link => {
        link.addEventListener('click', () => {
            navToggle.classList.remove('active');
            navMenu.classList.remove('active');
            document.body.style.overflow = '';
        });
    });

    // --- Language toggle ---
    let currentLang = 'en';
    const langToggle = document.getElementById('langToggle');

    const switchLanguage = (lang) => {
        currentLang = lang;
        document.querySelectorAll('[data-en]').forEach(el => {
            const text = lang === 'en' ? el.getAttribute('data-en') : el.getAttribute('data-sw');
            if (text) {
                el.textContent = text;
            }
        });

        // Update toggle display
        const activeSpan = langToggle.querySelector('.lang-active');
        const inactiveSpan = langToggle.querySelector('.lang-inactive');
        if (lang === 'en') {
            activeSpan.textContent = 'EN';
            inactiveSpan.textContent = 'SW';
        } else {
            activeSpan.textContent = 'SW';
            inactiveSpan.textContent = 'EN';
        }

        // Update html lang attribute
        document.documentElement.lang = lang === 'en' ? 'en' : 'sw';
    };

    langToggle.addEventListener('click', () => {
        switchLanguage(currentLang === 'en' ? 'sw' : 'en');
    });

    // --- Scroll animations (Intersection Observer) ---
    const observerOptions = {
        root: null,
        rootMargin: '0px 0px -80px 0px',
        threshold: 0.1
    };

    const animateOnScroll = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                animateOnScroll.unobserve(entry.target);
            }
        });
    }, observerOptions);

    // Add fade-in class to elements we want to animate
    const animateSelectors = [
        '.section-header',
        '.about-content',
        '.about-mission',
        '.pillar-card',
        '.product-card',
        '.msaidizi-content',
        '.msaidizi-visual',
        '.insights-coming-soon',
        '.community-card',
        '.contact-card',
        '.stat-card'
    ];

    animateSelectors.forEach(selector => {
        document.querySelectorAll(selector).forEach((el, index) => {
            el.classList.add('fade-in');
            el.style.transitionDelay = `${index * 0.1}s`;
            animateOnScroll.observe(el);
        });
    });

    // --- Newsletter form handling ---
    const handleNewsletter = (form) => {
        form.addEventListener('submit', (e) => {
            e.preventDefault();
            const email = form.querySelector('input[type="email"]').value;
            const btn = form.querySelector('button');
            const originalText = btn.textContent;

            btn.textContent = '✓ Subscribed!';
            btn.style.background = '#2a7d3f';
            btn.disabled = true;
            form.querySelector('input').value = '';

            setTimeout(() => {
                btn.textContent = originalText;
                btn.style.background = '';
                btn.disabled = false;
            }, 3000);

            // Log for future integration (do not log email in production)
            // console.log('Newsletter signup:', email);
        });
    };

    const mainNewsletter = document.getElementById('newsletterForm');
    const footerNewsletter = document.getElementById('footerNewsletterForm');
    if (mainNewsletter) handleNewsletter(mainNewsletter);
    if (footerNewsletter) handleNewsletter(footerNewsletter);

    // --- Smooth scroll for anchor links ---
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                e.preventDefault();
                const offset = navbar.offsetHeight + 20;
                const top = target.getBoundingClientRect().top + window.scrollY - offset;
                window.scrollTo({ top, behavior: 'smooth' });
            }
        });
    });

    // --- Active nav link highlighting ---
    const sections = document.querySelectorAll('section[id]');
    const navLinks = document.querySelectorAll('.nav-menu a[href^="#"]');

    const highlightNav = () => {
        const scrollPos = window.scrollY + 200;
        sections.forEach(section => {
            const top = section.offsetTop;
            const height = section.offsetHeight;
            const id = section.getAttribute('id');
            if (scrollPos >= top && scrollPos < top + height) {
                navLinks.forEach(link => {
                    link.style.color = '';
                    if (link.getAttribute('href') === `#${id}`) {
                        link.style.color = 'var(--accent-gold)';
                    }
                });
            }
        });
    };

    window.addEventListener('scroll', highlightNav, { passive: true });

    // --- Parallax effect on hero ---
    const hero = document.querySelector('.hero-bg-pattern');
    window.addEventListener('scroll', () => {
        if (window.scrollY < window.innerHeight) {
            const offset = window.scrollY * 0.3;
            hero.style.transform = `translateY(${offset}px)`;
        }
    }, { passive: true });

    // --- Service Worker Registration ---
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/biashara-intelligence/sw.js')
            .then(reg => console.log('SW registered:', reg.scope))
            .catch(err => console.log('SW registration failed:', err));
    }

    console.log('Biashara Intelligence — Website loaded successfully.');
});
