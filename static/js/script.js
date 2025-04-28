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
             
             
              
               
            }, 0);
        }, 200);
    }
}, 20);



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
