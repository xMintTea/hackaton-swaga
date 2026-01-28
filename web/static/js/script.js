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
        loginForm.addEventListener('submit', async function(e) {
            e.preventDefault();

            const loginField = document.getElementById("loginEmail").value;
            const passwordField = document.getElementById("loginPassword").value;

            const formData = new FormData();
            formData.append('username', loginField);
            formData.append('password', passwordField);

            try {            
                const response = await fetch("/auth/login/", {
                    method: "POST",
                    body: formData
                });

                const data = await response.json();
                
                if (response.ok) {
                    // Успешный вход
                    showNotification('Успех', data.data || 'Вход выполнен успешно', 'success');
                    
                    // Закрываем модальное окно
                    if (loginModal) loginModal.style.display = 'none';
                    
                    // Очищаем форму
                    loginForm.reset();
                    
                    // Сохраняем данные пользователя
                    const userData = {
                        login: loginField,
                        nickname: loginField,
                        avatar: '/static/img/avatars/avatar1.jpg',
                        token: data.access_token || null
                    };
                    
                    // Сохраняем в localStorage через объект auth
                    if (typeof auth !== 'undefined') {
                        auth.login(userData);
                    } else {
                        // Fallback
                        localStorage.setItem('currentUser', JSON.stringify(userData));
                        // Перезагружаем страницу для обновления интерфейса
                        setTimeout(() => location.reload(), 1000);
                    }
                } else {
                    showNotification('Ошибка', data.data || 'Ошибка при входе', 'error');
                }
            } catch (error) {
                console.error('Ошибка при входе:', error);
                showNotification('Ошибка', 'Произошла ошибка при подключении к серверу', 'error');
            }
        });
    }
    
    // Обработка отправки формы регистрации
    if (registerForm) {
        registerForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            // Получаем данные из формы
            const login = document.getElementById('registerLogin').value;
            const email = document.getElementById('registerEmail').value;
            const password = document.getElementById('registerPassword').value;
            
            // Проверяем, открыта ли админская секция
            const adminSection = document.getElementById('adminSection');
            const isAdminSectionVisible = adminSection && adminSection.style.display !== 'none';
            
            let requestBody = {
                login: login,
                nickname: login,
                email: email,
                password: password
            };
            
            // Добавляем данные для админов, если секция видима
            if (isAdminSectionVisible) {
                const secretCode = document.getElementById('secretCode').value;
                const userRole = document.getElementById('userRole').value;
                
                requestBody.secretCode = secretCode;
                requestBody.role = userRole;
            }
            
            try {
                // Отправляем запрос на сервер
                const response = await fetch('/auth/register/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(requestBody)
                });
                
                const data = await response.json();
                
                if (response.ok) {
                    showNotification('Успех', data.data || 'Регистрация прошла успешно', 'success');
                    
                    // Закрываем модальное окно
                    if (registerModal) registerModal.style.display = 'none';
                    
                    // Очищаем форму
                    registerForm.reset();
                    
                    // Автоматически логиним пользователя после регистрации
                    const userData = {
                        login: login,
                        nickname: login,
                        avatar: '/static/img/avatars/avatar1.jpg'
                    };
                    
                    // Сохраняем в localStorage через объект auth
                    if (typeof auth !== 'undefined') {
                        auth.login(userData);
                    } else {
                        // Fallback
                        localStorage.setItem('currentUser', JSON.stringify(userData));
                        // Перезагружаем страницу для обновления интерфейса
                        setTimeout(() => location.reload(), 1000);
                    }
                } else {
                    showNotification('Ошибка', data.data || 'Ошибка при регистрации', 'error');
                }
            } catch (error) {
                console.error('Ошибка при регистрации:', error);
                showNotification('Ошибка', 'Произошла ошибка при подключении к серверу', 'error');
            }
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