# Ladies.de Profile Scraper 🕷️

A Selenium-based scraper that collects user names and phone numbers from [Ladies.de](https://www.ladies.de), handling dynamic content, region-based filtering, and ad listings across multiple pages.

---

## 🔍 Features

- Headless Chrome scraping
- Accepts cookie consent, selects "Alle Regionen", and navigates to ad listings
- Skips malformed or incomplete profiles
- Multi-page support with random delays
- Clean output in `scraped_data.json`
- Live logging in the terminal with helpful emojis (✔, ❌, ⏭)

---

## 🧠 Real-World Complexity

Unlike simple static websites, Ladies.de presents several dynamic behaviors and interaction barriers:

- Cookie banners that block access until accepted
- Region filtering that requires JavaScript-powered dropdown interaction
- A promotional banner that overlays content until closed
- A "show ads" button that must be clicked before reaching listings
- Paginated ad results with dynamic loading (`?page=1`, `?page=2`, etc.)
- Some profile links lead to pages that don't contain usable information

These factors make this scraper more than just a loop and a few requests.

---

## 🛠 My Approach

This script uses **Selenium WebDriver** to simulate a user navigating the site, with careful steps to ensure stability and accuracy:

- ✅ Waits for and clicks the cookie consent button
- ✅ Selects "Alle Regionen" using form interaction and menu logic
- ✅ Closes the banner that may hide important links
- ✅ Navigates through the proper flow to reach ad listings
- ✅ Waits for content to load before interacting with the page
- ✅ Validates profile pages before scraping to avoid bad data
- ✅ Randomized delays to mimic natural browsing patterns
- ✅ Structured output saved to JSON for easy reuse

This approach ensures reliable data collection from a JavaScript-heavy, interaction-dependent site.

---

## 📁 Output Format

```json
[
  {
    "user_name": "MiaLust",
    "phone_number": "0123 456789"
  },
  {
    "user_name": "SweetHoney94",
    "phone_number": "0987 654321"
  }
]
