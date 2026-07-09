/**
 * Msaidizi — Basic Service Worker
 * Caches app shell for offline "Add to Home Screen" support
 *
 * Security: cache entries expire after CACHE_TTL_MS to prevent
 * indefinitely stale content from being served after deploys.
 */
const CACHE_NAME = 'msaidizi-v2';
const CACHE_TTL_MS = 24 * 60 * 60 * 1000; // 24 hours
const SHELL_ASSETS = [
  '/angavu-intelligence/',
  '/angavu-intelligence/index.html',
  '/angavu-intelligence/style.min.css',
  '/angavu-intelligence/script.min.js',
  '/angavu-intelligence/manifest.json'
];

/**
 * Store a cache entry with a timestamp header so we can check freshness.
 */
function putWithTimestamp(cache, request, response) {
  var headers = new Headers(response.headers);
  headers.set('sw-cached-at', Date.now().toString());
  var timedResponse = new Response(response.body, {
    status: response.status,
    statusText: response.statusText,
    headers: headers
  });
  return cache.put(request, timedResponse);
}

/**
 * Check if a cached response is still fresh.
 */
function isFresh(cachedResponse) {
  if (!cachedResponse) return false;
  var cachedAt = cachedResponse.headers.get('sw-cached-at');
  if (!cachedAt) return false;
  return (Date.now() - parseInt(cachedAt, 10)) < CACHE_TTL_MS;
}

// Install — cache app shell
self.addEventListener('install', function (event) {
  event.waitUntil(
    caches.open(CACHE_NAME).then(function (cache) {
      return cache.addAll(SHELL_ASSETS);
    })
  );
  self.skipWaiting();
});

// Activate — clean old caches
self.addEventListener('activate', function (event) {
  event.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(
        keys
          .filter(function (key) { return key !== CACHE_NAME; })
          .map(function (key) { return caches.delete(key); })
      );
    })
  );
  self.clients.claim();
});

// Fetch — cache-first for app shell (with TTL), network-first for everything else
self.addEventListener('fetch', function (event) {
  var url = new URL(event.request.url);

  // Only handle same-origin GET requests
  if (event.request.method !== 'GET' || url.origin !== self.location.origin) {
    return;
  }

  event.respondWith(
    caches.match(event.request).then(function (cached) {
      if (cached && isFresh(cached)) {
        // Return cached (still fresh), fetch in background to update
        fetch(event.request).then(function (response) {
          if (response && response.status === 200) {
            caches.open(CACHE_NAME).then(function (cache) {
              putWithTimestamp(cache, event.request, response);
            });
          }
        }).catch(function () {});
        return cached;
      }

      // Cache miss or expired — fetch from network
      return fetch(event.request).then(function (response) {
        if (!response || response.status !== 200) {
          return response;
        }
        var responseClone = response.clone();
        caches.open(CACHE_NAME).then(function (cache) {
          putWithTimestamp(cache, event.request, responseClone);
        });
        return response;
      }).catch(function () {
        // Offline fallback: serve expired cache if available, else navigation fallback
        if (cached) {
          return cached;
        }
        if (event.request.mode === 'navigate') {
          return caches.match('/angavu-intelligence/index.html');
        }
      });
    })
  );
});
