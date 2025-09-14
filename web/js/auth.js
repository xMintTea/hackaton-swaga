// Константы для API
const API_BASE_URL = 'http://localhost:8000';

// Функции для работы с аутентификацией
const auth = {
    // Сохранение токена
    setToken: function(token) {
        localStorage.setItem('access_token', token);
        this.updateUI();
    },
    
    // Получение токена
    getToken: function() {
        return localStorage.getItem('access_token');
    },
    
    // Удаление токена
    removeToken: function() {
        localStorage.removeItem('access_token');
        this.updateUI();
    },
    
    // Проверка авторизации
    isLoggedIn: function() {
        return this.getToken() !== null;
    },
    
    // Обновление интерфейса в зависимости от статуса авторизации
    updateUI: function() {
        const loginBtn = document.getElementById('loginBtn');
        const registerBtn = document.getElementById('registerBtn');
        const userMenu = document.getElementById('userMenu');
        const profileBtn = document.getElementById('profileBtn');
        const logoutBtn = document.getElementById('logoutBtn');
        
        if (this.isLoggedIn()) {
            if (loginBtn) loginBtn.style.display = 'none';
            if (registerBtn) registerBtn.style.display = 'none';
            if (userMenu) userMenu.style.display = 'flex';
        } else {
            if (loginBtn) loginBtn.style.display = 'inline-block';
            if (registerBtn) registerBtn.style.display = 'inline-block';
            if (userMenu) userMenu.style.display = 'none';
        }
    },
    
    // Выход из системы
    logout: function() {
        this.removeToken();
        window.location.href = 'index.html';
    },
    
    // Получение информации о пользователе
    getUserInfo: async function() {
        const token = this.getToken();
        
        if (!token) {
            return null;
        }
        
        try {
            const response = await fetch(`${API_BASE_URL}/users/me`, {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            
            if (response.ok) {
                return await response.json();
            } else {
                console.error('Failed to fetch user info');
                return null;
            }
        } catch (error) {
            console.error('Error:', error);
            return null;
        }
    }
};

// Инициализация аутентификации при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    auth.updateUI();
    
    // Обработчик кнопки выхода
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function(e) {
            e.preventDefault();
            auth.logout();
        });
    }
    
    // Если пользователь авторизован, загружаем информацию о нем
    if (auth.isLoggedIn()) {
        auth.getUserInfo().then(userInfo => {
            if (userInfo) {
                // Обновляем интерфейс с данными пользователя
                updateUserProfile(userInfo);
            }
        });
    }
});

// Функция для обновления профиля пользователя
function updateUserProfile(userInfo) {
    // Заглушка - в реальном приложении здесь будет обновление данных на странице
    console.log('User info:', userInfo);
}

// Обработка формы входа
document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const email = document.getElementById('loginEmail').value;
            const password = document.getElementById('loginPassword').value;
            
            try {
                const formData = new FormData();
                formData.append('username', email);
                formData.append('password', password);
                
                const response = await fetch(`${API_BASE_URL}/login/`, {
                    method: 'POST',
                    body: new URLSearchParams(formData),
                    headers: {
                        'Content-Type': 'application/x-www-form-urlencoded',
                    },
                });
                
                if (response.ok) {
                    const tokenData = await response.json();
                    auth.setToken(tokenData.access_token);
                    
                    // Закрываем модальное окно
                    const loginModal = document.getElementById('loginModal');
                    if (loginModal) {
                        loginModal.style.display = 'none';
                    }
                    
                    // Показываем уведомление
                    if (window.showNotification) {
                        window.showNotification('Вход выполнен успешно!');
                    }

                    // Показываем тестовое пуш-уведомление
                    if ('serviceWorker' in navigator && Notification.permission === 'granted') {
                        navigator.serviceWorker.ready.then(function(registration) {
                            registration.showNotification('Вход выполнен', {
                                body: 'Добро пожаловать в киберпространство!',
                                icon: 'img/icon-192.png',
                                vibrate: [200, 100, 200],
                                tag: 'login-notification'
                            });
                        });
                    }
                } else {
                    if (window.showNotification) {
                        window.showNotification('Ошибка входа. Проверьте данные.', 'error');
                    }
                }
            } catch (error) {
                console.error('Error:', error);
                if (window.showNotification) {
                    window.showNotification('Ошибка соединения.', 'error');
                }
            }
        });
    }
});