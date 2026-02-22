// profile.js - добавляем функциональность смены аватара

document.addEventListener('DOMContentLoaded', function() {
    // Элементы для работы с аватаром
    const changeAvatarBtn = document.getElementById('changeAvatarBtn');
    const avatarModal = document.getElementById('avatarModal');
    const closeAvatarModal = document.getElementById('closeAvatarModal');
    const confirmAvatarBtn = document.getElementById('confirmAvatarBtn');
    const avatarsGrid = document.querySelector('.avatars-grid');
    const userAvatar = document.getElementById('userAvatar');
    
    let selectedAvatarId = null;
    let currentAvatarId = null;
    
    // Открытие модального окна для выбора аватара
    if (changeAvatarBtn) {
        changeAvatarBtn.addEventListener('click', async function() {
            await loadAvatars();
            avatarModal.style.display = 'flex';
        });
    }
    
    // Закрытие модального окна
    if (closeAvatarModal) {
        closeAvatarModal.addEventListener('click', function() {
            avatarModal.style.display = 'none';
        });
    }
    
    // Загрузка доступных аватаров
    async function loadAvatars() {
        try {
            const userId = document.body.dataset.userId;
            if (!userId) {
                console.error('User ID not found');
                return;
            }
            
            const response = await fetch(`/api/users/${userId}/avatars`);
            if (!response.ok) {
                throw new Error('Failed to load avatars');
            }
            
            const data = await response.json();
            displayAvatars(data);
        } catch (error) {
            console.error('Error loading avatars:', error);
            showNotification('Ошибка загрузки аватаров', 'error');
        }
    }
    
    // Отображение аватаров в модальном окне
    function displayAvatars(data) {
        if (!avatarsGrid) return;
        
        avatarsGrid.innerHTML = '';
        const currentAvatar = data.current_avatar;
        const availableAvatars = data.available_avatars || [];
        
        // Добавляем стандартные публичные аватары
        const defaultAvatars = [
            { id: 1, name: 'Базовый аватар', image_url: '/static/img/avatars/avatar1.jpg', is_public: true },
            { id: 2, name: 'Кибер-аватар', image_url: '/static/img/avatars/avatar2.jpg', is_public: true },
            { id: 3, name: 'Хакерский аватар', image_url: '/static/img/avatars/avatar3.jpg', is_public: true },
            { id: 4, name: 'Премиум аватар', image_url: '/static/img/avatars/avatar4.jpg', is_public: false }
        ];
        
        // Объединяем все аватары
        const allAvatars = [...defaultAvatars];
        
        allAvatars.forEach(avatar => {
            const avatarElement = document.createElement('div');
            avatarElement.className = 'avatar-option';
            avatarElement.dataset.avatarId = avatar.id;
            
            // Проверяем, доступен ли аватар
            const isAvailable = avatar.is_public || 
                availableAvatars.some(a => a.id === avatar.id) || 
                (currentAvatar && currentAvatar.id === avatar.id);
            
            if (!isAvailable) {
                avatarElement.classList.add('locked');
            }
            
            // Проверяем, является ли текущим аватаром
            if (currentAvatar && currentAvatar.id === avatar.id) {
                avatarElement.classList.add('selected');
                selectedAvatarId = avatar.id;
                currentAvatarId = avatar.id;
            }
            
            const img = document.createElement('img');
            img.src = avatar.image_url;
            img.alt = avatar.name;
            
            avatarElement.appendChild(img);
            
            // Добавляем иконку замка для недоступных аватаров
            if (!isAvailable) {
                const lockOverlay = document.createElement('div');
                lockOverlay.className = 'lock-overlay';
                lockOverlay.textContent = '🔒';
                avatarElement.appendChild(lockOverlay);
            }
            
            // Обработчик клика
            avatarElement.addEventListener('click', function() {
                if (this.classList.contains('locked')) {
                    showNotification('Этот аватар заблокирован. Приобретите его в магазине.', 'error');
                    return;
                }
                
                document.querySelectorAll('.avatar-option').forEach(opt => {
                    opt.classList.remove('selected');
                });
                
                this.classList.add('selected');
                selectedAvatarId = this.dataset.avatarId;
            });
            
            avatarsGrid.appendChild(avatarElement);
        });
    }
    
    // Подтверждение выбора аватара
    if (confirmAvatarBtn) {
        confirmAvatarBtn.addEventListener('click', async function() {
            if (!selectedAvatarId || selectedAvatarId === currentAvatarId) {
                avatarModal.style.display = 'none';
                return;
            }
            
            try {
                const userId = document.body.dataset.userId;
                const response = await fetch(`/api/users/${userId}/avatar`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ avatar_id: parseInt(selectedAvatarId) })
                });
                
                if (!response.ok) {
                    const error = await response.json();
                    throw new Error(error.detail || 'Failed to change avatar');
                }
                
                const data = await response.json();
                
                // Обновляем аватар на странице
                const selectedAvatar = document.querySelector(`.avatar-option[data-avatar-id="${selectedAvatarId}"] img`);
                if (selectedAvatar) {
                    userAvatar.src = selectedAvatar.src;
                }
                
                avatarModal.style.display = 'none';
                showNotification('Аватар успешно изменен!', 'success');
                
            } catch (error) {
                console.error('Error changing avatar:', error);
                showNotification(error.message || 'Ошибка при смене аватара', 'error');
            }
        });
    }
    
    // Функция показа уведомлений
    function showNotification(message, type) {
        // Создаем контейнер для уведомлений, если его нет
        let notificationContainer = document.querySelector('.notification-container');
        if (!notificationContainer) {
            notificationContainer = document.createElement('div');
            notificationContainer.className = 'notification-container';
            document.body.appendChild(notificationContainer);
        }
        
        const notification = document.createElement('div');
        notification.className = `notification ${type}`;
        notification.innerHTML = `
            <div class="notification-content">
                <div class="notification-title">${type === 'success' ? 'Успех' : 'Ошибка'}</div>
                <div class="notification-message">${message}</div>
            </div>
            <button class="notification-close">&times;</button>
        `;
        
        notificationContainer.appendChild(notification);
        
        // Анимация появления
        setTimeout(() => {
            notification.classList.add('slide-in');
        }, 10);
        
        // Автоматическое скрытие через 5 секунд
        setTimeout(() => {
            notification.classList.remove('slide-in');
            notification.classList.add('slide-out');
            setTimeout(() => {
                notification.remove();
            }, 300);
        }, 5000);
        
        // Закрытие по клику
        notification.querySelector('.notification-close').addEventListener('click', function() {
            notification.classList.remove('slide-in');
            notification.classList.add('slide-out');
            setTimeout(() => {
                notification.remove();
            }, 300);
        });
    }
    
    // Закрытие модального окна при клике вне его
    window.addEventListener('click', function(event) {
        if (event.target === avatarModal) {
            avatarModal.style.display = 'none';
        }
    });
});