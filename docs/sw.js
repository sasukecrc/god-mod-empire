// J.A.R.V.I.S. Service Worker v3.0 - Ultimate Android + Offline
const CACHE = 'jarvis-godmod-v3';
const ASSETS = [
  '/god-mod-empire/',
  '/god-mod-empire/index.html',
  '/god-mod-empire/manifest.json',
  '/god-mod-empire/sw.js'
];

self.addEventListener('install', e => {
  e.waitUntil(
    caches.open(CACHE).then(cache => {
      return cache.addAll(ASSETS).then(() => self.skipWaiting());
    })
  );
});

self.addEventListener('activate', e => {
  e.waitUntil(
    caches.keys().then(keys => {
      return Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k)));
    }).then(() => self.clients.claim())
  );
});

self.addEventListener('fetch', e => {
  const url = new URL(e.request.url);
  
  // GitHub API - network first, cache fallback
  if (url.hostname === 'api.github.com') {
    e.respondWith(
      fetch(e.request).then(res => {
        const clone = res.clone();
        caches.open(CACHE).then(cache => cache.put(e.request, clone));
        return res;
      }).catch(() => caches.match(e.request))
    );
    return;
  }
  
  // PWABuilder API
  if (url.hostname === 'pwabuilder.com') {
    e.respondWith(
      fetch(e.request).catch(() => new Response('API offline', { status: 503 }))
    );
    return;
  }

  // Cache-first for everything else with network update
  e.respondWith(
    caches.open(CACHE).then(cache => {
      return cache.match(e.request).then(cached => {
        const fetchPromise = fetch(e.request).then(res => {
          if (res.ok) {
            cache.put(e.request, res.clone());
          }
          return res;
        }).catch(() => cached);
        
        // Return cached immediately if available, else wait for network
        return cached || fetchPromise;
      });
    })
  );
});

// Handle messages from the app
self.addEventListener('message', e => {
  if (e.data === 'skipWaiting') {
    self.skipWaiting();
  }
  if (e.data === 'update') {
    self.skipWaiting();
    // Notify all clients
    self.clients.matchAll().then(clients => {
      clients.forEach(client => {
        client.postMessage('updated');
      });
    });
  }
});

// Background sync for offline actions
self.addEventListener('sync', e => {
  if (e.tag === 'sync-data') {
    e.waitUntil(syncData());
  }
});

async function syncData() {
  const clients = await self.clients.matchAll();
  clients.forEach(client => {
    client.postMessage('sync-complete');
  });
}
