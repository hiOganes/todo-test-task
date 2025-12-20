// === КОНФИГУРАЦИЯ ===
const API_BASE = 'http://localhost:8001/api/tasks/';
const API_CREATE = 'http://localhost:8001/api/tasks/create/';
const API_LOGIN = 'http://localhost:8001/api/token/';
const API_REGISTER = 'http://localhost:8001/api/token/register/';
const API_REFRESH = 'http://localhost:8001/api/token/refresh/';

// Храним оба токена
function getAccessToken() {
    return localStorage.getItem('access_token');
}
function getRefreshToken() {
    return localStorage.getItem('refresh_token');
}
function setTokens(access, refresh) {
    localStorage.setItem('access_token', access);
    localStorage.setItem('refresh_token', refresh);
}
function clearTokens() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('refresh_token');
}

// === Проверка аутентификации ===
function checkAuth() {
    const access = getAccessToken();
    const isLoginPage = window.location.pathname.includes('login.html');

    if (!access && !isLoginPage) {
        window.location.href = 'login.html';
    }
    if (access && isLoginPage) {
        window.location.href = '/';
    }
}

// === Регистрация ===
document.getElementById('registerForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('regUsername').value.trim();
    const email = document.getElementById('regEmail').value.trim();
    const password = document.getElementById('regPassword').value;

    const res = await fetch(API_REGISTER, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ username, email, password })
    });

    const errorEl = document.getElementById('regError');
    if (res.ok) {
        errorEl.textContent = 'Регистрация успешна! Теперь войдите.';
        errorEl.style.color = 'green';
        // Можно автоматически заполнить логин
        document.getElementById('loginEmail').value = email;
        openTab('login');
    } else {
        const data = await res.json().catch(() => ({}));
        errorEl.textContent = 'Ошибка: ' + JSON.stringify(data);
        errorEl.style.color = 'red';
    }
});

// === Вход ===
document.getElementById('loginForm')?.addEventListener('submit', async (e) => {
    e.preventDefault();
    const email = document.getElementById('loginEmail').value.trim();
    const password = document.getElementById('loginPassword').value;

    const res = await fetch(API_LOGIN, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email, password })
    });

    const errorEl = document.getElementById('loginError');
    if (res.ok) {
        const data = await res.json();
        setTokens(data.access, data.refresh);
        window.location.href = '/';
    } else {
        const errData = await res.json().catch(() => ({}));
        errorEl.textContent = errData.detail || 'Неверный email или пароль';
        errorEl.style.color = 'red';
    }
});

// === Выход ===
document.getElementById('logoutBtn')?.addEventListener('click', () => {
    clearTokens();
    window.location.href = 'login.html';
});

// === Загрузка задач ===
async function loadTasks() {
    let res = await fetch(API_BASE, {
        headers: { 'Authorization': 'Bearer ' + getAccessToken() }
    });

    // Если access истёк — попробуем обновить
    if (res.status === 401) {
        const refreshed = await refreshToken();
        if (!refreshed) return;
        res = await fetch(API_BASE, {
            headers: { 'Authorization': 'Bearer ' + getAccessToken() }
        });
    }

    if (res.ok) {
        const tasks = await res.json();
        const list = document.getElementById('taskList');
        list.innerHTML = '';
        tasks.forEach(task => {
            const li = document.createElement('li');
            li.className = 'task-item' + (task.status === 'Выполнена' ? ' completed' : '');
            li.innerHTML = `
                <input type="checkbox" class="task-checkbox" ${task.status === 'Выполнена' ? 'checked' : ''} onchange="toggleStatus(${task.id}, this.checked)">
                <div class="task-content">
                    <div class="task-title ${task.status === 'Выполнена' ? 'completed-title' : ''}">${task.title}</div>
                    ${task.description ? `<div class="task-desc">${task.description}</div>` : ''}
                </div>
                <button class="delete-btn" onclick="deleteTask(${task.id})">Удалить</button>
            `;          list.appendChild(li);
        });
    }
}

// === Обновление токена ===
async function refreshToken() {
    const refresh = getRefreshToken();
    if (!refresh) {
        clearTokens();
        window.location.href = 'login.html';
        return false;
    }

    const res = await fetch(API_REFRESH, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh })
    });

    if (res.ok) {
        const data = await res.json();
        localStorage.setItem('access_token', data.access);
        return true;
    } else {
        clearTokens();
        window.location.href = 'login.html';
        return false;
    }
}

// === Создание задачи ===
document.getElementById('addTaskBtn')?.addEventListener('click', async () => {
    const title = document.getElementById('newTitle').value.trim();
    const description = document.getElementById('newDescription').value.trim();
    if (!title) return;

    let res = await fetch(API_CREATE, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + getAccessToken()
        },
        body: JSON.stringify({ title, description: description || null })
    });

    if (res.status === 401) {
        const refreshed = await refreshToken();
        if (!refreshed) return;
        res = await fetch(API_CREATE, { /* повторить запрос */ });
    }

    if (res.ok) {
        document.getElementById('newTitle').value = '';
        document.getElementById('newDescription').value = '';
        loadTasks();
    }
});

// === Смена статуса ===
async function toggleStatus(id, completed) {
    const payload = { status: completed ? 'completed' : 'pending' };

    let res = await fetch(`${API_BASE}${id}/status/`, {
        method: 'PATCH',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer ' + getAccessToken()
        },
        body: JSON.stringify(payload)
    });

    if (res.status === 401) await refreshToken();
    loadTasks();
}

// === Удаление ===
async function deleteTask(id) {
    if (!confirm('Удалить задачу?')) return;

    let res = await fetch(`${API_BASE}${id}/`, {
        method: 'DELETE',
        headers: { 'Authorization': 'Bearer ' + getAccessToken() }
    });

    if (res.status === 401) await refreshToken();
    loadTasks();
}

// === Табы на login.html ===
function openTab(tabName) {
    document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
    document.getElementById(tabName + 'Form').classList.add('active');
    document.querySelector(`[onclick="openTab('${tabName}')"]`).classList.add('active');
}

// === Запуск ===
document.addEventListener('DOMContentLoaded', () => {
    checkAuth();
    if (window.location.pathname.includes('index.html')) {
        loadTasks();
    }
});