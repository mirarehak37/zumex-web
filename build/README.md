# Generátor webu

Všechny stránky se generují z `content.json` skriptem `build.py`:

    python3 build/build.py . build/content.json

Bez argumentů vygeneruje celý web. Jednotlivé části: `home`, `styleguide`, `catalog`, `details`, `contact`, `404`.
Styly jsou v `assets/css/tokens.css` (barvy, písma, mezery) a `assets/css/components.css` (komponenty), interakce v `assets/js/site.js`.
Původní web před redesignem: git tag `puvodni-web` nebo soubor `zaloha-puvodni-web-2026-11-23.zip`.
