// Base Service Worker implementation

const offlineFile = "/offline/"
const staticCacheName = "yamsa-cache-v" + new Date().getTime();
const filesToCache = [
  offlineFile,
  "static/images/favicon.ico",
  "static/images/favicon-16x16.png",
  "static/images/favicon-32x32.png",
  "static/images/apple-touch-icon.png",
  "static/images/android-chrome-192x192.png",
  "static/images/android-chrome-512x512.png"
// TODO CT: Add splash images here
];

// Cache on install
self.addEventListener("install", event => {
  this.skipWaiting();
  event.waitUntil(
    caches.open(staticCacheName)
      .then(cache => {
        return cache.addAll(filesToCache);
      })
  )
});

// Clear cache on activate
self.addEventListener('activate', event => {
  event.waitUntil(
    caches.keys().then(cacheNames => {
      return Promise.all(
        cacheNames
          .filter(cacheName => (cacheName.startsWith("yamsa-cache-")))
          .filter(cacheName => (cacheName !== staticCacheName))
          .map(cacheName => caches.delete(cacheName))
      );
    })
  );
});

// Serve from Cache
self.addEventListener("fetch", event => {
  event.respondWith(
    caches.match(event.request)
      .then(response => {
        return response || fetch(event.request);
      })
      .catch(() => {
        return caches.match(offlineFile);
      })
  )
});

// Register event listener for the 'push' event.
self.addEventListener('push', (event) => {
  // Retrieve the textual payload from event.data (a PushMessageData object).
  // Other formats are supported (ArrayBuffer, Blob, JSON), check out the documentation
  // on https://developer.mozilla.org/en-US/docs/Web/API/PushMessageData.
  const {head, ...options} = JSON.parse(event.data.text());

  // Keep the service worker alive until the notification is created.
  event.waitUntil(
    self.registration.showNotification(head, options)
  );
});

const navigateClientsToUrl = async (event, url) => {// Get all the Window clients
  await event.waitUntil(self.clients.claim())

  const clientArray = await self.clients.matchAll({type: "window"})

  const hadWindowToFocus = clientArray.filter((windowClient) => {
      // If a Window tab matching the targeted URL already exists, focus that;
      if (windowClient.url === url) {
        windowClient.focus().then()
        return true
      }

      // Check to make sure WindowClient.navigate() is supported.
      if ('navigate' in windowClient) {
        windowClient.navigate(url).then();
        return true
      }

      return false
    }
  ).length > 0;

  // Otherwise, open a new tab to the applicable URL and focus it.
  if (!hadWindowToFocus) {
    const windowClient = await self.clients.openWindow(url)

    if (windowClient) {
      await windowClient.focus()
    }
  }
}

const getURLForAction = (action, actionClickUrls) => {
  for (let i = 0; i < actionClickUrls.length; i++) {
    if (actionClickUrls[i].action === action) {
      return actionClickUrls[i].url;
    }
  }
  // If no match is found, you may choose to return null or some other default value.
  return null;
}

self.addEventListener('notificationclick', async (event) => {
  // Close the notification popout
  event.notification.close();

  // console.log("event", event)
  // console.log("self", self)

  const {actionClickUrls, notificationClickUrl} = event.notification.data

  if (!event.action) {
    // Was a normal notification click
    console.log('Notification Click.');
    await navigateClientsToUrl(event, notificationClickUrl)
    return;
  }

  switch (event.action) {
    case 'click-me-action':
      console.debug("click-me-action clicked")
      const actionUrl = getURLForAction("click-me-action", actionClickUrls)
      navigateClientsToUrl(event, actionUrl)
      break;
    default:
      console.log(`Unknown action clicked: '${event.action}'`);
      break;
  }
});