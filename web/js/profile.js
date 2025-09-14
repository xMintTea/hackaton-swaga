// Основные функции для работы с профилем
document.addEventListener('DOMContentLoaded', function() {
    // Проверяем авторизацию
    // if (!auth.isLoggedIn()) {
    //     window.location.href = 'index.html';
    //     return;
    // }
    
    // Загружаем данные профиля
    loadProfileData();
    
    // Инициализируем обработчики событий
    initEventHandlers();
});

// Загрузка данных профиля
async function loadProfileData() {
    try {
        const token = auth.getToken();
        const response = await fetch(`${API_BASE_URL}/profile`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        if (response.ok) {
            const profileData = await response.json();
            updateProfileUI(profileData);
        } else {
            console.error('Ошибка загрузки данных профиля');
            // Используем заглушку, если сервер не отвечает
            const profileData = getStubProfileData();
            updateProfileUI(profileData);
        }
    } catch (error) {
        console.error('Ошибка загрузки данных профиля:', error);
        // Используем заглушку при ошибке
        const profileData = getStubProfileData();
        updateProfileUI(profileData);
    }
}

// Заглушка данных профиля
function getStubProfileData() {
    return {
        username: 'Neo_Matrix',
        title: 'Новичок в киберпространстве',
        level: 5,
        xp: 650,
        nextLevelXp: 1000,
        currency: 1250,
        description: 'Изучаю Python и кибербезопасность. Мечтаю стать профессиональным разработчиком.',
        socialLinks: [
            { type: 'youtube', url: 'youtube.com/user/neo_matrix' },
            { type: 'github', url: 'github.com/neo_matrix' }
        ],
        courses: {
            current: [
                { name: 'Python Basics', progress: 65 }
            ],
            completed: []
        },
        achievements: [
            { id: 1, name: 'Первые шаги', description: 'Зарегистрировался на платформе', icon: '⭐' },
            { id: 2, name: 'Начало пути', description: 'Завершил первый модуль курса', icon: '📚' }
        ],
        inventory: {
            avatars: [1],
            frames: [1],
            titles: [1]
        },
        shop: {
            avatars: [
                { id: 1, name: 'Базовый аватар', price: 0, owned: true },
                { id: 2, name: 'Кибер-аватар', price: 500, owned: false },
                { id: 3, name: 'Хакерский аватар', price: 750, owned: false }
            ],
            frames: [
                { id: 1, name: 'Базовая рамка', price: 0, owned: true },
                { id: 2, name: 'Золотая рамка', price: 1200, owned: false }
            ],
            titles: [
                { id: 1, name: 'Новичок в киберпространстве', price: 0, owned: true },
                { id: 2, name: 'Кибер-пионер', price: 800, owned: false }
            ]
        }
    };
}

// Обновление интерфейса профиля
function updateProfileUI(data) {
    // Основная информация
    document.getElementById('username').textContent = data.username;
    document.getElementById('userTitle').textContent = data.title;
    document.getElementById('userLevel').textContent = data.level;
    document.getElementById('currentXP').textContent = data.xp;
    document.getElementById('nextLevelXP').textContent = data.nextLevelXp;
    document.getElementById('userCurrency').textContent = data.currency;
    document.getElementById('shopCurrency').textContent = data.currency;
    
    // Прогресс-бар
    const progressPercentage = (data.xp / data.nextLevelXp) * 100;
    document.getElementById('progressFill').style.width = `${progressPercentage}%`;
    
    // Описание
    document.getElementById('userDescription').textContent = data.description;
    document.getElementById('descriptionInput').value = data.description;
    
    // Социальные ссылки
    updateSocialLinks(data.socialLinks);
    
    // Курсы
    updateCourses(data.courses);
    
    // Достижения
    updateAchievements(data.achievements);
    
    // Магазин
    updateShop(data.shop);
}

// Обновление социальных ссылок
function updateSocialLinks(socialLinks) {
    const socialLinksContainer = document.getElementById('socialLinks');
    socialLinksContainer.innerHTML = '';
    
    socialLinks.forEach(link => {
        const linkElement = document.createElement('div');
        linkElement.className = 'social-link-item';
        
        let icon = '🔗';
        if (link.type === 'youtube') icon = '📺';
        else if (link.type === 'github') icon = '🐙';
        else if (link.type === 'telegram') icon = '📨';
        else if (link.type === 'vk') icon = '👥';
        
        linkElement.innerHTML = `
            <span class="social-icon">${icon}</span>
            <span class="social-url">${link.url}</span>
        `;
        
        socialLinksContainer.appendChild(linkElement);
    });
}

// Обновление курсов
function updateCourses(courses) {
    const currentCoursesContainer = document.getElementById('currentCourses');
    const completedCoursesContainer = document.getElementById('completedCourses');
    
    // Текущие курсы
    currentCoursesContainer.innerHTML = '';
    if (courses.current.length > 0) {
        courses.current.forEach(course => {
            const courseElement = document.createElement('div');
            courseElement.className = 'course-progress-item';
            
            let icon = '📖';
            if (course.name.includes('Python')) icon = '🐍';
            else if (course.name.includes('JavaScript')) icon = '⚡';
            else if (course.name.includes('Java')) icon = '☕';
            
            courseElement.innerHTML = `
                <div class="course-icon">${icon}</div>
                <div class="course-details">
                    <h3>${course.name}</h3>
                    <p>Прогресс: ${course.progress}%</p>
                    <div class="mini-progress-bar">
                        <div class="mini-progress-fill" style="width: ${course.progress}%;"></div>
                    </div>
                </div>
            `;
            
            currentCoursesContainer.appendChild(courseElement);
        });
    } else {
        currentCoursesContainer.innerHTML = '<p>У вас нет активных курсов.</p>';
    }
    
    // Завершенные курсы
    completedCoursesContainer.innerHTML = '';
    if (courses.completed.length > 0) {
        courses.completed.forEach(course => {
            const courseElement = document.createElement('div');
            courseElement.className = 'course-progress-item';
            
            let icon = '📖';
            if (course.name.includes('Python')) icon = '🐍';
            else if (course.name.includes('JavaScript')) icon = '⚡';
            else if (course.name.includes('Java')) icon = '☕';
            
            courseElement.innerHTML = `
                <div class="course-icon">${icon}</div>
                <div class="course-details">
                    <h3>${course.name}</h3>
                    <p>Завершено: 100%</p>
                    <div class="mini-progress-bar">
                        <div class="mini-progress-fill" style="width: 100%;"></div>
                    </div>
                </div>
            `;
            
            completedCoursesContainer.appendChild(courseElement);
        });
    } else {
        completedCoursesContainer.innerHTML = '<p>У вас пока нет завершенных курсов.</p>';
    }
}

// Обновление достижений
function updateAchievements(achievements) {
    const achievementsContainer = document.querySelector('.achievements-grid');
    achievementsContainer.innerHTML = '';
    
    // Показываем только 6 достижений на главной странице профиля
    const displayedAchievements = achievements.slice(0, 6);
    
    displayedAchievements.forEach(achievement => {
        const achievementElement = document.createElement('div');
        achievementElement.className = 'achievement-item';
        
        achievementElement.innerHTML = `
            <div class="achievement-icon">${achievement.icon}</div>
            <div class="achievement-info">
                <h4>${achievement.name}</h4>
                <p>${achievement.description}</p>
            </div>
        `;
        
        achievementsContainer.appendChild(achievementElement);
    });
    
    // Добавляем заблокированные достижения, если нужно
    if (displayedAchievements.length < 6) {
        for (let i = displayedAchievements.length; i < 6; i++) {
            const lockedAchievement = document.createElement('div');
            lockedAchievement.className = 'achievement-item locked';
            
            lockedAchievement.innerHTML = `
                <div class="achievement-icon">🔒</div>
                <div class="achievement-info">
                    <h4>Неизвестное достижение</h4>
                    <p>Продолжайте учиться, чтобы открыть</p>
                </div>
            `;
            
            achievementsContainer.appendChild(lockedAchievement);
        }
    }
}

// Обновление магазина
function updateShop(shop) {
    // Аватары
    const avatarsContainer = document.getElementById('shopAvatars');
    avatarsContainer.innerHTML = '';
    
    shop.avatars.forEach(avatar => {
        const avatarElement = createShopItem(avatar, 'avatar');
        avatarsContainer.appendChild(avatarElement);
    });
    
    // Рамки
    const framesContainer = document.getElementById('shopFrames');
    framesContainer.innerHTML = '';
    
    shop.frames.forEach(frame => {
        const frameElement = createShopItem(frame, 'frame');
        framesContainer.appendChild(frameElement);
    });
    
    // Титулы
    const titlesContainer = document.getElementById('shopTitles');
    titlesContainer.innerHTML = '';
    
    shop.titles.forEach(title => {
        const titleElement = createShopItem(title, 'title');
        titlesContainer.appendChild(titleElement);
    });
}

// Создание элемента магазина
function createShopItem(item, type) {
    const itemElement = document.createElement('div');
    itemElement.className = `shop-item ${item.owned ? 'owned' : ''}`;
    
    let iconHtml = '';
    if (type === 'avatar') {
        iconHtml = `<img src="img/avatars/avatar${item.id}.png" alt="${item.name}">`;
    } else if (type === 'frame') {
        iconHtml = `
            <div class="${item.id === 2 ? 'premium-frame' : 'basic-frame'}">
                <img src="img/avatars/avatar1.png" alt="${item.name}">
            </div>
        `;
    } else {
        iconHtml = '<div class="item-icon">🏷️</div>';
    }
    
    itemElement.innerHTML = `
        <div class="item-icon">
            ${iconHtml}
        </div>
        <div class="item-info">
            <h4>${item.name}</h4>
            ${item.owned ? '<p>Ваш текущий предмет</p>' : `
                <div class="item-price">
                    <span class="currency-icon">ⓒ</span>
                    <span>${item.price}</span>
                </div>
            `}
        </div>
        ${!item.owned ? `<button class="btn btn-small" data-item-id="${item.id}" data-item-type="${type}">Купить</button>` : ''}
    `;
    
    return itemElement;
}

// Инициализация обработчиков событий
function initEventHandlers() {
    // Редактирование описания
    const editDescriptionBtn = document.getElementById('editDescriptionBtn');
    const saveDescriptionBtn = document.getElementById('saveDescriptionBtn');
    const cancelDescriptionBtn = document.getElementById('cancelDescriptionBtn');
    const descriptionForm = document.getElementById('editDescriptionForm');
    const descriptionText = document.getElementById('userDescription');
    
    if (editDescriptionBtn) {
        editDescriptionBtn.addEventListener('click', function() {
            descriptionForm.style.display = 'block';
            descriptionText.style.display = 'none';
            this.style.display = 'none';
        });
    }
    
    if (saveDescriptionBtn) {
        saveDescriptionBtn.addEventListener('click', function() {
            const newDescription = document.getElementById('descriptionInput').value;
            // Здесь будет запрос к API для сохранения описания
            descriptionText.textContent = newDescription;
            descriptionForm.style.display = 'none';
            descriptionText.style.display = 'block';
            editDescriptionBtn.style.display = 'block';
            
            // Временное уведомление
            showNotification('Описание успешно сохранено', 'success');
        });
    }
    
    if (cancelDescriptionBtn) {
        cancelDescriptionBtn.addEventListener('click', function() {
            descriptionForm.style.display = 'none';
            descriptionText.style.display = 'block';
            editDescriptionBtn.style.display = 'block';
        });
    }
    
    // Редактирование социальных ссылок
    const editSocialsBtn = document.getElementById('editSocialsBtn');
    const saveSocialsBtn = document.getElementById('saveSocialsBtn');
    const cancelSocialsBtn = document.getElementById('cancelSocialsBtn');
    const socialsForm = document.getElementById('editSocialsForm');
    const socialsList = document.getElementById('socialLinks');
    const addSocialBtn = document.getElementById('addSocialBtn');
    
    if (editSocialsBtn) {
        editSocialsBtn.addEventListener('click', function() {
            socialsForm.style.display = 'block';
            socialsList.style.display = 'none';
            this.style.display = 'none';
        });
    }
    
    if (addSocialBtn) {
        addSocialBtn.addEventListener('click', function() {
            const type = document.getElementById('socialTypeSelect').value;
            const url = document.getElementById('socialUrlInput').value;
            
            if (url) {
                // Здесь будет логика добавления социальной ссылки
                const newLink = document.createElement('div');
                newLink.className = 'social-link-item';
                
                let icon = '🔗';
                if (type === 'youtube') icon = '📺';
                else if (type === 'github') icon = '🐙';
                else if (type === 'telegram') icon = '📨';
                else if (type === 'vk') icon = '👥';
                
                newLink.innerHTML = `
                    <span class="social-icon">${icon}</span>
                    <span class="social-url">${url}</span>
                `;
                
                socialsList.appendChild(newLink);
                document.getElementById('socialUrlInput').value = '';
                
                showNotification('Ссылка добавлена', 'success');
            }
        });
    }
    
    if (saveSocialsBtn) {
        saveSocialsBtn.addEventListener('click', function() {
            // Здесь будет запрос к API для сохранения социальных ссылок
            socialsForm.style.display = 'none';
            socialsList.style.display = 'block';
            editSocialsBtn.style.display = 'block';
            
            showNotification('Социальные ссылки сохранены', 'success');
        });
    }
    
    if (cancelSocialsBtn) {
        cancelSocialsBtn.addEventListener('click', function() {
            socialsForm.style.display = 'none';
            socialsList.style.display = 'block';
            editSocialsBtn.style.display = 'block';
        });
    }
    
    // Переключение вкладок
    const tabBtns = document.querySelectorAll('.tab-btn');
    tabBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const tabName = this.getAttribute('data-tab');
            const tabContainer = this.closest('.profile-section');
            
            // Убираем активный класс у всех кнопок в этом контейнере
            tabContainer.querySelectorAll('.tab-btn').forEach(b => {
                b.classList.remove('active');
            });
            
            // Добавляем активный класс нажатой кнопке
            this.classList.add('active');
            
            // Скрываем все вкладки и показываем нужную
            tabContainer.querySelectorAll('.tab-content').forEach(content => {
                content.classList.remove('active');
            });
            
            tabContainer.querySelector(`#${this.getAttribute('data-tab') === 'current' ? 'currentCourses' : 
                                       this.getAttribute('data-tab') === 'completed' ? 'completedCourses' :
                                       `shop${this.getAttribute('data-tab').charAt(0).toUpperCase() + this.getAttribute('data-tab').slice(1)}`}`).classList.add('active');
        });
    });
    
    // Выбор аватара
    const changeAvatarBtn = document.getElementById('changeAvatarBtn');
    const avatarModal = document.getElementById('avatarModal');
    const closeAvatarModal = document.getElementById('closeAvatarModal');
    const confirmAvatarBtn = document.getElementById('confirmAvatarBtn');
    
    if (changeAvatarBtn) {
        changeAvatarBtn.addEventListener('click', function() {
            avatarModal.style.display = 'flex';
        });
    }
    
    if (closeAvatarModal) {
        closeAvatarModal.addEventListener('click', function() {
            avatarModal.style.display = 'none';
        });
    }
    
    if (confirmAvatarBtn) {
        confirmAvatarBtn.addEventListener('click', function() {
            const selectedAvatar = document.querySelector('.avatar-option.selected');
            if (selectedAvatar && !selectedAvatar.classList.contains('locked')) {
                // Здесь будет запрос к API для сменя аватара
                const avatarImg = selectedAvatar.querySelector('img').src;
                document.getElementById('userAvatar').src = avatarImg;
                avatarModal.style.display = 'none';
                
                showNotification('Аватар успешно изменен', 'success');
            } else {
                showNotification('Этот аватар заблокирован', 'error');
            }
        });
    }
    
    // Выбор элементов в модальном окне аватара
    const avatarOptions = document.querySelectorAll('.avatar-option');
    avatarOptions.forEach(option => {
        option.addEventListener('click', function() {
            if (!this.classList.contains('locked')) {
                avatarOptions.forEach(o => o.classList.remove('selected'));
                this.classList.add('selected');
            }
        });
    });
    
    // Покупка предметов в магазине
    document.addEventListener('click', function(e) {
        if (e.target.classList.contains('btn-small') && e.target.textContent === 'Купить') {
            const itemId = e.target.getAttribute('data-item-id');
            const itemType = e.target.getAttribute('data-item-type');
            
            // Здесь будет запрос к API для покупки предмета
            showNotification(`Предмет приобретен!`, 'success');
            
            // Обновляем интерфейс
            e.target.textContent = 'Приобретено';
            e.target.disabled = true;
            e.target.closest('.shop-item').classList.add('owned');
        }
    });
    
    // Настройки приватности
    const visibilityToggle = document.getElementById('profileVisibilityToggle');
    if (visibilityToggle) {
        visibilityToggle.addEventListener('change', function() {
            // Здесь будет запрос к API для изменения настроек приватности
            showNotification(`Профиль ${this.checked ? 'скрыт' : 'открыт'}`, 'success');
        });
    }
    
    // Открытие модального окна достижений
    const viewAllAchievementsBtn = document.querySelector('[data-translate="view_all"]');
    if (viewAllAchievementsBtn) {
        viewAllAchievementsBtn.addEventListener('click', openAchievementsModal);
    }
}

