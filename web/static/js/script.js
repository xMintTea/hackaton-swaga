// script4.js - Исправленная версия
const SELECTORS = {
    LOGIN_BUTTON: '#loginBtn',
    REGISTER_BUTTON: '#registerBtn',
    FORGOT_PASSWORD_BUTTON: '#forgotPasswordBtn',
    LOGIN_FORM: '#loginForm',
    REGISTER_FORM: '#registerForm',
    FORGOT_PASSWORD_FORM: '#forgotPasswordForm',
    LOGIN_MODAL: '#loginModal',
    REGISTER_MODAL: '#registerModal',
    FORGOT_PASSWORD_MODAL: '#forgotPasswordModal'
};

console.log("Инициализация модальных окон...");

function initModals() {
    console.log('Инициализация модальных окон...');
    
    // Находим кнопки открытия модальных окон
    const loginBtn = document.querySelector(SELECTORS.LOGIN_BUTTON);
    const registerBtn = document.querySelector(SELECTORS.REGISTER_BUTTON);
    const forgotPasswordBtn = document.getElementById('forgotPasswordBtn');
    
    // Находим модальные окна
    const loginModal = document.querySelector(SELECTORS.LOGIN_MODAL);
    const registerModal = document.querySelector(SELECTORS.REGISTER_MODAL);
    const forgotPasswordModal = document.querySelector(SELECTORS.FORGOT_PASSWORD_MODAL);
    
    // Находим кнопки закрытия
    const closeLoginModal = document.getElementById('closeLoginModal');
    const closeRegisterModal = document.getElementById('closeRegisterModal');
    const closeForgotPasswordModal = document.getElementById('closeForgotPasswordModal');
    
    // Отладочная информация
    console.log('Найдены элементы:', {
        loginBtn: !!loginBtn,
        registerBtn: !!registerBtn,
        loginModal: !!loginModal,
        registerModal: !!registerModal
    });
    
    // Обработчик для кнопки "Вы не ученик?" (переключение секции админа)
    const toggleAdminBtn = document.getElementById('toggleAdminBtn');
    if (toggleAdminBtn) {
        toggleAdminBtn.addEventListener('click', function(e) {
            e.preventDefault();
            const adminSection = document.getElementById('adminSection');
            if (adminSection) {
                adminSection.style.display = adminSection.style.display === 'none' ? 'block' : 'none';
            }
        });
    }
    
    // Открытие модальных окон
    if (loginBtn && loginModal) {
        loginBtn.addEventListener('click', function() {
            console.log('Открытие окна входа');
            loginModal.style.display = 'flex';
            document.body.style.overflow = 'hidden'; // Блокируем скролл
        });
    } else {
        console.warn('Не найдена кнопка входа или модальное окно');
    }
    
    if (registerBtn && registerModal) {
        registerBtn.addEventListener('click', function() {
            console.log('Открытие окна регистрации');
            registerModal.style.display = 'flex';
            document.body.style.overflow = 'hidden'; // Блокируем скролл
        });
    } else {
        console.warn('Не найдена кнопка регистрации или модальное окно');
    }
    
    if (forgotPasswordBtn && forgotPasswordModal) {
        forgotPasswordBtn.addEventListener('click', function() {
            forgotPasswordModal.style.display = 'flex';
            document.body.style.overflow = 'hidden';
        });
    }
    
    // Закрытие модальных окон
    if (closeLoginModal && loginModal) {
        closeLoginModal.addEventListener('click', function() {
            loginModal.style.display = 'none';
            document.body.style.overflow = ''; // Восстанавливаем скролл
        });
    }
    
    if (closeRegisterModal && registerModal) {
        closeRegisterModal.addEventListener('click', function() {
            registerModal.style.display = 'none';
            document.body.style.overflow = '';
        });
    }
    
    if (closeForgotPasswordModal && forgotPasswordModal) {
        closeForgotPasswordModal.addEventListener('click', function() {
            forgotPasswordModal.style.display = 'none';
            document.body.style.overflow = '';
        });
    }
    
    // Закрытие при клике вне модального окна
    window.addEventListener('click', function(event) {
        if (event.target === loginModal) {
            loginModal.style.display = 'none';
            document.body.style.overflow = '';
        }
        if (event.target === registerModal) {
            registerModal.style.display = 'none';
            document.body.style.overflow = '';
        }
        if (event.target === forgotPasswordModal) {
            forgotPasswordModal.style.display = 'none';
            document.body.style.overflow = '';
        }
    });
    
    // Обработчики форм
    const loginForm = document.getElementById('loginForm');
    const registerForm = document.getElementById('registerForm');
    const forgotPasswordForm = document.getElementById('forgotPasswordForm');
    
    if (loginForm) {
        loginForm.addEventListener('submit', function(e) {
            e.preventDefault();
            console.log('Отправка формы входа');
            // Здесь будет обработка входа
            loginModal.style.display = 'none';
            document.body.style.overflow = '';
        });
    }
    
    if (registerForm) {
        registerForm.addEventListener('submit', function(e) {
            e.preventDefault();
            console.log('Отправка формы регистрации');
            // Здесь будет обработка регистрации
            registerModal.style.display = 'none';
            document.body.style.overflow = '';
        });
    }
    
    if (forgotPasswordForm) {
        forgotPasswordForm.addEventListener('submit', function(e) {
            e.preventDefault();
            console.log('Восстановление пароля');
            // Здесь будет восстановление пароля
            forgotPasswordModal.style.display = 'none';
            document.body.style.overflow = '';
        });
    }
}

// Делаем функцию глобально доступной
window.initModals = initModals;

// Инициализация при загрузке DOM
document.addEventListener('DOMContentLoaded', function() {
    // Проверяем, загружен ли уже header
    const headerLoaded = document.querySelector(SELECTORS.LOGIN_BUTTON);
    if (headerLoaded) {
        initModals();
    }
    // Если нет, templateLoader.js вызовет initScripts() после загрузки шаблонов
});