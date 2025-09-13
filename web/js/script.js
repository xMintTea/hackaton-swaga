// Константы для классов и идентификаторов
const CLASSES = {
    VISIBLE: 'visible',
    ANIMATED: 'animate__animated',
    SCROLLED: 'scrolled',
    ACTIVE: 'active',
    ANIMATE_ON_SCROLL: 'animate-on-scroll'
};

const SELECTORS = {
    HEADER: '#header',
    MATRIX_RAIN: '#matrixRain',
    MOBILE_MENU_BTN: '#mobileMenuBtn',
    LOGIN_BTN: '#loginBtn',
    REGISTER_BTN: '#registerBtn',
    LOGIN_MODAL: '#loginModal',
    REGISTER_MODAL: '#registerModal',
    CLOSE_LOGIN_MODAL: '#closeLoginModal',
    CLOSE_REGISTER_MODAL: '#closeRegisterModal',
    LOGIN_FORM: '#loginForm',
    REGISTER_FORM: '#registerForm',
    LEADERBOARD_LIST: '#leaderboardList',
    JOHNNY_IMAGE: '#johnnyImage',
    JOHNNY_TEXT: '#johnnyText',
    TOGGLE_ADMIN_BTN: '#toggleAdminBtn',
    ADMIN_SECTION: '#adminSection'
};

// Глобальные переменные для управления анимациями
let animationObservers = [];

// Основная функция инициализации
document.addEventListener('DOMContentLoaded', function() {
    console.log('Инициализация сайта Cyberskill...');
    
    // Инициализация всех модулей
    initMatrixRain();
    initAnimations();
    initNavigation();
    initModals();
    initForms();
    initLeaderboard();
    initScrollEffects();
    initAdminToggle();
});

// Инициализация матричного дождя
function initMatrixRain() {
    const canvas = document.createElement('canvas');
    const ctx = canvas.getContext('2d');
    const container = document.querySelector(SELECTORS.MATRIX_RAIN);
    
    if (!container) return;
    
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
    if (title) {
        setInterval(() => {
            if (Math.random() > 0.9) {
                title.style.animation = 'glitch 0.3s linear';
                setTimeout(() => {
                    title.style.animation = '';
                }, 300);
            }
        }, 5000);
    }
}

// Инициализация анимаций
function initAnimations() {
    console.log('Инициализация анимаций...');
    
    // Анимация появления элементов при скролле
    const animatedElements = document.querySelectorAll('.' + CLASSES.ANIMATE_ON_SCROLL);
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const animation = entry.target.getAttribute('data-animation') || 'animate__fadeInUp';
                const delay = entry.target.getAttribute('data-delay') || 0;
                
                setTimeout(() => {
                    entry.target.classList.add(CLASSES.ANIMATED, animation);
                    
                    // Удаляем класс анимации после завершения для возможности повторного запуска
                    const animationDuration = parseInt(getComputedStyle(entry.target).animationDuration.replace('s', '')) * 1000 || 1000;
                    setTimeout(() => {
                        entry.target.classList.remove(CLASSES.ANIMATED, animation);
                    }, animationDuration);
                    
                }, parseInt(delay));
            } else {
                // Сбрасываем анимацию при выходе из viewport
                const animation = entry.target.getAttribute('data-animation') || 'animate__fadeInUp';
                entry.target.classList.remove(CLASSES.ANIMATED, animation);
            }
        });
    }, { threshold: 0.1 });
    
    animatedElements.forEach(element => {
        observer.observe(element);
    });
    
    // Сохраняем observer для последующей очистки
    animationObservers.push(observer);
}

// Инициализация навигации
function initNavigation() {
    console.log('Инициализация навигации...');
    
    // Переключение мобильного меню
    const mobileMenuBtn = document.querySelector(SELECTORS.MOBILE_MENU_BTN);
    const nav = document.querySelector('nav');
    
    if (mobileMenuBtn && nav) {
        mobileMenuBtn.addEventListener('click', function() {
            this.classList.toggle(CLASSES.ACTIVE);
            nav.classList.toggle(CLASSES.ACTIVE);
        });
    }
    
    // Плавная прокрутка для навигационных ссылок
    document.querySelectorAll('nav a').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            // Для внешних ссылок не предотвращаем стандартное поведение
            if (this.getAttribute('href').startsWith('http') || this.getAttribute('href').includes('.html')) {
                return;
            }
            
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
                    mobileMenuBtn.classList.remove(CLASSES.ACTIVE);
                    nav.classList.remove(CLASSES.ACTIVE);
                }
            }
        });
    });
}

// Инициализация модальных окон
function initModals() {
    console.log('Инициализация модальных окон...');
    
    const loginBtn = document.querySelector(SELECTORS.LOGIN_BTN);
    const registerBtn = document.querySelector(SELECTORS.REGISTER_BTN);
    const loginModal = document.querySelector(SELECTORS.LOGIN_MODAL);
    const registerModal = document.querySelector(SELECTORS.REGISTER_MODAL);
    const closeLoginModal = document.querySelector(SELECTORS.CLOSE_LOGIN_MODAL);
    const closeRegisterModal = document.querySelector(SELECTORS.CLOSE_REGISTER_MODAL);
    
    // Открытие модальных окон
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
    
    // Закрытие модальных окон
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
}

