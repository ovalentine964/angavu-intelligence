/* ========================================
   BIASHARA INTELLIGENCE — Website Scripts
   Professional, corporate, bilingual
   ======================================== */

(function() {
    'use strict';

    // ========== LANGUAGE SYSTEM ==========
    const translations = {
        'en': {
            'nav.home': 'Home',
            'nav.workers': 'For Workers',
            'nav.buyers': 'For Buyers',
            'nav.about': 'About Us',
            'nav.contact': 'Contact',
            'nav.download': 'Get the App',
            'hero.badge': '🇰🇪 Migori, Kenya — Building the future of economic data',
            'hero.title.line1': "Making Africa's",
            'hero.title.line2': 'Invisible Economy',
            'hero.title.line3': 'Visible.',
            'hero.subtitle': '200 million informal workers. $1.3 trillion in economic output. <strong>Zero data. Until now.</strong>',
            'hero.cta.worker': "I'm a Worker",
            'hero.cta.business': "I'm a Business",
            'hero.proof.workers': 'Informal Workers',
            'hero.proof.output': 'Annual Output',
            'hero.proof.digitized': 'Digitized (until now)',
            'problem.label': 'The Problem',
            'problem.title': "85% of Africa's employment is informal. <span>Nobody sees it.</span>",
            'problem.desc': "Governments plan blindly. Banks can't lend. FMCG companies guess demand. Workers don't know if they're making profit.",
            'problem.stat.workers': 'Informal workers in Africa',
            'problem.stat.output': 'Annual economic output',
            'problem.stat.digitized': 'Digitized (until Msaidizi)',
            'problem.stat.protests': 'Deaths in Kenya 2024 protests (governance failure)',
            'problem.quote': '"You can\'t manage what you can\'t measure. And right now, Africa\'s economy is mostly unmeasured."',
            'solution.label': 'The Solution',
            'solution.title': 'Msaidizi — <span>A voice-based AI assistant</span> that works offline on any Android phone',
            'solution.workers.title': 'For Workers',
            'solution.workers.l1': 'Record sales by voice in Swahili',
            'solution.workers.l2': 'Track profit automatically',
            'solution.workers.l3': 'Get business advice',
            'solution.workers.l4': 'Works without internet',
            'solution.workers.l5': 'Free forever',
            'solution.buyers.title': 'For Buyers',
            'solution.buyers.l1': 'Real-time demand data from informal markets',
            'solution.buyers.l2': 'Ground-truth economic intelligence',
            'solution.buyers.l3': 'Anonymized, aggregated, ethical',
            'solution.buyers.l4': 'API access for integration',
            'solution.chat1': 'Leo nimeuza vitu 5 kwa elfu kumi kila moja',
            'solution.chat2': 'Sawa! Mauzo ya leo: 50,000. Gharama: 30,000. Faida: 20,000. Kazi nzuri! 🎉',
            'solution.chat3': 'Naomba deni ya Bi Mwana',
            'solution.chat4': 'Bi Mwana anadaiwa 5,000. Aliahidi kulipa Ijumaa.',
            'solution.chat.placeholder': '🎤 Speak or type...',
            'workers.label': 'For Workers',
            'workers.title': 'Sema na biashara yako. <span>Simama na maarifa.</span>',
            'workers.subtitle': 'Speak to your business. Stand with knowledge. Msaidizi is your free voice-based business assistant that works offline.',
            'workers.step1.title': 'Speak',
            'workers.step1.desc': 'Tell Msaidizi your sales in Swahili. "Nimeuza vitu 5 kwa elfu kumi."',
            'workers.step2.title': 'Understand',
            'workers.step2.desc': 'Msaidizi records, calculates, and remembers everything for you.',
            'workers.step3.title': 'Grow',
            'workers.step3.desc': 'Know your profit. Make better decisions. Grow your business.',
            'workers.download': 'Download Msaidizi APK',
            'workers.meta': 'Android 6.0+ · 15MB · Free forever · No ads',
            'workers.community': 'Join 1,000+ entrepreneurs in our WhatsApp community:',
            'workers.whatsapp': 'Join WhatsApp Group',
            'workers.card.voice.title': 'Voice Input',
            'workers.card.voice.desc': 'Speak your sales in Swahili or Sheng. No typing needed.',
            'workers.card.offline.title': 'Works Offline',
            'workers.card.offline.desc': 'No internet? No problem. Everything works on your phone.',
            'workers.card.profit.title': 'Profit Tracking',
            'workers.card.profit.desc': "See your daily profit and loss. Know if you're making money.",
            'workers.card.debts.title': 'Debt Memory',
            'workers.card.debts.desc': 'Never forget who owes you. Msaidizi remembers every debt.',
            'buyers.label': 'For Buyers',
            'buyers.title': "Economic Intelligence from <span>Africa's Informal Economy</span>",
            'buyers.desc': "Real-time, ground-truth data from 100,000+ informal markets. Anonymized. Aggregated. Ethical.",
            'buyers.product.demand.title': 'Demand Forecasting',
            'buyers.product.demand.desc': 'Real-time demand patterns from 100,000+ informal markets. Know what sells, where, and when.',
            'buyers.product.demand.tag': 'FMCG · Retail · Distribution',
            'buyers.product.heatmap.title': 'Economic Heatmaps',
            'buyers.product.heatmap.desc': 'Activity maps for infrastructure planning. See where economic activity concentrates.',
            'buyers.product.heatmap.tag': 'Government · NGOs · Development',
            'buyers.product.credit.title': 'Credit Scoring',
            'buyers.product.credit.desc': 'Transaction-based lending signals for the unbanked. Lend with confidence.',
            'buyers.product.credit.tag': 'Banks · Microfinance · Fintech',
            'buyers.product.policy.title': 'Policy Impact',
            'buyers.product.policy.desc': 'Measure policy effects on MSMEs in real-time. See the impact before the reports come in.',
            'buyers.product.policy.tag': 'Government · Research · Development',
            'buyers.categories.title': 'Who Buys Our Intelligence?',
            'buyers.cat.fmcg.title': 'FMCG Companies',
            'buyers.cat.fmcg.desc': '"Know what dukawallahs sell before your distributors do."',
            'buyers.cat.gov.title': 'Government',
            'buyers.cat.gov.desc': '"Plan with real data, not estimates."',
            'buyers.cat.banks.title': 'Banks',
            'buyers.cat.banks.desc': '"Lend to the unbanked with confidence."',
            'buyers.cat.ngo.title': 'NGOs',
            'buyers.cat.ngo.desc': '"Measure impact with ground-truth data."',
            'buyers.cta.title': "Ready to see Africa's informal economy?",
            'buyers.cta.desc': 'Request a demo and discover how ground-truth economic intelligence can transform your business.',
            'buyers.cta.whatsapp': 'Request a Demo via WhatsApp',
            'buyers.cta.email': 'Email Us',
            'pilot.label': 'Pilot Program',
            'pilot.title': 'Be Among Our <span>First Users</span>',
            'pilot.desc': "Msaidizi is launching with a pilot in Migori markets. We're starting small — real workers, real businesses, real data. No fake reviews. No inflated numbers. Just honest technology built for people who need it.",
            'pilot.card1.title': 'Starting with Gikomba',
            'pilot.card1.desc': 'Our first users are market vendors in Gikomba, Migori. Real dukawallahs and mama mbogas testing Msaidizi with their daily transactions.',
            'pilot.card2.title': 'Real Data Only',
            'pilot.card2.desc': "Every number on this site comes from real transactions. No projections disguised as facts. We'll publish actual metrics as our pilot progresses.",
            'pilot.card3.title': 'Join the Pilot',
            'pilot.card3.desc': 'Are you a market vendor in Migori? Download Msaidizi and be part of the first group to ever see their business data in real time.',
            'pilot.join': 'Join the Pilot',
            'about.label': 'About Us',
            'about.title': 'Biashara Intelligence — <span>Migori, Kenya</span>',
            'about.mission.title': 'Our Mission',
            'about.mission.text': "To make Africa's invisible economy visible, one transaction at a time.",
            'about.story.title': 'Our Story',
            'about.story.p1': "Started with one question: <strong>Why does my mum's business have no data?</strong>",
            'about.story.p2': 'She sells mandazi in Gikomba. She works harder than any CEO. But no bank sees her. No government counts her. No company studies her market.',
            'about.story.p3': "Biashara Intelligence changes that. We're building the data infrastructure for Africa's informal economy — starting with the workers themselves.",
            'about.team.title': 'The Team',
            'about.team.valentine.role': 'Founder & CEO',
            'about.team.valentine.bio': "BSc Economics & Statistics. Passionate about using data to empower Africa's informal economy.",
            'about.team.future.name': 'You?',
            'about.team.future.role': 'Future Team Member',
            'about.team.future.bio': "We're looking for mission-driven people. Interested? Get in touch.",
            'contact.label': 'Contact',
            'contact.title': "Let's Talk",
            'contact.desc': "Whether you're a worker, a business, an investor, or a journalist — we'd love to hear from you.",
            'contact.email.title': 'Email',
            'contact.location': 'Migori, Kenya',
            'footer.desc': "Making Africa's invisible economy visible. Built in Migori for Africa's 200 million informal workers.",
            'footer.product': 'Product',
            'footer.app': 'Msaidizi App',
            'footer.intelligence': 'Intelligence Products',
            'footer.changelog': 'Changelog',
            'footer.company': 'Company',
            'footer.about': 'About Us',
            'footer.contact': 'Contact',
            'footer.github': 'GitHub',
            'footer.connect': 'Connect',
            'footer.whatsapp': 'WhatsApp Community',
            'footer.rights': 'All rights reserved.',
            'footer.made': "Built in Migori for Africa's 200 million informal workers 🌍"
        },
        'sw': {
            'nav.home': 'Nyumbani',
            'nav.workers': 'Kwa Wafanyakazi',
            'nav.buyers': 'Kwa Wanunuzi',
            'nav.about': 'Kutuhusu',
            'nav.contact': 'Wasiliana',
            'nav.download': 'Pata Programu',
            'hero.badge': '🇰🇪 Migori, Kenya — Tunajenga mustakabali wa data ya kiuchumi',
            'hero.title.line1': 'Kufanya Uchumi',
            'hero.title.line2': 'Usioonekana wa Afrika',
            'hero.title.line3': 'Uonekane.',
            'hero.subtitle': 'Wafanyakazi milioni 200 wasio rasmi. Pato la dola trilioni 1.3. <strong>Hakuna data. Hadi sasa.</strong>',
            'hero.cta.worker': 'Mimi ni Mfanyakazi',
            'hero.cta.business': 'Mimi ni Biashara',
            'hero.proof.workers': 'Wafanyakazi Wasio Rasmi',
            'hero.proof.output': 'Pato la Mwaka',
            'hero.proof.digitized': 'Imedigitalishwa (hadi sasa)',
            'problem.label': 'Tatizo',
            'problem.title': "85% ya ajira ya Afrika ni isiyo rasmi. <strong>Hakuna mtu anaiona.</strong>",
            'problem.desc': "Serikali zinapanga kwa upofu. Benki hazikopeshi. Kampuni za FMCG zinadhani mahitaji. Wafanyakazi hawajui kama wanapata faida.",
            'problem.stat.workers': 'Wafanyakazi wasio rasmi Afrika',
            'problem.stat.output': 'Pato la mwaka la kiuchumi',
            'problem.stat.digitized': 'Imedigitalishwa (hadi Msaidizi)',
            'problem.stat.protests': 'Vifo vya maandamano ya Kenya 2024 (ushindani wa utawala)',
            'problem.quote': '"Huwezi kusimamia usichopima. Na sasa, uchumi wa Afrika haujapimwa.',
            'solution.label': 'Suluhisho',
            'solution.title': 'Msaidizi — <strong>Msaidizi wa AI unaotumia sauti</strong> unaofanya kazi nje ya mtandao kwenye simu yoyote ya Android',
            'solution.workers.title': 'Kwa Wafanyakazi',
            'solution.workers.l1': 'Rekodi mauzo kwa sauti kwa Kiswahili',
            'solution.workers.l2': 'Fuatilia faida kiotomatiki',
            'solution.workers.l3': 'Pata ushauri wa biashara',
            'solution.workers.l4': 'Inafanya kazi bila mtandao',
            'solution.workers.l5': 'Bure milele',
            'solution.buyers.title': 'Kwa Wanunuzi',
            'solution.buyers.l1': 'Data ya mahitaji ya wakati halisi kutoka masoko yasiyo rasmi',
            'solution.buyers.l2': 'Ujasusi wa kiuchumi wa ukweli',
            'solution.buyers.l3': 'Imefichwa, imekusanywa, ya kimaadili',
            'solution.buyers.l4': 'Upatikanaji wa API',
            'workers.label': 'Kwa Wafanyakazi',
            'workers.title': 'Sema na biashara yako. <span>Simama na maarifa.</span>',
            'workers.subtitle': 'Ongea na biashara yako. Simama na maarifa. Msaidizi ni msaidizi wako wa biashara unaotumia sauti na kufanya kazi nje ya mtandao.',
            'about.label': 'Kutuhusu',
            'about.title': 'Biashara Intelligence — <span>Migori, Kenya</span>',
            'about.mission.title': 'Dhamira Yetu',
            'about.mission.text': 'Kufanya uchumi usioonekana wa Afrika uonekane, miamala moja kwa wakati.',
            'about.story.title': 'Hadithi Yetu',
            'about.story.p1': '<strong>Kwa nini biashara ya mama yangu haina data?</strong>',
            'contact.label': 'Wasiliana',
            'contact.title': 'Tuongee',
            'contact.desc': 'Iwe wewe ni mfanyakazi, biashara, mwekezaji, au mwandishi — tungependa kusikia kutoka kwako.',
            'footer.desc': 'Kufanya uchumi usioonekana wa Afrika uonekane. Imejengwa Migori kwa wafanyakazi milioni 200 wasio rasmi wa Afrika.'
        }
    };

    // Merge comprehensive Swahili translations from external file
    if (window.SwahiliContent) {
        Object.assign(translations.sw, window.SwahiliContent);
    }

    let currentLang = 'en';

    // ========== DOM READY ==========
    document.addEventListener('DOMContentLoaded', function() {
        initNavigation();
        initLanguageToggle();
        initScrollAnimations();
        initCounterAnimations();
        initScrollToTop();
        initSmoothScroll();
    });

    // ========== NAVIGATION ==========
    function initNavigation() {
        const nav = document.getElementById('nav');
        const hamburger = document.getElementById('hamburger');
        const mobileMenu = document.getElementById('mobile-menu');

        // Sticky navigation
        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 50) {
                nav.classList.add('scrolled');
            } else {
                nav.classList.remove('scrolled');
            }
        });

        // Mobile menu toggle
        if (hamburger && mobileMenu) {
            hamburger.addEventListener('click', function() {
                hamburger.classList.toggle('active');
                mobileMenu.classList.toggle('active');
                document.body.style.overflow = mobileMenu.classList.contains('active') ? 'hidden' : '';
            });

            // Close mobile menu on link click
            mobileMenu.querySelectorAll('a').forEach(function(link) {
                link.addEventListener('click', function() {
                    hamburger.classList.remove('active');
                    mobileMenu.classList.remove('active');
                    document.body.style.overflow = '';
                });
            });
        }
    }

    // ========== LANGUAGE TOGGLE ==========
    function initLanguageToggle() {
        const btns = document.querySelectorAll('.lang-toggle__btn');
        if (!btns.length) return;

        btns.forEach(function(btn) {
            btn.addEventListener('click', function() {
                const lang = this.getAttribute('data-lang');
                if (lang === currentLang) return;

                currentLang = lang;
                btns.forEach(function(b) {
                    b.classList.remove('active');
                    b.setAttribute('aria-pressed', 'false');
                });
                this.classList.add('active');
                this.setAttribute('aria-pressed', 'true');
                applyTranslations();
            });
        });
    }

    function applyTranslations() {
        const elements = document.querySelectorAll('[data-i18n]');
        elements.forEach(function(el) {
            const key = el.getAttribute('data-i18n');
            const translationKey = 'data-i18n-' + currentLang;
            const translated = el.getAttribute(translationKey);

            if (translated) {
                if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
                    el.placeholder = translated;
                } else {
                    el.innerHTML = translated;
                }
            } else if (translations[currentLang] && translations[currentLang][key]) {
                if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
                    el.placeholder = translations[currentLang][key];
                } else {
                    el.innerHTML = translations[currentLang][key];
                }
            }
        });
    }

    // ========== SCROLL ANIMATIONS ==========
    function initScrollAnimations() {
        const observerOptions = {
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        };

        const observer = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add('visible');
                    observer.unobserve(entry.target);
                }
            });
        }, observerOptions);

        // Observe all fade-in elements
        document.querySelectorAll('.fade-in').forEach(function(el, index) {
            // Add stagger delay based on position in parent
            const parent = el.parentElement;
            const siblings = parent ? Array.from(parent.querySelectorAll('.fade-in')) : [];
            const siblingIndex = siblings.indexOf(el);
            if (siblingIndex > 0 && siblingIndex <= 4) {
                el.style.transitionDelay = (siblingIndex * 0.1) + 's';
            }
            observer.observe(el);
        });
    }

    // ========== COUNTER ANIMATIONS ==========
    function initCounterAnimations() {
        const counters = document.querySelectorAll('[data-count]');

        const observerOptions = {
            threshold: 0.5
        };

        const observer = new IntersectionObserver(function(entries) {
            entries.forEach(function(entry) {
                if (entry.isIntersecting) {
                    animateCounter(entry.target);
                    observer.unobserve(entry.target);
                }
            });
        }, observerOptions);

        counters.forEach(function(counter) {
            observer.observe(counter);
        });
    }

    function animateCounter(element) {
        const target = parseInt(element.getAttribute('data-count'));
        const duration = 2000;
        const startTime = performance.now();

        function update(currentTime) {
            const elapsed = currentTime - startTime;
            const progress = Math.min(elapsed / duration, 1);
            const easeOutQuart = 1 - Math.pow(1 - progress, 4);
            const current = Math.floor(target * easeOutQuart);

            element.textContent = current.toLocaleString();

            if (progress < 1) {
                requestAnimationFrame(update);
            }
        }

        requestAnimationFrame(update);
    }

    // ========== SCROLL TO TOP ==========
    function initScrollToTop() {
        // Create scroll-to-top button if it doesn't exist
        let scrollTopBtn = document.querySelector('.scroll-top');
        if (!scrollTopBtn) {
            scrollTopBtn = document.createElement('button');
            scrollTopBtn.className = 'scroll-top';
            scrollTopBtn.innerHTML = '↑';
            scrollTopBtn.setAttribute('aria-label', 'Scroll to top');
            document.body.appendChild(scrollTopBtn);
        }

        window.addEventListener('scroll', function() {
            if (window.pageYOffset > 500) {
                scrollTopBtn.classList.add('visible');
            } else {
                scrollTopBtn.classList.remove('visible');
            }
        });

        scrollTopBtn.addEventListener('click', function() {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });
    }

    // ========== SMOOTH SCROLL ==========
    function initSmoothScroll() {
        document.querySelectorAll('a[href^="#"]').forEach(function(anchor) {
            anchor.addEventListener('click', function(e) {
                const targetId = this.getAttribute('href');
                if (targetId === '#') return;

                const target = document.querySelector(targetId);
                if (!target) return;

                e.preventDefault();

                const nav = document.getElementById('nav');
                const navHeight = nav ? nav.offsetHeight : 72;
                const targetPosition = target.offsetTop - navHeight - 20;

                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            });
        });
    }

    // ========== KEYBOARD NAVIGATION ==========
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape') {
            const mobileMenu = document.getElementById('mobile-menu');
            const hamburger = document.getElementById('hamburger');
            if (mobileMenu && mobileMenu.classList.contains('active')) {
                mobileMenu.classList.remove('active');
                hamburger.classList.remove('active');
                document.body.style.overflow = '';
            }
        }
    });

})();
