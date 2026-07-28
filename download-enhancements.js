/**
 * Download page enhancements for msaidizi-app.
 * Add this script to the download.html page.
 *
 * Features:
 * - SHA-256 checksum display and verification
 * - Privacy-friendly download analytics
 * - Smart share link handling (WhatsApp-safe)
 * - Installation instructions expansion
 */

(function() {
    'use strict';

    // ── Download Analytics (privacy-friendly) ──────────────────
    const ANALYTICS_KEY = 'msaidizi_dl_count';
    const SESSION_KEY = 'msaidizi_dl_session';

    function getAnonymousId() {
        let id = localStorage.getItem('msaidizi_anon_id');
        if (!id) {
            id = crypto.randomUUID ? crypto.randomUUID() :
                 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
                     const r = Math.random() * 16 | 0;
                     return (c === 'x' ? r : (r & 0x3 | 0x8)).toString(16);
                 });
            localStorage.setItem('msaidizi_anon_id', id);
        }
        return id;
    }

    function trackDownload(source) {
        // Local count
        const count = parseInt(localStorage.getItem(ANALYTICS_KEY) || '0') + 1;
        localStorage.setItem(ANALYTICS_KEY, count.toString());

        // Send to backend (fire-and-forget)
        try {
            fetch('https://angavu.com/api/msaidizi/analytics/download', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    anonymousId: getAnonymousId(),
                    source: source,
                    version: '1.0.0-alpha1',
                    timestamp: Date.now()
                }),
                keepalive: true
            }).catch(() => {}); // Silently fail
        } catch (e) { /* analytics should never break the page */ }
    }

    // ── SHA-256 Checksum Display ───────────────────────────────
    const CHECKSUMS = {
        'msaidizi-release.apk': {
            sha256: '',  // Populated by CI after build
            size: '~500 MB'
        }
    };

    function displayChecksums() {
        const container = document.getElementById('checksum-display');
        if (!container) return;

        const apk = CHECKSUMS['msaidizi-release.apk'];
        if (!apk || !apk.sha256) {
            container.innerHTML = `
                <div style="margin-top:1rem;padding:1rem;background:var(--gray-50);border-radius:var(--radius-lg);font-size:0.85rem;">
                    <p style="color:var(--gray-500);margin:0;">
                        🔐 <strong>Checksum:</strong> Available in
                        <a href="https://github.com/ovalentine964/msaidizi-app/releases/latest" target="_blank">GitHub Release</a>
                    </p>
                </div>
            `;
            return;
        }

        container.innerHTML = `
            <div style="margin-top:1rem;padding:1rem;background:var(--gray-50);border-radius:var(--radius-lg);font-size:0.85rem;">
                <p style="margin:0 0 0.5rem;color:var(--gray-700);">
                    🔐 <strong>SHA-256 Checksum:</strong>
                </p>
                <div style="display:flex;align-items:center;gap:0.5rem;flex-wrap:wrap;">
                    <code style="background:var(--gray-100);padding:0.5rem;border-radius:var(--radius);font-size:0.75rem;word-break:break-all;flex:1;min-width:200px;">
                        ${apk.sha256}
                    </code>
                    <button onclick="navigator.clipboard.writeText('${apk.sha256}').then(() => this.textContent = 'Copied!')"
                            style="padding:0.5rem 1rem;background:var(--navy-900);color:white;border:none;border-radius:var(--radius);cursor:pointer;font-size:0.8rem;">
                        Copy
                    </button>
                </div>
                <p style="margin:0.5rem 0 0;color:var(--gray-500);font-size:0.8rem;">
                    Verify after download: <code>sha256sum msaidizi-release.apk</code>
                </p>
            </div>
        `;
    }

    // ── WhatsApp Link Safety ───────────────────────────────────
    // Use a redirect page instead of direct APK link in WhatsApp shares
    function getShareUrl() {
        // The download page URL itself — safer than direct APK link
        return window.location.origin + '/download.html';
    }

    function getWhatsAppShareUrl() {
        const text = encodeURIComponent(
            'Pakua Msaidizi - App ya bure ya CFO kwa wafanyabiashara wote! ' +
            'Sauti kwanza. Bure milele. ' +
            getShareUrl()
        );
        return `https://wa.me/?text=${text}`;
    }

    // ── Download Button Handler ────────────────────────────────
    function setupDownloadButton() {
        const btn = document.getElementById('download-btn');
        if (!btn) return;

        btn.addEventListener('click', function(e) {
            // Track the download
            trackDownload('download_page');

            // Update local counter display
            const counter = document.getElementById('download-counter');
            if (counter) {
                const count = parseInt(localStorage.getItem(ANALYTICS_KEY) || '0');
                counter.textContent = `You've downloaded ${count} time${count !== 1 ? 's' : ''}`;
            }
        });
    }

    // ── Init ───────────────────────────────────────────────────
    document.addEventListener('DOMContentLoaded', function() {
        displayChecksums();
        setupDownloadButton();

        // Update WhatsApp share links to use page URL (not direct APK)
        document.querySelectorAll('a[href*="wa.me"]').forEach(function(link) {
            link.href = getWhatsAppShareUrl();
        });
    });

})();
