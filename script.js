/* ================================================================
   ANGAVU INTELLIGENCE — Enterprise Interactions
   ================================================================ */

(function () {
  'use strict';

  // --- Navigation Scroll Effect ---
  const nav = document.querySelector('.nav');
  if (nav) {
    let lastScroll = 0;
    const handleScroll = () => {
      const currentScroll = window.scrollY;
      if (currentScroll > 50) {
        nav.classList.add('scrolled');
      } else {
        nav.classList.remove('scrolled');
      }
      lastScroll = currentScroll;
    };
    window.addEventListener('scroll', handleScroll, { passive: true });
    handleScroll();
  }

  // --- Mobile Menu ---
  const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
  const mobileMenu = document.querySelector('.mobile-menu');
  if (mobileMenuBtn && mobileMenu) {
    mobileMenuBtn.addEventListener('click', () => {
      const isOpen = mobileMenu.classList.toggle('open');
      mobileMenuBtn.setAttribute('aria-expanded', isOpen);
      // Toggle icon
      const icon = mobileMenuBtn.querySelector('svg');
      if (icon) {
        icon.innerHTML = isOpen
          ? '<line x1="18" y1="6" x2="6" y2="18"/><line x1="6" y1="6" x2="18" y2="18"/>'
          : '<line x1="3" y1="12" x2="21" y2="12"/><line x1="3" y1="6" x2="21" y2="6"/><line x1="3" y1="18" x2="21" y2="18"/>';
      }
    });
    // Close on link click
    mobileMenu.querySelectorAll('a').forEach(link => {
      link.addEventListener('click', () => {
        mobileMenu.classList.remove('open');
        mobileMenuBtn.setAttribute('aria-expanded', 'false');
      });
    });
  }

  // --- Scroll-triggered Animations (IntersectionObserver) ---
  const animateElements = document.querySelectorAll('.animate-on-scroll');
  if (animateElements.length > 0 && 'IntersectionObserver' in window) {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('is-visible');
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.1, rootMargin: '0px 0px -50px 0px' }
    );
    animateElements.forEach((el) => observer.observe(el));
  } else {
    // Fallback: show all immediately
    animateElements.forEach((el) => el.classList.add('is-visible'));
  }

  // --- Animated Counter ---
  function animateCounter(element, target, duration) {
    const start = 0;
    const startTime = performance.now();
    const suffix = element.dataset.suffix || '';
    const prefix = element.dataset.prefix || '';

    function update(currentTime) {
      const elapsed = currentTime - startTime;
      const progress = Math.min(elapsed / duration, 1);
      // Ease out cubic
      const eased = 1 - Math.pow(1 - progress, 3);
      const current = Math.floor(start + (target - start) * eased);
      element.textContent = prefix + current.toLocaleString() + suffix;
      if (progress < 1) {
        requestAnimationFrame(update);
      }
    }
    requestAnimationFrame(update);
  }

  const counters = document.querySelectorAll('[data-count]');
  if (counters.length > 0 && 'IntersectionObserver' in window) {
    const counterObserver = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            const el = entry.target;
            const target = parseInt(el.dataset.count, 10);
            const duration = parseInt(el.dataset.duration || '2000', 10);
            animateCounter(el, target, duration);
            counterObserver.unobserve(el);
          }
        });
      },
      { threshold: 0.5 }
    );
    counters.forEach((el) => counterObserver.observe(el));
  }

  // --- FAQ Accordion ---
  document.querySelectorAll('.faq-question').forEach((btn) => {
    btn.addEventListener('click', () => {
      const item = btn.closest('.faq-item');
      const isOpen = item.classList.contains('open');
      // Close all others
      document.querySelectorAll('.faq-item.open').forEach((openItem) => {
        if (openItem !== item) openItem.classList.remove('open');
      });
      item.classList.toggle('open', !isOpen);
    });
  });

  // --- Language Toggle ---
  const langToggle = document.querySelector('.lang-toggle');
  if (langToggle) {
    let currentLang = 'en';
    langToggle.addEventListener('click', (e) => {
      e.preventDefault();
      currentLang = currentLang === 'en' ? 'sw' : 'en';
      document.querySelectorAll('[data-en]').forEach((el) => {
        const text = el.dataset[currentLang];
        if (text) el.textContent = text;
      });
      langToggle.textContent = currentLang === 'en' ? 'Kiswahili' : 'English';
    });
  }

  // --- WhatsApp Share ---
  window.shareWhatsApp = function (text) {
    const url = encodeURIComponent(window.location.href);
    const msg = encodeURIComponent(text || document.title);
    window.open(`https://wa.me/?text=${msg}%20${url}`, '_blank');
  };

  // --- Smooth Scroll for anchor links ---
  document.querySelectorAll('a[href^="#"]').forEach((anchor) => {
    anchor.addEventListener('click', function (e) {
      const target = document.querySelector(this.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

  // --- Copy Code Block ---
  document.querySelectorAll('.code-block').forEach((block) => {
    const wrapper = document.createElement('div');
    wrapper.style.position = 'relative';
    block.parentNode.insertBefore(wrapper, block);
    wrapper.appendChild(block);

    const btn = document.createElement('button');
    btn.className = 'copy-btn';
    btn.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1"/></svg>';
    btn.style.cssText = 'position:absolute;top:0.75rem;right:0.75rem;background:rgba(255,255,255,0.1);border:1px solid rgba(255,255,255,0.2);border-radius:6px;padding:0.375rem;color:#94a3b8;cursor:pointer;transition:all 150ms;z-index:2;';
    btn.addEventListener('mouseenter', () => { btn.style.background = 'rgba(255,255,255,0.2)'; btn.style.color = '#fff'; });
    btn.addEventListener('mouseleave', () => { btn.style.background = 'rgba(255,255,255,0.1)'; btn.style.color = '#94a3b8'; });
    btn.addEventListener('click', async () => {
      try {
        await navigator.clipboard.writeText(block.textContent);
        btn.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>';
        setTimeout(() => {
          btn.innerHTML = '<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2" ry="2"/><path d="M5 15H4a2 2 0 01-2-2V4a2 2 0 012-2h9a2 2 0 012 2v1"/></svg>';
        }, 2000);
      } catch (err) {
        console.error('Copy failed', err);
      }
    });
    wrapper.appendChild(btn);
  });

  // --- Parallax on hero orbs ---
  const orbs = document.querySelectorAll('.orb');
  if (orbs.length > 0) {
    window.addEventListener('mousemove', (e) => {
      const x = (e.clientX / window.innerWidth - 0.5) * 2;
      const y = (e.clientY / window.innerHeight - 0.5) * 2;
      orbs.forEach((orb, i) => {
        const speed = (i + 1) * 15;
        orb.style.transform = `translate(${x * speed}px, ${y * speed}px)`;
      });
    }, { passive: true });
  }

  // --- Stagger animation helper ---
  window.staggerChildren = function (parentSelector, childSelector, delay) {
    document.querySelectorAll(parentSelector).forEach((parent) => {
      const children = parent.querySelectorAll(childSelector);
      children.forEach((child, i) => {
        child.style.animationDelay = `${i * (delay || 100)}ms`;
      });
    });
  };

})();

// ====== LIVE MARKET TICKER ======
(function () {
  'use strict';

  var tickerData = [
    // Category A: Commodity Prices
    { emoji: '🍅', name: 'Tomatoes', location: 'Nairobi', price: 'KES 120', change: 5.2, source: 'Gikomba Market', unit: '1 kg' },
    { emoji: '🌽', name: 'Maize flour', location: 'Migori', price: 'KES 165', change: -1.8, source: 'Migori Central', unit: '2 kg' },
    { emoji: '🫒', name: 'Cooking oil', location: 'Lagos', price: '₦2,800', change: 3.1, source: 'Oshodi Market', unit: '1 L' },
    { emoji: '🥬', name: 'Sukuma wiki', location: 'Nairobi', price: 'KES 30', change: 0, source: 'Wakulima Market', unit: '1 bunch' },
    { emoji: '🪵', name: 'Charcoal', location: 'Kampala', price: 'UGX 35,000', change: 8.4, source: 'Nakasero Market', unit: '4 kg bag' },
    { emoji: '🐟', name: 'Tilapia', location: 'Dar es Salaam', price: 'TZS 12,000', change: -2.0, source: 'Kariakoo Market', unit: '1 kg' },
    { emoji: '🍚', name: 'Rice', location: 'Accra', price: 'GH₵ 18.50', change: 1.2, source: 'Makola Market', unit: '1 kg' },
    { emoji: '🧅', name: 'Onions', location: 'Addis Ababa', price: 'ETB 85', change: 4.5, source: 'Merkato', unit: '1 kg' },
    { emoji: '🍞', name: 'Bread', location: 'Nairobi', price: 'KES 65', change: 1.5, source: 'Eastlands', unit: '400g loaf' },
    { emoji: '🥛', name: 'Milk', location: 'Kisumu', price: 'KES 60', change: -0.5, source: 'Kisumu Market', unit: '500ml' },
    { emoji: '🥩', name: 'Beef', location: 'Nairobi', price: 'KES 650', change: 2.3, source: 'City Market', unit: '1 kg' },
    { emoji: '🥔', name: 'Irish potatoes', location: 'Nakuru', price: 'KES 80', change: -3.1, source: 'Nakuru Town', unit: '1 kg' },

    // Category B: Transaction / Volume
    { emoji: '📱', name: 'M-Pesa Transactions', location: 'Kenya', price: '48.2M', change: 12.0, source: 'Today' },
    { emoji: '👥', name: 'Msaidizi Users', location: 'Active', price: '12,847', change: 8.3, source: 'This Hour' },
    { emoji: '💰', name: 'Avg. Daily Revenue', location: 'Nairobi workers', price: 'KES 1,450', change: 2.1, source: 'Msaidizi Data' },
    { emoji: '📊', name: 'Transactions Tracked', location: 'Today', price: '2.3M', change: 15.7, source: 'All Markets' },
    { emoji: '🆕', name: 'New Workers', location: 'This Week', price: '8,421', change: 22.4, source: 'Onboarded' },

    // Category C: Macro Pulse (some featured)
    { emoji: '📈', name: 'Kenya Informal GDP', location: '', price: 'KES 3.2T', change: 0.8, source: '56% of GDP', featured: true },
    { emoji: '🌍', name: 'Africa Informal Employment', location: '', price: '85.7%', change: 0.1, source: 'ILO Estimate', featured: true },
    { emoji: '📊', name: 'Alama Score (Avg)', location: 'Informal workers', price: '342', change: 5.0, source: 'Credit readiness', featured: true },
    { emoji: '🔄', name: 'EAC Trade Index', location: 'Cross-border', price: '118.4', change: 2.3, source: 'Regional trade' }
  ];

  function buildTickerItem(item) {
    var div = document.createElement('div');
    div.className = 'ticker-item' + (item.featured ? ' ticker-featured' : '');

    var dir = item.change > 0 ? 'up' : item.change < 0 ? 'down' : 'flat';
    var arrow = dir === 'up' ? '▲' : dir === 'down' ? '▼' : '—';

    var html = '<span class="ticker-commodity">' + item.emoji + ' ' + item.name;
    if (item.location) html += ' · ' + item.location;
    html += '</span>';
    html += '<span class="ticker-price">' + item.price + '</span>';

    if (item.featured) {
      var points = [];
      for (var i = 0; i < 5; i++) {
        var x = i * 15;
        var y = 14 - Math.random() * 12;
        points.push(x + ',' + y.toFixed(1));
      }
      html += '<svg class="ticker-sparkline" viewBox="0 0 60 16" width="60" height="16">' +
        '<polyline points="' + points.join(' ') + '" fill="none" stroke="var(--gold-400)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/>' +
        '</svg>';
    }

    html += '<span class="ticker-change ticker-' + dir + '">' + arrow + ' ' + Math.abs(item.change) + '%</span>';
    if (item.source) html += '<span class="ticker-source">' + item.source + '</span>';

    div.innerHTML = html;
    return div;
  }

  function buildDivider() {
    var d = document.createElement('div');
    d.className = 'ticker-divider';
    d.setAttribute('aria-hidden', 'true');
    return d;
  }

  function initTicker() {
    var track = document.querySelector('.ticker-track');
    if (!track) return;

    // Shuffle data
    var shuffled = tickerData.slice().sort(function () { return Math.random() - 0.5; });

    // Clear existing content
    track.innerHTML = '';

    // Build items x2 for seamless loop
    var fragment = document.createDocumentFragment();
    for (var copy = 0; copy < 2; copy++) {
      for (var i = 0; i < shuffled.length; i++) {
        fragment.appendChild(buildTickerItem(shuffled[i]));
        if (i < shuffled.length - 1) fragment.appendChild(buildDivider());
      }
    }
    track.appendChild(fragment);

    // Simulate live price updates every 8-15 seconds
    setInterval(function () {
      var items = track.querySelectorAll('.ticker-item');
      var randomItem = items[Math.floor(Math.random() * items.length)];
      randomItem.classList.add('flash');
      setTimeout(function () { randomItem.classList.remove('flash'); }, 800);

      // Visual feedback: scale price briefly
      if (Math.random() > 0.5) {
        var priceEl = randomItem.querySelector('.ticker-price');
        if (priceEl) {
          priceEl.style.transition = 'transform 200ms';
          priceEl.style.transform = 'scale(1.05)';
          setTimeout(function () { priceEl.style.transform = 'scale(1)'; }, 200);
        }
      }
    }, 8000 + Math.random() * 7000);
  }

  // Run after DOM ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initTicker);
  } else {
    initTicker();
  }
})();
