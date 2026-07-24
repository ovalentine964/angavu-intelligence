/* ============================================
   ANGAVU INTELLIGENCE — Main Script v2.0
   Download logic, WhatsApp share, language toggle
   Optimized for 2G/3G — minimal JS, no deps
   ============================================ */

(function() {
    'use strict';

    // ── Constants ──
    var APK_URL = 'https://github.com/ovalentine964/msaidizi-app/releases/download/latest/msaidizi-release.apk';
    var APK_FILENAME = 'msaidizi-v2.1.0.apk';
    var APK_SIZE = '500MB';
    var SITE_URL = 'https://ovalentine964.github.io/angavu-intelligence/';

    // ── Navbar scroll ──
    var navbar = document.getElementById('navbar');
    if (navbar) {
        var onScroll = function() {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        };
        window.addEventListener('scroll', onScroll, { passive: true });
        onScroll();
    }

    // ── Mobile nav toggle ──
    var navToggle = document.getElementById('navToggle');
    var navMenu = document.getElementById('navMenu');
    if (navToggle && navMenu) {
        navToggle.addEventListener('click', function() {
            var isActive = navMenu.classList.toggle('active');
            navToggle.classList.toggle('active');
            document.body.style.overflow = isActive ? 'hidden' : '';
            navToggle.setAttribute('aria-expanded', isActive);
        });
        // Close on link click
        navMenu.querySelectorAll('a').forEach(function(link) {
            link.addEventListener('click', function() {
                navMenu.classList.remove('active');
                navToggle.classList.remove('active');
                document.body.style.overflow = '';
            });
        });
    }

    // ── Smooth scroll for anchors ──
    document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
        anchor.addEventListener('click', function(e) {
            var href = this.getAttribute('href');
            if (href === '#') return;
            var target = document.querySelector(href);
            if (target) {
                e.preventDefault();
                var offset = navbar ? navbar.offsetHeight + 20 : 80;
                var top = target.getBoundingClientRect().top + window.scrollY - offset;
                window.scrollTo({ top: top, behavior: 'smooth' });
            }
        });
    });

    // ── Active nav link ──
    var sections = document.querySelectorAll('section[id]');
    var navLinks = document.querySelectorAll('.nav-menu a[href^="#"]');
    if (sections.length && navLinks.length) {
        window.addEventListener('scroll', function() {
            var scrollPos = window.scrollY + 200;
            sections.forEach(function(section) {
                var top = section.offsetTop;
                var height = section.offsetHeight;
                var id = section.getAttribute('id');
                if (scrollPos >= top && scrollPos < top + height) {
                    navLinks.forEach(function(link) {
                        link.style.color = '';
                        if (link.getAttribute('href') === '#' + id) {
                            link.style.color = '#E8A838';
                        }
                    });
                }
            });
        }, { passive: true });
    }

    // ── Language Toggle (data-sw / data-en attributes) ──
    var langToggle = document.getElementById('langToggle');
    var announcement = document.getElementById('lang-announcement');
    var currentLang = localStorage.getItem('angavu-lang') || 'sw';

    function applyLang(lang) {
        document.querySelectorAll('[data-' + lang + ']').forEach(function(el) {
            var text = el.getAttribute('data-' + lang);
            if (text !== null) el.innerHTML = text;
        });
        if (langToggle) {
            langToggle.textContent = lang === 'sw' ? '\u{1F1F8}\u{1F1F3} EN' : '\u{1F1EC}\u{1F1E7} SW';
            langToggle.setAttribute('aria-label', lang === 'sw' ? 'Switch to English' : 'Badilisha Kiswahili');
        }
        document.documentElement.lang = lang;
        // Update meta OG locale
        var ogLocale = document.querySelector('meta[property="og:locale"]');
        if (ogLocale) ogLocale.setAttribute('content', lang === 'sw' ? 'sw_KE' : 'en_KE');
    }

    applyLang(currentLang);

    if (langToggle) {
        langToggle.addEventListener('click', function() {
            currentLang = currentLang === 'sw' ? 'en' : 'sw';
            localStorage.setItem('angavu-lang', currentLang);
            applyLang(currentLang);
            if (announcement) {
                announcement.textContent = currentLang === 'en' ? 'Language changed to English' : 'Lugha imebadilishwa Kiswahili';
            }
        });
    }

    // ── Auto-download APK ──
    window.downloadAPK = function(e) {
        if (e) e.preventDefault();
        // Trigger download
        var link = document.createElement('a');
        link.href = APK_URL;
        link.download = APK_FILENAME;
        link.setAttribute('rel', 'noopener');
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        // Track if analytics available
        if (typeof gtag === 'function') {
            gtag('event', 'download', { 'event_category': 'APK', 'event_label': APK_FILENAME });
        }
    };

    // ── WhatsApp Share ──
    window.shareWhatsApp = function(customText) {
        var text = customText || 'Pakua Msaidizi \u2014 Msaidizi wako wa biashara! Sauti kwanza. Bure milele.\n\n' + SITE_URL + 'download.html';
        var url = 'https://wa.me/?text=' + encodeURIComponent(text);
        window.open(url, '_blank', 'noopener');
    };

    // ── QR Code Generator (inline, no external lib) ──
    window.generateQR = function(containerId, data, size) {
        var container = document.getElementById(containerId);
        if (!container) return;
        size = size || 140;
        // Use Google Charts QR API as fallback (lightweight)
        var img = document.createElement('img');
        img.src = 'https://api.qrserver.com/v1/create-qr-code/?size=' + size + 'x' + size + '&data=' + encodeURIComponent(data);
        img.alt = 'QR Code';
        img.width = size;
        img.height = size;
        img.loading = 'lazy';
        img.style.borderRadius = '12px';
        img.style.background = '#fff';
        img.style.padding = '8px';
        container.appendChild(img);
    };

    // ── FAQ Accordion ──
    document.querySelectorAll('.faq-question').forEach(function(btn) {
        btn.addEventListener('click', function() {
            var expanded = btn.getAttribute('aria-expanded') === 'true';
            var answer = document.getElementById(btn.getAttribute('aria-controls'));
            btn.setAttribute('aria-expanded', !expanded);
            if (answer) answer.hidden = expanded;
            var icon = btn.querySelector('.faq-icon');
            if (icon) icon.textContent = expanded ? '+' : '\u2212';
        });
    });

    // ── Contact Form ──
    var contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            e.preventDefault();
            var btn = contactForm.querySelector('button[type="submit"]');
            var originalText = btn.textContent;
            btn.textContent = '\u2713 Ujumbe umetumwa!';
            btn.style.background = '#2a7d3f';
            btn.disabled = true;
            contactForm.reset();
            setTimeout(function() {
                btn.textContent = originalText;
                btn.style.background = '';
                btn.disabled = false;
            }, 3000);
        });
    }

    // ── Service Worker Registration ──
    if ('serviceWorker' in navigator) {
        window.addEventListener('load', function() {
            navigator.serviceWorker.register('sw.js').catch(function() {});
        });
    }

    console.log('Angavu Intelligence \u2014 Website v2.0 loaded.');
})();
