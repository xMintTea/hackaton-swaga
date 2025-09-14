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
    FORGOT_PASSWORD_MODAL: '#forgotPasswordModal',
    CLOSE_LOGIN_MODAL: '#closeLoginModal',
    CLOSE_REGISTER_MODAL: '#closeRegisterModal',
    CLOSE_FORGOT_PASSWORD_MODAL: '#closeForgotPasswordModal',
    LOGIN_FORM: '#loginForm',
    REGISTER_FORM: '#registerForm',
    FORGOT_PASSWORD_FORM: '#forgotPasswordForm',
    LEADERBOARD_LIST: '#leaderboardList',
    JOHNNY_IMAGE: '#johnnyImage',
    JOHNNY_TEXT: '#johnnyText',
    TOGGLE_ADMIN_BTN: '#toggleAdminBtn',
    ADMIN_SECTION: '#adminSection',
    FORGOT_PASSWORD_BTN: '#forgotPasswordBtn'
};

// Глобальные переменные для управления анимациями
let animationObservers = [];

// Основная функция инициализации
function initScripts() {
    console.log('Инициализация сайта Cyberskill...');
    
    // Создаем контейнер для уведомлений
    createNotificationContainer();
    
    // Инициализация всех модулей
    initMatrixRain();
    initAnimations();
    initNavigation();
    initModals();
    initForms();
    initLeaderboard();
    initScrollEffects();
    initAdminToggle();
    
    // Запрос разрешения на уведомления
    initNotifications();
}

