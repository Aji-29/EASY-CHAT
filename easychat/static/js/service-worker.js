const CACHE_NAME = 'easychat-cache-v1';
const urlsToCache = [
    '/',
    '/static/css/bootstrap/bootstrap.min.css',
    '/static/css/index.css',
    '/static/js/jquery.min.js',  // Add any other necessary static files here
    '/static/img/icons/icon-192x192.png',  // Placeholder for icon file
    '/static/img/icons/icon-512x512.png'   // Placeholder for icon file
];

self.addEventListener('install', function(event) {
    event.waitUntil(
        caches.open(CACHE_NAME)
            .then(function(cache) {
                return cache.addAll(urlsToCache);
            })
    );
});

self.addEventListener('fetch', function(event) {
    event.respondWith(
        caches.match(event.request)
            .then(function(response) {
                if (response) {
                    return response;
                }
                return fetch(event.request);
            })
    );
});

self.addEventListener('activate', function(event) {
    const cacheWhitelist = [CACHE_NAME];
    event.waitUntil(
        caches.keys().then(function(cacheNames) {
            return Promise.all(
                cacheNames.map(function(cacheName) {
                    if (cacheWhitelist.indexOf(cacheName) === -1) {
                        return caches.delete(cacheName);
                    }
                })
            );
        })
    );
});
