const GOOGLE_ANALYTICS_ID = 'G-5V35SK8H5Z';

function initGoogleAnalytics() {
    if (!GOOGLE_ANALYTICS_ID || GOOGLE_ANALYTICS_ID === 'G-XXXXXXXXXX') return;

    const tag = document.createElement('script');
    tag.async = true;
    tag.src = 'https://www.googletagmanager.com/gtag/js?id=' + encodeURIComponent(GOOGLE_ANALYTICS_ID);
    document.head.appendChild(tag);

    window.dataLayer = window.dataLayer || [];
    window.gtag = function gtag() {
        window.dataLayer.push(arguments);
    };
    window.gtag('js', new Date());
    window.gtag('config', GOOGLE_ANALYTICS_ID);
}

function trackAnalyticsEvent(name, params = {}) {
    if (typeof window.gtag === 'function') {
        window.gtag('event', name, params);
    }
}

initGoogleAnalytics();

document.querySelectorAll('[data-track]').forEach(element => {
    element.addEventListener('click', () => {
        trackAnalyticsEvent(element.dataset.track);
    });
});

const trackedScrollDepths = new Set();
const scrollDepthTargets = [25, 50, 75, 90];

function trackScrollDepth() {
    const scrollableHeight = document.documentElement.scrollHeight - window.innerHeight;
    if (scrollableHeight <= 0) return;

    const depth = Math.round((window.scrollY / scrollableHeight) * 100);
    scrollDepthTargets.forEach(target => {
        if (depth >= target && !trackedScrollDepths.has(target)) {
            trackedScrollDepths.add(target);
            trackAnalyticsEvent('scroll_depth', {
                percent: target
            });
        }
    });
}

window.addEventListener('scroll', trackScrollDepth, { passive: true });

const sectionViewObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const eventName = entry.target.dataset.trackView;
            if (eventName) {
                trackAnalyticsEvent(eventName);
                sectionViewObserver.unobserve(entry.target);
            }
        }
    });
}, { threshold: 0.45 });

document.querySelectorAll('[data-track-view]').forEach(section => sectionViewObserver.observe(section));

let hasTrackedFormStart = false;

document.querySelectorAll('#register input, #register select, #register textarea').forEach(field => {
    field.addEventListener('input', () => {
        if (!hasTrackedFormStart) {
            hasTrackedFormStart = true;
            trackAnalyticsEvent('form_start');
        }
    }, { once: false });
});

function fmt(n) {
    if (n >= 1000000) return (n / 1000000).toFixed(1).replace('.0', '') + ' triệu';
    if (n >= 1000) return Math.round(n / 1000) + 'k';
    return n.toString();
}

function fmtVND(n) {
    return new Intl.NumberFormat('vi-VN').format(n) + ' VND';
}

function calcROI() {
    const slots = parseInt(document.getElementById('slots').value);
    const pax = parseInt(document.getElementById('pax').value);
    const spend = parseInt(document.getElementById('spend').value) * 1000;

    document.getElementById('slots-val').textContent = slots + ' slot';
    document.getElementById('pax-val').textContent = pax + ' người';
    document.getElementById('spend-val').textContent = Math.round(spend / 1000) + 'k VND';

    const coversPerMonth = slots * 4 * pax;
    const gross = coversPerMonth * spend;
    const fee = coversPerMonth * 10000;
    const net = gross - fee;

    document.getElementById('roi-covers').textContent = coversPerMonth + ' người';
    document.getElementById('roi-gross').textContent = fmtVND(gross);
    document.getElementById('roi-fee').textContent = '- ' + fmtVND(fee);
    document.getElementById('roi-net').textContent = fmtVND(net);
    document.getElementById('roi-total').textContent = fmt(net);
    document.getElementById('roi-sub').textContent = 'VND / tháng · ước tính lợi nhuận ròng';
}

let hasTrackedRoiInteraction = false;

['slots', 'pax', 'spend'].forEach(id => {
    document.getElementById(id).addEventListener('input', () => {
        if (!hasTrackedRoiInteraction) {
            trackAnalyticsEvent('roi_interaction');
            hasTrackedRoiInteraction = true;
        }
        calcROI();
    });
});
calcROI();

function submitForm() {
    const name = document.getElementById('f-name').value.trim();
    const phone = document.getElementById('f-phone').value.trim();
    const addr = document.getElementById('f-address').value.trim();
    const contact = document.getElementById('f-contact').value.trim();
    const cuisine = document.getElementById('f-cuisine').value;
    const slot = document.getElementById('f-slot').value;
    const note = document.getElementById('f-note').value.trim();

    if (!name || !phone || !contact) {
        alert('Vui lòng điền tên nhà hàng, tên của bạn và số điện thoại.');
        return;
    }

    const btn = document.querySelector('.btn-submit');
    btn.textContent = 'Đang gửi...';
    btn.disabled = true;
    trackAnalyticsEvent('generate_lead', {
        method: 'partner_form'
    });

    fetch('https://formsubmit.co/ajax/thanhpx@mamji.vn', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        },
        body: JSON.stringify({
            _subject: 'MÂM - Đăng ký mới: ' + name,
            'Tên nhà hàng': name,
            'Loại ẩm thực': cuisine,
            'Địa chỉ': addr,
            'Người liên hệ': contact,
            'Số điện thoại': phone,
            'Khung giờ trống': slot,
            'Ghi chú': note
        })
    })
    .then(response => response.json())
    .then(data => {
        trackAnalyticsEvent('partner_form_success', {
            restaurant_type: cuisine || 'unspecified'
        });
        document.getElementById('form-content').style.display = 'none';
        document.getElementById('form-success').style.display = 'block';
    })
    .catch(error => {
        console.error('Form error:', error);
        trackAnalyticsEvent('partner_form_error', {
            restaurant_type: cuisine || 'unspecified'
        });
        document.getElementById('form-content').style.display = 'none';
        document.getElementById('form-success').style.display = 'block';
    });
}

const observer = new IntersectionObserver((entries) => {
    entries.forEach(e => {
        if (e.isIntersecting) {
            e.target.classList.add('visible');
            e.target.style.transitionDelay = '0.1s';
        }
    });
}, { threshold: 0.1 });

document.querySelectorAll('.fade-up').forEach(el => observer.observe(el));
