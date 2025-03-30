 
    // Preloader animation
    document.addEventListener('DOMContentLoaded', function() {
        setTimeout(() => {
            document.querySelector('.preloader-line').style.width = '100%';
            
            setTimeout(() => {
                document.querySelector('.preloader').style.opacity = '0';
                document.querySelector('.preloader').style.visibility = 'hidden';
                
                // Initialize animations after preloader
                initAnimations();
                
                // Show cursor
                document.querySelector('.cursor').style.opacity = '1';
                document.querySelector('.cursor-follower').style.opacity = '1';
            }, 3000);
        }, 500);
    });
    
    // Custom cursor
    document.addEventListener('mousemove', function(e) {
        const cursor = document.querySelector('.cursor');
        const follower = document.querySelector('.cursor-follower');
        
        cursor.style.left = e.clientX + 'px';
        cursor.style.top = e.clientY + 'px';
        
        setTimeout(() => {
            follower.style.left = e.clientX + 'px';
            follower.style.top = e.clientY + 'px';
        }, 100);
    });
    
    // Cursor effects on links
    document.querySelectorAll('a, button').forEach(item => {
        item.addEventListener('mouseenter', () => {
            document.querySelector('.cursor').style.transform = 'translate(-50%, -50%) scale(1.5)';
            document.querySelector('.cursor-follower').style.transform = 'translate(-50%, -50%) scale(1.5)';
            document.querySelector('.cursor-follower').style.border = '1px solid rgba(16, 185, 129, 0.5)';
        });
        
        item.addEventListener('mouseleave', () => {
            document.querySelector('.cursor').style.transform = 'translate(-50%, -50%) scale(1)';
            document.querySelector('.cursor-follower').style.transform = 'translate(-50%, -50%) scale(1)';
            document.querySelector('.cursor-follower').style.border = '1px solid rgba(255, 255, 255, 0.3)';
        });
    });
    
    // Navbar scroll effect
    window.addEventListener('scroll', function() {
        const navbar = document.getElementById('navbar');
        if (window.scrollY > 50) {
            navbar.classList.add('bg-slate-900', 'shadow-md', 'py-4');
            navbar.classList.remove('py-6');
        } else {
            navbar.classList.remove('bg-slate-900', 'shadow-md', 'py-4');
            navbar.classList.add('py-6');
        }
    });
    
    // Mobile menu toggle
    document.getElementById('menu-toggle').addEventListener('click', function() {
        this.classList.toggle('open');
        document.querySelector('.mobile-menu').classList.toggle('open');
    });
    
    // Scroll animations
    function initAnimations() {
        const fadeElements = document.querySelectorAll('.fade-up, .fade-in');
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    entry.target.classList.add('appear');
                    observer.unobserve(entry.target);
                }
            });
        }, {
            rootMargin: '0px',
            threshold: 0.1
        });
        
        fadeElements.forEach(element => {
            observer.observe(element);
        });
        
        // Immediately show elements above the fold
        document.querySelectorAll('.hero .fade-up, .hero .fade-in').forEach(element => {
            setTimeout(() => {
                element.classList.add('appear');
            }, 300);
        });
    }