// The shell is cached up front; card pictures only when a card comes up, since nobody wants
// to download two megabytes per card in advance.
const CACHE = "data-flashcards-v1";
const FILES = ["./", "./index.html", "./cards.json", "./manifest.json",
               "./icon.svg", "./icon-192.png", "./icon-512.png"];

// Cards and shell: network first, so a changed card arrives at once. Pictures: cache first,
// they do not change.
const FRESH = [/cards\.json$/, /index\.html$/, /\/$/];

self.addEventListener("install", e => {
  e.waitUntil(caches.open(CACHE).then(c => c.addAll(FILES)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", e => {
  e.waitUntil(caches.keys()
    .then(names => Promise.all(names.filter(n => n.startsWith("data-flashcards-") && n !== CACHE).map(n => caches.delete(n))))
    .then(() => self.clients.claim()));
});

self.addEventListener("fetch", e => {
  if (e.request.method !== "GET") return;
  const networkFirst = FRESH.some(r => r.test(new URL(e.request.url).pathname));

  e.respondWith((async () => {
    const cache = await caches.open(CACHE);
    // Keep only successes; a cached 404 would otherwise stay a 404 forever.
    const keep = (response) => {
      if (response.ok) cache.put(e.request, response.clone());
      return response;
    };
    if (networkFirst) {
      try {
        return keep(await fetch(e.request));
      } catch (offline) {
        const hit = await cache.match(e.request);
        if (hit) return hit;
        throw offline;
      }
    }
    const hit = await cache.match(e.request);
    if (hit) return hit;
    return keep(await fetch(e.request));
  })());
});
