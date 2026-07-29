/**
 * Rae ARK site — shared behavior across all pages.
 * Progressive enhancement only: every feature here has a working
 * fallback without JS (see the <noscript> blocks in each page's
 * <head> and in feedback.html). Nothing here is required to read
 * the site or reach any page.
 *
 * Sections:
 *   1. Mobile nav toggle
 *   2. Active-page nav highlight
 *   3. Reveal-on-scroll (cosmetic only, degrades to fully visible)
 *   4. Feedback form -> mailto link builder
 */

document.addEventListener('DOMContentLoaded', function () {
  // Mobile nav toggle
  var toggle = document.querySelector('.nav-toggle');
  var nav = document.querySelector('.main-nav');
  if (toggle && nav) {
    toggle.addEventListener('click', function () {
      var isOpen = nav.classList.toggle('open');
      toggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
    });
    // Close menu after a nav link is tapped
    nav.querySelectorAll('a').forEach(function (a) {
      a.addEventListener('click', function () { nav.classList.remove('open'); });
    });
  }

  // Mark current page in nav
  var here = location.pathname.split('/').pop() || 'index.html';
  document.querySelectorAll('.main-nav a').forEach(function (a) {
    var target = a.getAttribute('href');
    if (target === here || (here === '' && target === 'index.html')) {
      a.classList.add('active');
    }
  });

  // Gentle reveal-on-scroll for cards and sections
  var revealables = document.querySelectorAll('.work-card, .journal-entry, .read-card');
  if ('IntersectionObserver' in window && revealables.length) {
    revealables.forEach(function (el) {
      el.style.opacity = '0';
      el.style.transform = 'translateY(10px)';
      el.style.transition = 'opacity 0.5s ease, transform 0.5s ease';
    });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.style.opacity = '1';
          entry.target.style.transform = 'translateY(0)';
          io.unobserve(entry.target);
        }
      });
    }, { threshold: 0.1 });
    revealables.forEach(function (el) { io.observe(el); });
  }

  // Feedback form — builds a mailto: link, no server involved
  var feedbackForm = document.getElementById('feedback-form');
  if (feedbackForm) {
    feedbackForm.addEventListener('submit', function (e) {
      e.preventDefault();
      var subject = document.getElementById('fb-subject').value;
      var name = document.getElementById('fb-name').value.trim();
      var message = document.getElementById('fb-message').value.trim();
      var body = (name ? 'From: ' + name + '\n\n' : '') + message;
      var mailto = 'mailto:horizonarkstudio@gmail.com'
        + '?subject=' + encodeURIComponent(subject)
        + '&body=' + encodeURIComponent(body);
      window.location.href = mailto;
    });
  }
});

if ("serviceWorker" in navigator) {
    window.addEventListener("load", () => {
        navigator.serviceWorker.register("/sw.js");
    });
}
