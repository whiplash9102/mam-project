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
            document.getElementById('roi-fee').textContent = '− ' + fmtVND(fee);
            document.getElementById('roi-net').textContent = fmtVND(net);
            document.getElementById('roi-total').textContent = fmt(net);
            document.getElementById('roi-sub').textContent = 'VND / tháng · ước tính lợi nhuận ròng';
        }

        ['slots', 'pax', 'spend'].forEach(id => {
            document.getElementById(id).addEventListener('input', calcROI);
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

            // Disable button to prevent double submit
            const btn = document.querySelector('.btn-submit');
            btn.textContent = 'Đang gửi...';
            btn.disabled = true;

            fetch('https://formsubmit.co/ajax/mamj.partner@gmail.com', {
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
                document.getElementById('form-content').style.display = 'none';
                document.getElementById('form-success').style.display = 'block';
            })
            .catch(error => {
                // Fallback: still show success and log error
                console.error('Form error:', error);
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