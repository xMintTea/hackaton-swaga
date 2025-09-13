document.addEventListener('DOMContentLoaded', function() {
    // Эффект матричного дождя
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
    
    // Символы для матричного эффекта
    const matrixChars = "01010101Cyberskill10101010コードコードコード";
    const fontSize = 14;
    let columns = Math.floor(canvas.width / fontSize);
    
    // Массив для хранения позиций капель
    let drops = [];
    for (let i = 0; i < columns; i++) {
        drops[i] = Math.floor(Math.random() * canvas.height / fontSize);
    }
    
    // Функция отрисовки матричного дождя
    function draw() {
        // Полупрозрачный черный для создания эффекта шлейфа
        ctx.fillStyle = 'rgba(10, 10, 10, 0.04)';
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
    
    // Запуск анимации матричного дождя
    setInterval(draw, 33);
    
    // Глитч-эффект для заголовка
    const title = document.querySelector('.logo');
    setInterval(() => {
        if (Math.random() > 0.9) {
            title.style.animation = 'glitch 0.3s linear';
            setTimeout(() => {
                title.style.animation = '';
            }, 300);
        }
    }, 5000);
    
    // Переключение мобильного меню
    const mobileMenuBtn = document.getElementById('mobileMenuBtn');
    const nav = document.querySelector('nav');
    
    if (mobileMenuBtn) {
        mobileMenuBtn.addEventListener('click', function() {
            this.classList.toggle('active');
            nav.classList.toggle('active');
        });
    }
    
    // Плавная прокрутка для навигационных ссылок
    document.querySelectorAll('nav a').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);
            
            if (targetElement) {
                window.scrollTo({
                    top: targetElement.offsetTop - 80,
                    behavior: 'smooth'
                });
                
                // Закрытие мобильного меню если открыто
                if (mobileMenuBtn) {
                    mobileMenuBtn.classList.remove('active');
                    nav.classList.remove('active');
                }
            }
        });
    });
    
    // Эффект скролла для хедера
    window.addEventListener('scroll', function() {
        const header = document.getElementById('header');
        if (window.scrollY > 50) {
            header.classList.add('scrolled');
        } else {
            header.classList.remove('scrolled');
        }
        
        // Анимация секции Johnny Silverhand
        const johnnySection = document.getElementById('about');
        const johnnyImage = document.getElementById('johnnyImage');
        const johnnyText = document.getElementById('johnnyText');
        
        if (johnnySection && johnnyImage && johnnyText) {
            const sectionTop = johnnySection.offsetTop;
            const sectionHeight = johnnySection.offsetHeight;
            
            if (window.scrollY > sectionTop - window.innerHeight / 2 && 
                window.scrollY < sectionTop + sectionHeight - window.innerHeight / 2) {
                johnnyImage.classList.add('visible');
                johnnyText.classList.add('visible');
            } else {
                johnnyImage.classList.remove('visible');
                johnnyText.classList.remove('visible');
            }
        }
    });
    
    // Функционал модальных окон
    const loginBtn = document.getElementById('loginBtn');
    const registerBtn = document.getElementById('registerBtn');
    const loginModal = document.getElementById('loginModal');
    const registerModal = document.getElementById('registerModal');
    const closeLoginModal = document.getElementById('closeLoginModal');
    const closeRegisterModal = document.getElementById('closeRegisterModal');
    
    if (loginBtn && loginModal) {
        loginBtn.addEventListener('click', function(e) {
            e.preventDefault();
            loginModal.style.display = 'flex';
        });
    }
    
    if (registerBtn && registerModal) {
        registerBtn.addEventListener('click', function(e) {
            e.preventDefault();
            registerModal.style.display = 'flex';
        });
    }
    
    if (closeLoginModal && loginModal) {
        closeLoginModal.addEventListener('click', function() {
            loginModal.style.display = 'none';
        });
    }
    
    if (closeRegisterModal && registerModal) {
        closeRegisterModal.addEventListener('click', function() {
            registerModal.style.display = 'none';
        });
    }
    
    // Закрытие модальных окон при клике вне их области
    window.addEventListener('click', function(e) {
        if (e.target === loginModal) {
            loginModal.style.display = 'none';
        }
        if (e.target === registerModal) {
            registerModal.style.display = 'none';
        }
    });
    
    // Обработка отправки форм
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            alert('Функционал входа будет реализован с бэкендом!');
            if (loginModal) loginModal.style.display = 'none';
        });
    }
    
    if (registerForm) {
        registerForm.addEventListener('submit', function(e) {
            e.preventDefault();
            alert('Функционал регистрации будет реализован с бэкендом!');
            if (registerModal) registerModal.style.display = 'none';
        });
    }
    
    // Загрузка данных лидерборда (заглушка)
    function loadLeaderboard() {
        const leaderboardData = [
            { rank: 1, player: 'Neo_Matrix', points: 2450 },
            { rank: 2, player: 'Cyber_Tr1x', points: 2280 },
            { rank: 3, player: 'Data_Stream', points: 2150 },
            { rank: 4, player: 'Byte_Runner', points: 1980 },
            { rank: 5, player: 'Code_Hunter', points: 1840 }
        ];
        
        const leaderboardList = document.getElementById('leaderboardList');
        if (leaderboardList) {
            leaderboardList.innerHTML = '';
            
            leaderboardData.forEach(item => {
                const itemElement = document.createElement('div');
                itemElement.className = `leaderboard-item ${item.rank <= 3 ? 'top-' + item.rank : ''}`;
                
                itemElement.innerHTML = `
                    <span class="rank">${item.rank}</span>
                    <span class="player">${item.player}</span>
                    <span class="points">${item.points}</span>
                `;
                
                leaderboardList.appendChild(itemElement);
            });
        }
    }
    
    // Инициализация лидерборда
    loadLeaderboard();
    
    // УБРАНА ФУНКЦИЯ ПРИНУДИТЕЛЬНОЙ ПРОКРУТКИ СЕКЦИЙ ПРИ СКРОЛЛЕ
    // Теперь пользователь может свободно скроллить контент
});