/* ============================================================
   CUSTOM CURSOR
   ============================================================ */
(function() {
    const dot  = document.getElementById('cursor-dot');
    const ring = document.getElementById('cursor-ring');
    if (!dot || !ring) return;
    let mx = 0, my = 0, rx = 0, ry = 0;
    document.addEventListener('mousemove', e => { mx = e.clientX; my = e.clientY; });
    function animCursor() {
        rx += (mx - rx) * 0.14;
        ry += (my - ry) * 0.14;
        dot.style.left  = mx + 'px';  dot.style.top  = my + 'px';
        ring.style.left = rx + 'px';  ring.style.top = ry + 'px';
        requestAnimationFrame(animCursor);
    }
    animCursor();
    document.querySelectorAll('a, button').forEach(el => {
        el.addEventListener('mouseenter', () => {
            dot.style.width = dot.style.height = '16px';
            dot.style.background = 'var(--green2)';
        });
        el.addEventListener('mouseleave', () => {
            dot.style.width = dot.style.height = '8px';
            dot.style.background = 'var(--green)';
        });
    });
})();

/* ============================================================
   DOT GRID + SOUND WAVES
   ============================================================ */
(function() {
    const canvas = document.getElementById('hero-canvas');
    if (!canvas) return;
    const ctx = canvas.getContext('2d');

    let W, H, dots = [];
    const SPACING = 36;

    function buildGrid() {
        dots = [];
        const cols = Math.ceil(W / SPACING) + 1;
        const rows = Math.ceil(H / SPACING) + 1;
        for (let r = 0; r < rows; r++)
            for (let c = 0; c < cols; c++)
                dots.push({ bx: c * SPACING, by: r * SPACING });
    }

    function resize() {
        W = canvas.width  = window.innerWidth;
        H = canvas.height = window.innerHeight;
        buildGrid();
    }
    window.addEventListener('resize', resize);

    // Mouse
    let mx = -9999, my = -9999, tx = -9999, ty = -9999;
    window.addEventListener('mousemove', e => { tx = e.clientX; ty = e.clientY; });

    // Sound waves pool
    const wavePool = [];
    let waveTimer = 0;
    const WAVE_INTERVAL = 18;

    let idleT = 0;

    function draw() {
        idleT += 0.008;
        mx += (tx - mx) * 0.08;
        my += (ty - my) * 0.08;

        // Light green background fill
        ctx.fillStyle = 'rgba(238,247,240,0.96)';
        ctx.fillRect(0, 0, W, H);

        // Dot grid
        dots.forEach(d => {
            const dx   = d.bx - mx;
            const dy   = d.by - my;
            const dist = Math.sqrt(dx * dx + dy * dy);
            const inf  = Math.max(0, 1 - dist / 220);
            const push = inf * inf * 28;
            const breathe = Math.sin(idleT + d.bx * 0.015 + d.by * 0.012) * 1.5;
            const nx = d.bx - (dx / (dist || 1)) * push + breathe;
            const ny = d.by - (dy / (dist || 1)) * push + breathe;
            const dotR  = 1.2 + inf * 1.8;
            const alpha = 0.12 + inf * 0.28;
            ctx.beginPath();
            ctx.arc(nx, ny, dotR, 0, Math.PI * 2);
            ctx.fillStyle = `rgba(22,163,74,${alpha})`;
            ctx.fill();
        });

        // Sound waves
        waveTimer++;
        if (waveTimer >= WAVE_INTERVAL && tx > 0) {
            waveTimer = 0;
            wavePool.push({ cx: mx, cy: my, r: 0, maxR: 180, speed: 1.4 });
        }
        for (let i = wavePool.length - 1; i >= 0; i--) {
            const w = wavePool[i];
            w.r += w.speed;
            const a = 0.18 * (1 - w.r / w.maxR);
            ctx.beginPath();
            ctx.arc(w.cx, w.cy, w.r, 0, Math.PI * 2);
            ctx.strokeStyle = `rgba(22,163,74,${Math.max(0, a)})`;
            ctx.lineWidth = 0.75;
            ctx.stroke();
            if (w.r >= w.maxR) wavePool.splice(i, 1);
        }

        requestAnimationFrame(draw);
    }

    resize();
    draw();
})();

/* ============================================================
   TYPEWRITER
   ============================================================ */
(function() {
    const el = document.getElementById('typewriter-text');
    if (!el) return;
    const roles = [
        'Lead Solution Architect',
        'Cloud Architect · Azure & AWS',
        'GenAI Builder',
        'CyberSecurity Architect',
        'Scrum Master · Product Owner',
        'Project Manager'
    ];
    let ri = 0, ci = 0, deleting = false;
    function tick() {
        const full = roles[ri];
        if (!deleting) {
            el.textContent = full.slice(0, ++ci);
            if (ci === full.length) { deleting = true; setTimeout(tick, 1800); return; }
        } else {
            el.textContent = full.slice(0, --ci);
            if (ci === 0) { deleting = false; ri = (ri + 1) % roles.length; setTimeout(tick, 400); return; }
        }
        setTimeout(tick, deleting ? 40 : 70);
    }
    setTimeout(tick, 1200);
})();

/* ============================================================
   SCROLL REVEAL & NAVBAR
   ============================================================ */