// Инициализация переключателя режима администратора
function initAdminToggle() {
    console.log('Инициализация переключателя администратора...');
    
    const toggleAdminBtn = document.querySelector(SELECTORS.TOGGLE_ADMIN_BTN);
    const adminSection = document.querySelector(SELECTORS.ADMIN_SECTION);
    
    if (toggleAdminBtn && adminSection) {
        toggleAdminBtn.addEventListener('click', function(e) {
            e.preventDefault();
            
            if (adminSection.style.display === 'none') {
                adminSection.style.display = 'block';
                this.textContent = 'Я ученик';
            } else {
                adminSection.style.display = 'none';
                this.textContent = 'Вы не ученик?';
            }
        });
    }
}

// Инициализация форм
function initForms() {
    console.log('Инициализация форм...');
    
    const loginForm = document.querySelector(SELECTORS.LOGIN_FORM);
    const registerForm = document.querySelector(SELECTORS.REGISTER_FORM);
    const loginModal = document.querySelector(SELECTORS.LOGIN_MODAL);
    const registerModal = document.querySelector(SELECTORS.REGISTER_MODAL);
    
    // Обработка отправки формы входа
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            alert('Функционал входа будет реализован с бэкендом!');
            if (loginModal) loginModal.style.display = 'none';
        });
    }
    
    // Обработка отправки формы регистрации
    if (registerForm) {
        registerForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            const secretCode = document.getElementById('secretCode').value;
            const userRole = document.getElementById('userRole').value;
            const adminSection = document.querySelector(SELECTORS.ADMIN_SECTION);
            
            // Проверка секретного кода (на фронтенде, на бэкенде будет дополнительная проверка)
            if (adminSection.style.display !== 'none') {
                if (!secretCode) {
                    alert('Пожалуйста, введите секретный код');
                    return;
                }
                
                // Проверка кодов (временно, должно быть на бэкенде)
                const validCodes = {
                    'teacher': 'TEACHER2025',
                    'admin': 'ADMIN256'
                };
                
                if (userRole === 'teacher' && secretCode !== validCodes.teacher) {
                    alert('Неверный код для преподавателя');
                    return;
                }
                
                if (userRole === 'admin' && secretCode !== validCodes.admin) {
                    alert('Неверный код для администратора');
                    return;
                }
            }
            
            alert(`Регистрация успешна! Роль: ${adminSection.style.display !== 'none' ? userRole : 'student'}`);
            if (registerModal) registerModal.style.display = 'none';
        });
    }
}

// Инициализация лидерборда
function initLeaderboard() {
    console.log('Инициализация лидерборда...');
    
    const leaderboardList = document.querySelector(SELECTORS.LEADERBOARD_LIST);
    if (!leaderboardList) return;
    
    // Загрузка данных лидерборда (заглушка)
    const leaderboardData = [
        { rank: 1, player: 'Neo_Matrix', points: 2450 },
        { rank: 2, player: 'Cyber_Tr1x', points: 2280 },
        { rank: 3, player: 'Data_Stream', points: 2150 },
        { rank: 4, player: 'Byte_Runner', points: 1980 },
        { rank: 5, player: 'Code_Hunter', points: 1840 }
    ];
    
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

// Инициализация эффектов скролла
function initScrollEffects() {
    console.log('Инициализация эффектов скролла...');
    
    const header = document.querySelector(SELECTORS.HEADER);
    const johnnySection = document.getElementById('about');
    const johnnyImage = document.querySelector(SELECTORS.JOHNNY_IMAGE);
    const johnnyText = document.querySelector(SELECTORS.JOHNNY_TEXT);
    
    // Эффект скролла для хедера
    window.addEventListener('scroll', function() {
        if (header) {
            if (window.scrollY > 50) {
                header.classList.add(CLASSES.SCROLLED);
            } else {
                header.classList.remove(CLASSES.SCROLLED);
            }
        }
        
        // Анимация секции Johnny Silverhand
        if (johnnySection && johnnyImage && johnnyText) {
            const sectionTop = johnnySection.offsetTop;
            const sectionHeight = johnnySection.offsetHeight;
            
            if (window.scrollY > sectionTop - window.innerHeight / 2 && 
                window.scrollY < sectionTop + sectionHeight - window.innerHeight / 2) {
                johnnyImage.classList.add(CLASSES.VISIBLE);
                johnnyText.classList.add(CLASSES.VISIBLE);
            } else {
                johnnyImage.classList.remove(CLASSES.VISIBLE);
                johnnyText.classList.remove(CLASSES.VISIBLE);
            }
        }
    });
}

// Утилитарные функции
const utils = {
    // Форматирование чисел
    formatNumber: function(num) {
        return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    },
    
    // Генерация случайного числа в диапазоне
    randomInt: function(min, max) {
        return Math.floor(Math.random() * (max - min + 1)) + min;
    },
    
    // Проверка поддержки WebGL
    supportsWebGL: function() {
        try {
            const canvas = document.createElement('canvas');
            return !!window.WebGLRenderingContext && 
                (canvas.getContext('webgl') || canvas.getContext('experimental-webgl'));
        } catch (e) {
            return false;
        }
    },
    
    // Очистка всех observers
    cleanupObservers: function() {
        animationObservers.forEach(observer => {
            observer.disconnect();
        });
        animationObservers = [];
    }
};

// Обработка изменения размера окна
window.addEventListener('resize', function() {
    // Переинициализация анимаций при изменении размера окна
    utils.cleanupObservers();
    initAnimations();
});

// Экспорт для использования в других модулях (если нужно)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        initMatrixRain,
        initAnimations,
        initNavigation,
        initModals,
        initForms,
        initLeaderboard,
        initScrollEffects,
        initAdminToggle,
        utils
    };
}