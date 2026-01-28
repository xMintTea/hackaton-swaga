// templateLoader.js
// Функция для загрузки и вставки шаблонов
async function loadTemplates() {
    try {
        // Загрузка header
        const headerResponse = await fetch('/static/templates/header.html');
        const headerHTML = await headerResponse.text();
        document.getElementById('header-placeholder').outerHTML = headerHTML;
        
        // Загрузка footer
        const footerResponse = await fetch('/static/templates/footer.html');
        const footerHTML = await footerResponse.text();
        document.getElementById('footer-placeholder').outerHTML = footerHTML;
        
        // Обновляем UI в зависимости от состояния авторизации
        setTimeout(() => {
            if (typeof auth !== 'undefined') {
                auth.updateUI();
            } else {
                console.warn('Объект auth не определен, проверьте порядок загрузки скриптов');
            }
        }, 100);
        
        // Инициализация скриптов после загрузки шаблонов
        initScripts();
    } catch (error) {
        console.error('Ошибка загрузки шаблонов:', error);
    }
}

// Инициализация скриптов после загрузки DOM и шаблонов
function initScripts() {
    // Инициализация основных скриптов
    if (typeof initMatrixRain !== 'undefined') initMatrixRain();
    if (typeof initAnimations !== 'undefined') initAnimations();
    if (typeof initNavigation !== 'undefined') initNavigation();
    if (typeof initModals !== 'undefined') initModals();
    if (typeof initForms !== 'undefined') initForms();
    if (typeof initScrollEffects !== 'undefined') initScrollEffects();
    if (typeof initAdminToggle !== 'undefined') initAdminToggle();
}

// Загрузка шаблонов при загрузке DOM
document.addEventListener('DOMContentLoaded', loadTemplates);