// Функция для открытия модального окна достижений
function openAchievementsModal() {
    const modal = document.getElementById('achievementsModal');
    modal.style.display = 'flex';
    loadAllAchievements();
}

// Функция для загрузки всех достижений
async function loadAllAchievements() {
    try {
        const token = auth.getToken();
        const response = await fetch(`${API_BASE_URL}/achievements`, {
            headers: {
                'Authorization': `Bearer ${token}`
            }
        });
        
        let achievements = [];
        
        if (response.ok) {
            achievements = await response.json();
        } else {
            // Используем заглушку, если сервер не отвечает
            achievements = [
                { id: 1, name: "Первые шаги", description: "Зарегистрировался на платформе", icon: "⭐", earned: true, date: "15.04.2025" },
                { id: 2, name: "Начало пути", description: "Завершил первый модуль курса", icon: "📚", earned: true, date: "18.04.2025" },
                { id: 3, name: "Неделя активности", description: "Заходил на платформу 7 дней подряд", icon: "🔥", earned: false, progress: "5/7 дней" },
                { id: 4, name: "Мастер Python", description: "Завершил курс Python Basics", icon: "🐍", earned: false, progress: "65%" },
                { id: 5, name: "Социальная активность", description: "Добавил 3 социальные ссылки в профиль", icon: "👥", earned: false, progress: "2/3 ссылок" },
                { id: 6, name: "Коллекционер", description: "Приобрел 5 предметов в магазине", icon: "🛍️", earned: false, progress: "1/5 предметов" },
                { id: 7, name: "Эксперт JavaScript", description: "Завершил курс JavaScript Fundamentals", icon: "⚡", earned: false },
                { id: 8, name: "Кибер-легенда", description: "Достиг 10 уровня", icon: "🏆", earned: false }
            ];
        }
        
        const container = document.getElementById('allAchievements');
        container.innerHTML = '';
        
        achievements.forEach(achievement => {
            const achievementElement = document.createElement('div');
            achievementElement.className = `achievement-item ${achievement.earned ? '' : 'locked'}`;
            
            achievementElement.innerHTML = `
                <div class="achievement-icon">${achievement.icon}</div>
                <div class="achievement-info">
                    <h4>${achievement.name}</h4>
                    <p>${achievement.description}</p>
                    ${achievement.earned ? 
                        `<div class="achievement-date">Получено: ${achievement.date}</div>` : 
                        achievement.progress ? 
                            `<div class="achievement-progress">Прогресс: ${achievement.progress}</div>` :
                            `<div class="achievement-progress">Еще не получено</div>`
                    }
                </div>
            `;
            
            container.appendChild(achievementElement);
        });
    } catch (error) {
        console.error('Ошибка загрузки достижений:', error);
    }
}

// Вспомогательная функция для показа уведомлений
function showNotification(message, type) {
    // Создаем элемент уведомления
    const notification = document.createElement('div');
    notification.className = `notification ${type}`;
    notification.textContent = message;
    
    // Стилизуем уведомление
    notification.style.position = 'fixed';
    notification.style.top = '20px';
    notification.style.right = '20px';
    notification.style.padding = '10px 20px';
    notification.style.borderRadius = '5px';
    notification.style.color = '#fff';
    notification.style.zIndex = '10000';
    notification.style.opacity = '0';
    notification.style.transition = 'opacity 0.3s ease';
    
    if (type === 'success') {
        notification.style.background = 'var(--neon-green)';
        notification.style.boxShadow = '0 0 10px var(--neon-green)';
    } else {
        notification.style.background = 'var(--neon-pink)';
        notification.style.boxShadow = '0 0 10px var(--neon-pink)';
    }
    
    // Добавляем уведомление на страницу
    document.body.appendChild(notification);
    
    // Показываем уведомление
    setTimeout(() => {
        notification.style.opacity = '1';
    }, 10);
    
    // Убираем уведомление через 3 секунды
    setTimeout(() => {
        notification.style.opacity = '0';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}