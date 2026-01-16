// Константы для API
const API_BASE_URL = 'http://localhost:8000';

// Функции для работы с аутентификацией


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
