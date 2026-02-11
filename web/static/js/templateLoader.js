// templateLoader3.js - Исправленная версия
async function loadTemplates() {
    try {
        console.log('Начало загрузки шаблонов...');
        
        // Загрузка header
        const headerResponse = await fetch('/static/templates/header.html');
        const headerHTML = await headerResponse.text();
        document.getElementById('header-placeholder').outerHTML = headerHTML;
        
        // Загрузка footer
        const footerResponse = await fetch('/static/templates/footer.html');
        const footerHTML = await footerResponse.text();
        document.getElementById('footer-placeholder').outerHTML = footerHTML;
        
        console.log('Шаблоны загружены, инициализация скриптов...');
        
        // Обновляем UI в зависимости от состояния авторизации
        setTimeout(() => {
            if (typeof auth !== 'undefined') {
                auth.updateUI();
            } else {
                console.warn('Объект auth не определен');
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
    console.log('Инициализация всех скриптов...');
    
    // Инициализация основных скриптов
    if (typeof initMatrixRain !== 'undefined') initMatrixRain();
    if (typeof initAnimations !== 'undefined') initAnimations();
    if (typeof initNavigation !== 'undefined') initNavigation();
    if (typeof initScrollEffects !== 'undefined') initScrollEffects();
    
    // Инициализация модальных окон (ВАЖНО!)
    if (typeof initModals !== 'undefined') {
        console.log('Инициализация модальных окон...');
        initModals();
    } else {
        console.error('Функция initModals не определена!');
    }
    
    // Инициализация форм авторизации
    if (typeof initForms !== 'undefined') initForms();
    if (typeof initAdminToggle !== 'undefined') initAdminToggle();
}

// Загрузка шаблонов при загрузке DOM
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', loadTemplates);
} else {
    // DOM уже загружен
    loadTemplates();
}

// Экспортируем функцию для ручного вызова при необходимости
window.loadTemplates = loadTemplates;
window.initScripts = initScripts;