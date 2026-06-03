# HER — deploy runbook (Firebase Hosting → her.dancinlab.org)

Serves `HER/web/` as a static site on **Firebase Hosting** (a Google Cloud product →
satisfies XPRIZE **R2**), with the custom domain **her.dancinlab.org** + automatic HTTPS.

Compiler-independent: this ships the frontend now, regardless of the hexa backend status.
The chat box works once the backend is live (self-hosted hexa compiler) or via an interim
function; until then `/api/chat` fails gracefully and HER shows its waitlist/offline line.

## what gets served

```
HER/web/index.html  ──▶  Firebase Hosting  ──▶  https://her.dancinlab.org
(landing + signup + chat UI)   (Google · CDN · HTTPS)        (custom domain)
```

`firebase.json` points `public` at `../web`, so run all commands from **this dir** (`HER/deploy/`).

## one-time setup (user — needs a Google account)

```sh
# 1. install the CLI (once)
npm i -g firebase-tools           # or: curl -sL https://firebase.tools | bash

# 2. log in (interactive — run in your own shell with `! firebase login`)
firebase login

# 3. create the Firebase project (or reuse one), then point .firebaserc at it
#    Console: https://console.firebase.google.com  → Add project → id e.g. her-dancinlab
#    then edit .firebaserc "default" to your real project id.
firebase projects:list
```

## deploy

```sh
cd HER/deploy
firebase deploy --only hosting
# → Hosting URL: https://<project>.web.app   (live immediately)
```

## connect her.dancinlab.org (custom domain)

```
1. Firebase Console → Hosting → Add custom domain → her.dancinlab.org
2. Firebase shows DNS records to add at the dancinlab.org registrar:
     - a TXT record (ownership verification), then
     - two A records (151.101.1.195 / 151.101.65.195) OR a CNAME for the subdomain
3. Add those records in the dancinlab.org DNS zone (subdomain host = `her`).
4. Wait for propagation (mins–hours). Firebase auto-provisions the SSL cert.
   → https://her.dancinlab.org is live.
```

> Apex vs subdomain: `her.dancinlab.org` is a subdomain, so a CNAME to
> `<project>.web.app` also works if the registrar supports it on subdomains.

## later — wiring the chat backend (when self-hosted hexa compiler ships)

The chat UI POSTs to same-origin `/api/chat`. Two options when the backend is ready:
- **Cloud Run** service (her_server.hexa) + a Firebase Hosting rewrite:
  add to `firebase.json` →
  `"rewrites": [ { "source": "/api/**", "run": { "serviceId": "her", "region": "us-central1" } }, { "source": "**", "destination": "/index.html" } ]`
- or a Firebase **Cloud Function** named `her` with a `/api/**` rewrite.

Gemini key at runtime (R3): `GOOGLE_API_KEY=$(secret get gemini.api_key)` injected into the
backend service env — never embed it in the static frontend.

## rollback

```sh
firebase hosting:rollback        # revert to the previous release
# or just delete the Firebase project; HER/ files are untouched.
```
