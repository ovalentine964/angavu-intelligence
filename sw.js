/**
 * Msaidizi — Basic Service Worker
 * Caches app shell for offline "Add to Home Screen" support
 */
const CACHE_NAME = 'msaidizi-v1';
const SHELL_ASSETS = [
  '/angavu-intelligence/',
  '/angavu-intelligence/index.html',
  '/angavu-intelligence/style.min.css',
  '/angavu-intelligence/script.min.js',
  '/angavu-intelligence/manifest.json'
];

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

// Fetch — cache-first for app shell, network-first for everything else
self.addEventListener('fetch', function (event) {
  var url = new URL(event.request.url);

  // Only handle same-origin GET requests
  if (event.request.method !== 'GET' || url.origin !== self.location.origin) {
    return;
  }

  event.respondWith(
    caches.match(event.request).then(function (cached) {
      if (cached) {
        // Return cached, fetch in background to update
        fetch(event.request).then(function (response) {
          if (response && response.status === 200) {
            caches.open(CACHE_NAME).then(function (cache) {
              cache.put(event.request, response);
            });
          }
        }).catch(function () {});
        return cached;
      }

      return fetch(event.request).then(function (response) {
        if (!response || response.status !== 200) {
          return response;
        }
        var responseClone = response.clone();
        caches.open(CACHE_NAME).then(function (cache) {
          cache.put(event.request, responseClone);
        });
        return response;
      }).catch(function () {
        // Offline fallback for navigation
        if (event.request.mode === 'navigate') {
          return caches.match('/angavu-intelligence/index.html');
        }
      });
    })
  );
});
