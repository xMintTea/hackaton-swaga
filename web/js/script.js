document.addEventListener('DOMContentLoaded', function() {
    // Matrix rain effect
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    const container = document.getElementById('matrixRain');
    
    container.appendChild(canvas);
    
    function resizeCanvas() {
        canvas.width = container.offsetWidth;
        canvas.height = container.offsetHeight;
    }
    
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);
    
    // Matrix characters
    const matrixChars = "01010101NeuroAcademy10101010コードコードコード";
    const fontSize = 14;
    let columns = Math.floor(canvas.width / fontSize);
    
    // Drops array
    let drops = [];
    for (let i = 0; i < columns; i++) {
        drops[i] = Math.floor(Math.random() * canvas.height / fontSize);
    }
    
    // Drawing function
    function draw() {
        // Semi-transparent black to create trail effect
        ctx.fillStyle = 'rgba(10, 10, 10, 0.05)';
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        ctx.fillStyle = '#00ff00';
        ctx.font = `${fontSize}px Orbitron`;
        
        for (let i = 0; i < drops.length; i++) {
            const text = matrixChars[Math.floor(Math.random() * matrixChars.length)];
            
            ctx.fillText(text, i * fontSize, drops[i] * fontSize);
            
            if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
                drops[i] = 0;
            }
            
            drops[i]++;
        }
    }
    
    // Animation loop
    setInterval(draw, 33);
    
    // Glitch effect on title
    const title = document.querySelector('.logo');
    setInterval(() => {
        if (Math.random() > 0.9) {
            title.style.animation = 'glitch 0.3s linear';
            setTimeout(() => {
                title.style.animation = '';
            }, 300);
        }
    }, 5000);
    
    // Mobile menu toggle
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const nav = document.querySelector('nav');
    
    mobileMenuBtn.addEventListener('click', function() {
        this.classList.toggle('active');
        nav.classList.toggle('active');
    });
    
    // Smooth scrolling for navigation links
    document.querySelectorAll('a[data-scroll]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('data-scroll');
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 80,
                    behavior: 'smooth'
                });
                
                // Close mobile menu if open
                mobileMenuBtn.classList.remove('active');
                nav.classList.remove('active');
            }
        });
    });
    
    // Header scroll effect
    window.addEventListener('scroll', function() {
        const header = document.querySelector('header');
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
    });
    
    // Animate progress bars
    function animateProgressBars() {
        document.querySelectorAll('.progress').forEach(progressBar => {
            const progress = progressBar.getAttribute('data-progress');
            progressBar.style.width = progress + '%';
        });
    }
    
    // Animate stats counter
    function animateStats() {
        const statElements = document.querySelectorAll('.stat-number');
        
        statElements.forEach(stat => {
            const target = parseInt(stat.getAttribute('data-target'));
            const duration = 2000; // 2 seconds
            const steps = 60; // 60 frames per second
            const stepValue = target / (duration / (1000 / steps));
            let current = 0;
            
            const timer = setInterval(() => {
                current += stepValue;
                if (current >= target) {
                    current = target;
                    clearInterval(timer);
                }
                stat.textContent = Math.floor(current);
            }, 1000 / steps);
        });
    }
    
    // Intersection Observer for animations
    const observerOptions = {
        threshold: 0.5,
        rootMargin: '0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                if (entry.target.classList.contains('courses')) {
                    animateProgressBars();
                } else if (entry.target.classList.contains('community')) {
                    animateStats();
                }
            }
        });
    }, observerOptions);
    
    // Observe sections
    const coursesSection = document.querySelector('.courses');
    const communitySection = document.querySelector('.community');
    
    if (coursesSection) observer.observe(coursesSection);
    if (communitySection) observer.observe(communitySection);
});