(function() {
    const navbar = document.getElementById('navbar');
    const backTop = document.getElementById('back-top');
    const links   = document.querySelectorAll('.nav-link');
    const sections = document.querySelectorAll('section[id]');

    window.addEventListener('scroll', () => {
        const sy = window.scrollY;
        if (navbar)  navbar.classList.toggle('scrolled', sy > 50);
        if (backTop) backTop.classList.toggle('visible', sy > 400);

        // Active nav link
        let cur = '';
        sections.forEach(s => {
            if (sy >= s.offsetTop - 120) cur = s.id;
        });
        links.forEach(l => l.classList.toggle('active', l.getAttribute('href') === '#'+cur));
    });

    if (backTop) backTop.addEventListener('click', () => window.scrollTo({ top: 0, behavior: 'smooth' }));

    // Mobile nav toggle
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu   = document.querySelector('.nav-menu');
    if (navToggle && navMenu) {
        navToggle.addEventListener('click', () => navMenu.classList.toggle('open'));
        links.forEach(l => l.addEventListener('click', () => navMenu.classList.remove('open')));
    }

    // Smooth anchor scroll
    document.querySelectorAll('a[href^="#"]').forEach(a => {
        a.addEventListener('click', e => {
            const t = document.querySelector(a.getAttribute('href'));
            if (t) { e.preventDefault(); window.scrollTo({ top: t.offsetTop - 68, behavior: 'smooth' }); }
        });
    });
})();

/* ============================================================
   INTERSECTION OBSERVER — section headers + cards
   ============================================================ */
(function() {
    const io = new IntersectionObserver(entries => {
        entries.forEach(e => {
            if (e.isIntersecting) {
                e.target.classList.add('revealed');
                io.unobserve(e.target);
            }
        });
    }, { threshold: 0.15, rootMargin: '0px 0px -60px 0px' });

    document.querySelectorAll('.section-header h2, .section-header p').forEach(el => io.observe(el));

    // stagger cards
    const cardObs = new IntersectionObserver(entries => {
        entries.forEach((e, idx) => {
            if (e.isIntersecting) {
                // find siblings for stagger
                const siblings = [...e.target.parentElement.querySelectorAll('.reveal-item:not(.revealed)')];
                siblings.forEach((s, i) => {
                    setTimeout(() => {
                        s.classList.add('revealed');
                    }, i * 80);
                });
                cardObs.unobserve(e.target);
            }
        });
    }, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });

    document.querySelectorAll('.reveal-item').forEach(el => cardObs.observe(el));
})();

/* ============================================================
   COUNT-UP ANIMATION
   ============================================================ */
(function() {
    const counters = document.querySelectorAll('[data-count]');
    const io = new IntersectionObserver(entries => {
        entries.forEach(e => {
            if (e.isIntersecting) {
                const el  = e.target;
                const end = parseInt(el.dataset.count);
                const sfx = el.dataset.suffix || '';
                let start = 0;
                const dur = 1400, step = 16;
                const inc = end / (dur / step);
                const timer = setInterval(() => {
                    start = Math.min(start + inc, end);
                    el.textContent = Math.round(start) + sfx;
                    if (start >= end) clearInterval(timer);
                }, step);
                io.unobserve(el);
            }
        });
    }, { threshold: 0.5 });
    counters.forEach(c => io.observe(c));
})();

/* ============================================================
   TIMELINE DRAW
   ============================================================ */
(function() {
    const timeline = document.getElementById('timeline');
    const fill     = document.getElementById('timeline-fill');
    const dots     = document.querySelectorAll('.timeline-dot');
    if (!timeline || !fill) return;

    window.addEventListener('scroll', () => {
        const rect = timeline.getBoundingClientRect();
        const visible = Math.max(0, Math.min(1, (-rect.top + window.innerHeight * 0.8) / rect.height));
        fill.style.height = (visible * 100) + '%';

        // pulse dots as they enter view
        dots.forEach(dot => {
            const dr = dot.getBoundingClientRect();
            if (dr.top < window.innerHeight * 0.85 && !dot.classList.contains('pulse')) {
                dot.classList.add('pulse');
            }
        });
    });
})();

/* ============================================================
   MAGNETIC BUTTONS
   ============================================================ */
(function() {
    document.querySelectorAll('.btn').forEach(btn => {
        btn.addEventListener('mousemove', e => {
            const r = btn.getBoundingClientRect();
            const dx = e.clientX - (r.left + r.width/2);
            const dy = e.clientY - (r.top  + r.height/2);
            btn.style.transform = `translate(${dx*0.2}px, ${dy*0.2}px)`;
        });
        btn.addEventListener('mouseleave', () => {
            btn.style.transform = '';
        });
    });
})();

/* ============================================================
   SKILL BADGE STAGGER FLOAT
   ============================================================ */
(function() {
    document.querySelectorAll('.skill-badge').forEach((b, i) => {
        b.style.animationDuration = (3 + (i % 5) * 0.4) + 's';
        b.style.animationDelay   = (i * 0.12) + 's';
    });
})();

/* ============================================================
   CONTACT FORM
   ============================================================ */
(function() {
    const form = document.getElementById('contactForm');
    if (!form) return;
    form.addEventListener('submit', e => {
        e.preventDefault();
        const btn = form.querySelector('button[type="submit"]');
        const orig = btn.querySelector('.btn-inner').textContent;
        btn.querySelector('.btn-inner').textContent = 'Sending…';
        btn.disabled = true;
        setTimeout(() => {
            btn.querySelector('.btn-inner').textContent = '✓ Message sent!';
            setTimeout(() => {
                btn.querySelector('.btn-inner').textContent = orig;
                btn.disabled = false;
                form.reset();
            }, 2500);
        }, 1000);
    });
})();

/* ============================================================
   VIEW COUNT
   ============================================================ */
(function() {
    const el = document.getElementById('view-count');
    if (!el) return;
    fetch('https://raw.githubusercontent.com/sivahari1983/My-Profile/main/view_count.json?t=' + Date.now(), { cache: 'no-store' })
        .then(r => r.json())
        .then(d => { if (d.views) el.textContent = d.views.toLocaleString(); })
        .catch(() => { el.textContent = '—'; });
})();
