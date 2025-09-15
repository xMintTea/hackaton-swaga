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


function updateUI() {
    const token = localStorage.getItem('access_token');
    const loginBtn = document.getElementById('loginBtn');
    const logoutBtn = document.getElementById('logoutBtn');
    const userInfo = document.getElementById('userInfo');
    
    if (token) {
        // Пользователь авторизован
        if (loginBtn) loginBtn.style.display = 'none';
        if (logoutBtn) logoutBtn.style.display = 'block';
        if (userInfo) userInfo.style.display = 'block';
    } else {
        // Пользователь не авторизован
        if (loginBtn) loginBtn.style.display = 'block';
        if (logoutBtn) logoutBtn.style.display = 'none';
        if (userInfo) userInfo.style.display = 'none';
    }
}


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
    // Успешная авторизация
    const data = await response.json();
    
    // Отладочная информация
    console.log('Токен получен:', data.access_token);
    
    // Сохраняем токены
    localStorage.setItem('access_token', data.access_token);
    localStorage.setItem('refresh_token', data.refresh_token);
    
    // Проверяем сохранение
    console.log('Токен сохранен в localStorage:', localStorage.getItem('access_token'));
    
    // Показываем уведомление об успехе
    showNotification('Успех', 'Вы успешно вошли в систему', 'success');
    
    // Закрываем модальное окно
    if (loginModal) loginModal.style.display = 'none';
    
    // Обновляем интерфейс
    if (typeof auth !== 'undefined' && typeof auth.updateUI === 'function') {
        auth.updateUI();
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