// Создание контейнера для уведомлений
function createNotificationContainer() {
    const container = document.createElement('div');
    container.className = 'notification-container';
    container.id = 'notificationContainer';
    document.body.appendChild(container);
}

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
                    // Убираем начальную прозрачность после анимации
                    setTimeout(() => {
                        entry.target.style.opacity = '1';
                    }, parseInt(delay) + 1000);
                    
                }, parseInt(delay));
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
        mobileMenuBtn.addEventListener('click', function(e) {
            e.stopPropagation();
            this.classList.toggle(CLASSES.ACTIVE);
            nav.classList.toggle(CLASSES.ACTIVE);
        });
        
        // Закрытие меню при клике на ссылку
        const navLinks = nav.querySelectorAll('a');
        navLinks.forEach(link => {
            link.addEventListener('click', () => {
                mobileMenuBtn.classList.remove(CLASSES.ACTIVE);
                nav.classList.remove(CLASSES.ACTIVE);
            });
        });
        
        // Закрытие меню при клике вне его области
        document.addEventListener('click', function(e) {
            if (nav.classList.contains(CLASSES.ACTIVE) && 
                !nav.contains(e.target) && 
                e.target !== mobileMenuBtn && 
                !mobileMenuBtn.contains(e.target)) {
                mobileMenuBtn.classList.remove(CLASSES.ACTIVE);
                nav.classList.remove(CLASSES.ACTIVE);
            }
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
    const forgotPasswordModal = document.querySelector(SELECTORS.FORGOT_PASSWORD_MODAL);
    const closeLoginModal = document.querySelector(SELECTORS.CLOSE_LOGIN_MODAL);
    const closeRegisterModal = document.querySelector(SELECTORS.CLOSE_REGISTER_MODAL);
    const closeForgotPasswordModal = document.querySelector(SELECTORS.CLOSE_FORGOT_PASSWORD_MODAL);
    const forgotPasswordBtn = document.querySelector(SELECTORS.FORGOT_PASSWORD_BTN);
    
    // Функция для закрытия всех модальных окон
    function closeAllModals() {
        if (loginModal) loginModal.style.display = 'none';
        if (registerModal) registerModal.style.display = 'none';
        if (forgotPasswordModal) forgotPasswordModal.style.display = 'none';
    }
    
    // Открытие модальных окон
    if (loginBtn && loginModal) {
        loginBtn.addEventListener('click', function(e) {
            e.preventDefault();
            closeAllModals();
            loginModal.style.display = 'flex';
        });
    }
    
    if (registerBtn && registerModal) {
        registerBtn.addEventListener('click', function(e) {
            e.preventDefault();
            closeAllModals();
            registerModal.style.display = 'flex';
        });
    }
    
    if (forgotPasswordBtn && forgotPasswordModal && loginModal) {
        forgotPasswordBtn.addEventListener('click', function(e) {
            e.preventDefault();
            closeAllModals();
            forgotPasswordModal.style.display = 'flex';
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
    
    if (closeForgotPasswordModal && forgotPasswordModal) {
        closeForgotPasswordModal.addEventListener('click', function() {
            forgotPasswordModal.style.display = 'none';
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
        if (e.target === forgotPasswordModal) {
            forgotPasswordModal.style.display = 'none';
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
    const forgotPasswordForm = document.querySelector(SELECTORS.FORGOT_PASSWORD_FORM);
    const loginModal = document.querySelector(SELECTORS.LOGIN_MODAL);
    const registerModal = document.querySelector(SELECTORS.REGISTER_MODAL);
    const forgotPasswordModal = document.querySelector(SELECTORS.FORGOT_PASSWORD_MODAL);
    
    // Обработка отправки формы входа
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            
            // Показываем тестовое уведомление при нажатии на кнопку входа
            showNotification('Тест', 'Это тестовое уведомление при нажатии на кнопку входа', 'success');
            
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
            
            // В реальном приложении проверка кода должна быть на бэкенде
            // Здесь просто отправляем данные на сервер
            const formData = {
                name: document.getElementById('registerName').value,
                email: document.getElementById('registerEmail').value,
                password: document.getElementById('registerPassword').value,
                role: adminSection.style.display !== 'none' ? userRole : 'student',
                secretCode: adminSection.style.display !== 'none' ? secretCode : ''
            };
            
            console.log('Данные для регистрации:', formData);
            showNotification('Регистрация', 'Регистрация отправлена на сервер. Проверка секретного кода будет выполнена на бэкенде.', 'success');
            
            if (registerModal) registerModal.style.display = 'none';
        });
    }
    
    // Обработка отправки формы восстановления пароля
    if (forgotPasswordForm) {
        forgotPasswordForm.addEventListener('submit', function(e) {
            e.preventDefault();
            showNotification('Восстановление пароля', 'Запрос на восстановление пароля отправлен! Проверьте вашу электронную почту.', 'success');
            if (forgotPasswordModal) forgotPasswordModal.style.display = 'none';
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

// Функция для показа уведомлений
function showNotification(title, message, type = 'info') {
    const container = document.getElementById('notificationContainer');
    if (!container) return;
    
    // Создаем элемент уведомления
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    
    // Создаем содержимое уведомления
    notification.innerHTML = `
        <div class="notification-content">
            <div class="notification-title">${title}</div>
            <div class="notification-message">${message}</div>
        </div>
        <button class="notification-close">&times;</button>
    `;
    
    // Добавляем уведомление в контейнер
    container.appendChild(notification);
    
    // Показываем уведомление
    setTimeout(() => {
        notification.classList.add('slide-in');
    }, 10);
    
    // Обработчик закрытия уведомления
    const closeBtn = notification.querySelector('.notification-close');
    closeBtn.addEventListener('click', function() {
        notification.classList.remove('slide-in');
        notification.classList.add('slide-out');
        setTimeout(() => {
            if (notification.parentNode) {
                container.removeChild(notification);
            }
        }, 300);
    });
    
    // Убираем уведомление через 5 секунд
    setTimeout(() => {
        if (notification.parentNode) {
            notification.classList.remove('slide-in');
            notification.classList.add('slide-out');
            setTimeout(() => {
                if (notification.parentNode) {
                    container.removeChild(notification);
                }
            }, 300);
        }
    }, 5000);
}

// Инициализация системы уведомлений
function initNotifications() {
    // Запрос разрешения на уведомления
    if (!("Notification" in window)) {
        console.log("Этот браузер не поддерживает уведомления");
        return;
    }

    // Показываем модальное окно с запросом разрешения
    if (Notification.permission === "default") {
        setTimeout(() => {
            showNotificationPermissionModal();
        }, 3000);
    }
}

// Функция для показа модального окна запроса разрешения на уведомления
function showNotificationPermissionModal() {
    const notificationModal = document.createElement('div');
    notificationModal.className = 'modal';
    notificationModal.id = 'notificationPermissionModal';
    notificationModal.innerHTML = `
        <div class="modal-content">
            <h2 class="modal-title">Уведомления</h2>
            <p>Разрешить Cyberskill отправлять вам уведомления о новых курсах, достижениях и событиях?</p>
            <div class="modal-buttons">
                <button class="btn" id="allowNotifications">Разрешить</button>
                <button class="btn btn-pink" id="denyNotifications">Отклонить</button>
            </div>
        </div>
    `;
    
    document.body.appendChild(notificationModal);
    notificationModal.style.display = 'flex';

    // Обработчики для кнопок
    document.getElementById('allowNotifications').addEventListener('click', function() {
        Notification.requestPermission().then(permission => {
            if (permission === "granted") {
                console.log("Notification permission granted.");
                showNotification("Cyberskill", "Добро пожаловать в киберпространство!", "success");
                
                // Создаем тестовое пуш-уведомление
                if ('serviceWorker' in navigator) {
                    navigator.serviceWorker.ready.then(function(registration) {
                        registration.showNotification('Добро пожаловать в киберпространство!', {
                            body: 'Теперь вы будете получать уведомления о новых курсах и событиях',
                            icon: 'img/icon-192.png',
                            vibrate: [200, 100, 200],
                            tag: 'welcome-notification'
                        });
                    });
                }
            }
            notificationModal.style.display = 'none';
        });
    });

    document.getElementById('denyNotifications').addEventListener('click', function() {
        notificationModal.style.display = 'none';
    });
}

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
        utils,
        showNotification
    };
}