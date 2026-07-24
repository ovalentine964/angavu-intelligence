/**
 * Msaidizi Service Worker v2.0
 * Cache-first with 24h TTL for app shell
 * Network-first for dynamic content
 * Optimized for 2G/3G connections
 */
var CACHE_NAME = 'angavu-v2';
var CACHE_TTL_MS = 24 * 60 * 60 * 1000; // 24 hours
var SHELL_ASSETS = [
    '/angavu-intelligence/',
    '/angavu-intelligence/index.html',
    '/angavu-intelligence/download.html',
    '/angavu-intelligence/for-workers.html',
    '/angavu-intelligence/for-businesses.html',
    '/angavu-intelligence/for-government.html',
    '/angavu-intelligence/technology.html',
    '/angavu-intelligence/vision.html',
    '/angavu-intelligence/api.html',
    '/angavu-intelligence/privacy-policy.html',
    '/angavu-intelligence/style.css',
    '/angavu-intelligence/script.js',
    '/angavu-intelligence/design-tokens.css',
    '/angavu-intelligence/manifest.json'
];

function putWithTimestamp(cache, request, response) {
    var headers = new Headers(response.headers);
    headers.set('sw-cached-at', Date.now().toString());
    var timed = new Response(response.body, {
        status: response.status,
        statusText: response.statusText,
        headers: headers
    });
    return cache.put(request, timed);
}

function isFresh(cached) {
    if (!cached) return false;
    var ts = cached.headers.get('sw-cached-at');
    if (!ts) return false;
    return (Date.now() - parseInt(ts, 10)) < CACHE_TTL_MS;
}

self.addEventListener('install', function(e) {
    e.waitUntil(
        caches.open(CACHE_NAME).then(function(cache) {
            return cache.addAll(SHELL_ASSETS);
        })
    );
    self.skipWaiting();
});

self.addEventListener('activate', function(e) {
    e.waitUntil(
        caches.keys().then(function(keys) {
            return Promise.all(
                keys.filter(function(k) { return k !== CACHE_NAME; })
                    .map(function(k) { return caches.delete(k); })
            );
        })
    );
    self.clients.claim();
});

self.addEventListener('fetch', function(e) {
    var url = new URL(e.request.url);
    if (e.request.method !== 'GET' || url.origin !== self.location.origin) return;

    e.respondWith(
        caches.match(e.request).then(function(cached) {
            if (cached && isFresh(cached)) {
                // Stale-while-revalidate: return cached, update in background
                fetch(e.request).then(function(resp) {
                    if (resp && resp.status === 200) {
                        caches.open(CACHE_NAME).then(function(c) {
                            putWithTimestamp(c, e.request, resp);
                        });
                    }
                }).catch(function() {});
                return cached;
            }
            return fetch(e.request).then(function(resp) {
                if (!resp || resp.status !== 200) return resp;
                var clone = resp.clone();
                caches.open(CACHE_NAME).then(function(c) {
                    putWithTimestamp(c, e.request, clone);
                });
                return resp;
            }).catch(function() {
                if (cached) return cached;
                if (e.request.mode === 'navigate') {
                    return caches.match('/angavu-intelligence/index.html');
                }
            });
        })
    );
});
