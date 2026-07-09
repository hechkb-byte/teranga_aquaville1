document.addEventListener('DOMContentLoaded', () => {

  // ── AOS init ──────────────────────────────────────────────────────
  AOS.init({ duration: 700, once: true, offset: 60 });

  // ── GLightbox (galerie immersive) ─────────────────────────────────
  if (typeof GLightbox !== 'undefined') {
    GLightbox({
      selector: '.glightbox',
      touchNavigation: true,
      loop: true,
      autoplayVideos: false,
    });
  }

  // ── Navbar scroll ─────────────────────────────────────────────────
  const navbar = document.getElementById('navbar');
  if (navbar) {
    const onScroll = () => {
      navbar.classList.toggle('scrolled', window.scrollY > 80);
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  // ── Burger menu mobile ────────────────────────────────────────────
  const burger = document.getElementById('burgerBtn');
  const navMenu = document.getElementById('navMenu');
  if (burger && navMenu) {
    burger.addEventListener('click', () => {
      navMenu.classList.toggle('open');
      burger.setAttribute('aria-expanded', navMenu.classList.contains('open'));
    });

    document.addEventListener('click', (e) => {
      if (!navbar.contains(e.target)) navMenu.classList.remove('open');
    });
  }

  // ── Tabs tarifs location ──────────────────────────────────────────
  document.querySelectorAll('.tarifs-tab').forEach(tab => {
    tab.addEventListener('click', () => {
      const target = tab.dataset.tab;
      document.querySelectorAll('.tarifs-tab').forEach(t => t.classList.remove('active'));
      document.querySelectorAll('.tarifs-tab__content').forEach(c => c.classList.remove('active'));
      tab.classList.add('active');
      const content = document.getElementById(`tab-${target}`);
      if (content) content.classList.add('active');
    });
  });

  // ── Formulaire multi-étapes ───────────────────────────────────────
  const form = document.getElementById('contactForm');
  if (form) {
    const steps = form.querySelectorAll('.multistep__step');
    const indicators = document.querySelectorAll('.step-indicator');
    const lines = document.querySelectorAll('.step-indicator__line');

    const goTo = (num) => {
      steps.forEach(s => s.classList.toggle('active', parseInt(s.dataset.step) === num));
      indicators.forEach((ind, i) => {
        ind.classList.toggle('active', i + 1 === num);
        ind.classList.toggle('done', i + 1 < num);
      });
      lines.forEach((line, i) => line.classList.toggle('done', i + 1 < num));
      document.getElementById('currentStep').value = num;
    };

    form.querySelectorAll('.multistep__next').forEach(btn => {
      btn.addEventListener('click', () => {
        const next = parseInt(btn.dataset.next);
        const currentStep = next - 1;

        if (currentStep === 1) {
          const checked = form.querySelector('input[name="type_bien_radio"]:checked');
          if (!checked) { showError(btn, 'Veuillez choisir une option'); return; }
          document.getElementById('hidden_type_bien').value = checked.value;
        }

        if (currentStep === 2) {
          const checked = form.querySelector('input[name="budget_radio"]:checked');
          if (checked) document.getElementById('hidden_budget').value = checked.value;
        }

        goTo(next);
      });
    });

    form.querySelectorAll('.multistep__prev').forEach(btn => {
      btn.addEventListener('click', () => goTo(parseInt(btn.dataset.prev)));
    });

    // Présélection si query param type_bien
    const params = new URLSearchParams(window.location.search);
    const preBien = params.get('type_bien');
    if (preBien) {
      const radio = form.querySelector(`input[value="${preBien}"]`);
      if (radio) {
        radio.checked = true;
        radio.closest('.option-card__content').parentElement.querySelector('.option-card__content').style.borderColor = 'var(--ocean)';
      }
    }
  }

  // ── Helper erreur bouton ──────────────────────────────────────────
  function showError(btn, msg) {
    const existing = btn.parentElement.querySelector('.step-error');
    if (existing) existing.remove();
    const el = document.createElement('p');
    el.className = 'step-error';
    el.style.cssText = 'color:#c0392b;font-size:.8rem;margin-top:.4rem;text-align:center;';
    el.textContent = msg;
    btn.parentElement.appendChild(el);
    setTimeout(() => el.remove(), 3000);
  }

  // ── Smooth scroll ancres ──────────────────────────────────────────
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', e => {
      const target = document.querySelector(a.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });

});
