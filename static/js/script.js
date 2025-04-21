// =================== Preloader ===================
const preloader = document.getElementById('preloader');
const preloaderCounter = document.getElementById('preloader-counter');
const preloaderBar = document.getElementById('preloader-bar');

// Hide all content except preloader at the start
document.body.classList.add('preloader-active');

let preloaderCount = 0;
const preloaderInterval = setInterval(() => {
    preloaderCount++;
    if (preloaderCounter) preloaderCounter.textContent = preloaderCount;
    if (preloaderBar) preloaderBar.style.width = `${preloaderCount}%`;

    if (preloaderCount >= 100) {
        clearInterval(preloaderInterval);
        setTimeout(() => {
            if (preloader) preloader.style.opacity = '0';
            setTimeout(() => {
                if (preloader) preloader.style.display = 'none';
                document.body.classList.remove('preloader-active'); // Show content
                animateRevealElements();
                animateChartBars();
                animateCounters();
                initCharts?.();
            }, 0);
        }, 200);
    }
}, 20);


// =================== Custom Cursor ===================
const cursor = document.querySelector('.cursor');
const cursorFollower = document.querySelector('.cursor-follower');

document.addEventListener('mousemove', (e) => {
    if (cursor) {
        cursor.style.left = e.clientX + 'px';
        cursor.style.top = e.clientY + 'px';
    }

    setTimeout(() => {
        if (cursorFollower) {
            cursorFollower.style.left = e.clientX + 'px';
            cursorFollower.style.top = e.clientY + 'px';
        }
    }, 100);
});


// =================== Magnetic Hover Effect ===================
const magneticElements = document.querySelectorAll('.magnetic-hover');

magneticElements.forEach(elem => {
    elem.addEventListener('mousemove', (e) => {
        const rect = elem.getBoundingClientRect();
        const x = e.clientX - rect.left - rect.width / 2;
        const y = e.clientY - rect.top - rect.height / 2;
        elem.style.transform = `translate(${x * 0.2}px, ${y * 0.2}px)`;
    });

    elem.addEventListener('mouseleave', () => {
        elem.style.transform = 'translate(0px, 0px)';
    });
});


// =================== Reveal On Scroll ===================
function animateRevealElements() {
    const reveals = document.querySelectorAll('.reveal');

    reveals.forEach((el, index) => {
        setTimeout(() => {
            el.classList.add('active');
        }, 200 * index);
    });

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('active');
                observer.unobserve(entry.target);
            }
        });
    }, { threshold: 0.1 });

    reveals.forEach(reveal => {
        observer.observe(reveal);
    });
}


// =================== Animate Chart Bars ===================
function animateChartBars() {
    const chartBars = document.querySelectorAll('.chart-bar');
    setTimeout(() => {
        chartBars.forEach(bar => {
            const height = bar.getAttribute('data-height');
            if (height) {
                bar.style.height = height;
            }
        });
    }, 500);
}


// =================== Counter Animations ===================
function animateCounters() {
    animateCounter('counter-1', 160, 2000);
    animateCounter('counter-2', 16, 2000);
    animateCounter('counter-3', 79, 2000);
}

function animateCounter(id, targetValue, duration) {
    const counter = document.getElementById(id);
    if (!counter) return;

    const startTime = Date.now();
    const startValue = 0;

    function updateCounter() {
        const currentTime = Date.now();
        const elapsedTime = currentTime - startTime;

        if (elapsedTime < duration) {
            const progress = elapsedTime / duration;
            const currentValue = Math.floor(progress * targetValue);
            counter.textContent = currentValue;
            requestAnimationFrame(updateCounter);
        } else {
            counter.textContent = targetValue;
        }
    }

    updateCounter();
}


// =================== Mobile Menu Toggle ===================
document.addEventListener('DOMContentLoaded', function () {
    const mobileMenuButton = document.getElementById('mobile-menu-button');
    const closeMenuButton = document.getElementById('close-menu-button');
    const mobileMenu = document.getElementById('mobile-menu');

    if (mobileMenuButton && closeMenuButton && mobileMenu) {
        // Toggle menu visibility when hamburger is clicked
        mobileMenuButton.addEventListener('click', function () {
            mobileMenu.classList.toggle('hidden');
        });

        // Close menu when close button is clicked
        closeMenuButton.addEventListener('click', function () {
            mobileMenu.classList.add('hidden');
        });

        // Close menu when clicking a nav link (for better UX)
        const navLinks = document.querySelectorAll('.nav-link');
        navLinks.forEach(link => {
            link.addEventListener('click', function () {
                if (window.innerWidth < 640) {
                    mobileMenu.classList.add('hidden');
                }
            });
        });

        // Handle window resize
        window.addEventListener('resize', function () {
            if (window.innerWidth >= 640) {
                mobileMenu.classList.remove('hidden');
            } else {
                mobileMenu.classList.add('hidden');
            }
        });
    }
});
