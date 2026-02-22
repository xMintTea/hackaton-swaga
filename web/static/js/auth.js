// auth.js
// Константы для API
const API_BASE_URL = 'http://localhost:8000';

// Объект для работы с аутентификацией
const auth = {
    // Проверка, авторизован ли пользователь
    isLoggedIn: function() {
        return localStorage.getItem('currentUser') !== null;
    },
    
    // Получение данных пользователя
    getUserInfo: function() {
        const userData = localStorage.getItem('currentUser');
        return userData ? JSON.parse(userData) : null;
    },
    
    // Сохранение данных пользователя после успешного входа
    login: function(userData) {
        localStorage.setItem('currentUser', JSON.stringify(userData));
        this.updateUI();
        return userData;
    },
    
    // Выход из системы
    logout: function() {
        localStorage.removeItem('currentUser');
        this.updateUI();
        // Перенаправление на главную страницу
        window.location.href = '/';
        return true;
    },
    
    // Обновление UI в зависимости от состояния авторизации
    updateUI: function() {
        const loginBtn = document.getElementById('loginBtn');
        const registerBtn = document.getElementById('registerBtn');
        const userMenu = document.getElementById('userMenu');
        
        if (!loginBtn || !registerBtn || !userMenu) return;
        
        const user = this.getUserInfo();
        
        if (user) {
            // Пользователь авторизован
            loginBtn.style.display = 'none';
            registerBtn.style.display = 'none';
            userMenu.style.display = 'block';
            
            // Обновляем данные пользователя в меню
            const userAvatar = document.getElementById('userAvatar');
            const userNickname = document.getElementById('userNickname');
            
            if (userAvatar) {
                userAvatar.src = user.avatar || '/static/img/avatars/avatar1.jpg';
                userAvatar.alt = user.nickname || user.login;
            }
            
            if (userNickname) {
                userNickname.textContent = user.nickname || user.login;
            }
            
            // Добавляем обработчик для кнопки выхода
            const logoutBtn = document.getElementById('logoutBtn');
            if (logoutBtn) {
                // Удаляем старый обработчик, чтобы избежать дублирования
                logoutBtn.replaceWith(logoutBtn.cloneNode(true));
                const newLogoutBtn = document.getElementById('logoutBtn');
                
                newLogoutBtn.addEventListener('click', (e) => {
                    e.preventDefault();
                    this.logout();
                });
            }
        } else {
            // Пользователь не авторизован
            loginBtn.style.display = 'inline-block';
            registerBtn.style.display = 'inline-block';
            userMenu.style.display = 'none';
        }
    },
    
    // Получение информации о пользователе с сервера
    getUserInfoFromServer: async function() {
        try {
            const token = this.getToken();
            if (!token) return null;
            
            const response = await fetch(`${API_BASE_URL}/auth/me`, {
                headers: {
                    'Authorization': `Bearer ${token}`
                }
            });
            
            if (response.ok) {
                return await response.json();
            }
            return null;
        } catch (error) {
            console.error('Ошибка получения данных пользователя:', error);
            return null;
        }
    },
    
    // Получение токена из localStorage
    getToken: function() {
        const userData = this.getUserInfo();
        return userData ? userData.token : null;
    }
};

// Инициализация аутентификации при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    // Проверяем авторизацию и обновляем UI
    if (auth.isLoggedIn()) {
        auth.updateUI();
    }
    
    // Обработчик кнопки выхода
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function(e) {
            e.preventDefault();
            auth.logout();
        });
    }
});

// Функция для обновления профиля пользователя
function updateUserProfile(userInfo) {
    // Заглушка - в реальном приложении здесь будет обновление данных на странице
    console.log('User info:', userInfo);
}

// Экспорт объекта auth для использования в других файлах
window.auth = auth;