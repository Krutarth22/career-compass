---
title: "Push Notifications and Deep Links"
track: "mobile-engineer"
difficulty_tier: "intermediate"
estimated_hours: 12
role: "core"
skill_tags: ["push-notifications", "mobile-ui-patterns", "mobile-development", "backend-frameworks"]
skill_prerequisites: ["mobile-development"]
project_prerequisites: ["api-backed-list-detail-app.md"]
prerequisite_learning_hours: 3
---

# Push Notifications and Deep Links

## Production Workflow Mirrored
1. Registering a device for push and storing its token server-side
2. Sending notifications from a backend through APNs or FCM
3. Handling notifications in foreground, background, and terminated states
4. Routing a tap to the right screen via deep links and universal links
5. Respecting permission prompts and letting users manage preferences

## What You'll Build
Extend the app from `api-backed-list-detail-app.md` with push
notifications sent from a small backend you write, where tapping a
notification deep-links directly to the relevant detail screen, the app
handles notifications correctly in every lifecycle state, universal or
app links open the same screens from a web URL, and a settings screen
lets the user opt in or out of notification categories.

## Student-Scope Notes
- Requires a developer account and a physical device for iOS push;
  Android works on an emulator with Google Play services.
- The backend is a single endpoint that sends a push to a stored token
  via the provider's SDK. No notification campaign tooling.
- One or two notification categories are enough to demonstrate
  preferences.

## Steps
1. Configure push credentials for your platform and implement the
   permission request at a sensible moment, not on first launch.
2. Register for push, receive the device token, and send it to your
   backend with the user's identity.
3. Build the backend endpoint that sends a notification with a payload
   containing the target item id.
4. Handle notification receipt in the foreground (in-app banner), in the
   background, and when the app is launched from a terminated state.
5. Implement deep-link routing: parse the payload and navigate to the
   detail screen for that item, including when the navigation stack is
   empty.
6. Configure universal links or app links so a web URL for an item opens
   the same screen, with the association file hosted on your backend.
7. Add a settings screen for notification preferences, persist them, and
   have the backend respect them.
8. Test every lifecycle path on a physical device and write up the
   routing design and the lifecycle matrix you tested.

## Extension Ideas
- Add rich notifications with images and action buttons.
- Add silent pushes that trigger a background refresh.
- Add notification grouping and badge count management.
- Add analytics for delivery and open rates.

## Skills Demonstrated
- Push notification registration, sending, and lifecycle handling
- Deep linking and universal or app link configuration
- Navigation routing from external entry points
- Notification permission and preference UX

## Industry Relevance

E-commerce, Social, Fintech. Re-engagement, order updates, and transaction alerts all depend on push and deep links working across every app state, and broken deep links are one of the most common mobile bugs these companies ship. Engineers who have wired the full path from backend to screen are trusted with these high-visibility features.
