// Базовый URL API (относительный, т.к. фронтенд и бэкенд на одном домене)
const API_BASE = '/api/v1';

// Утилита для отображения результата
function showResult(element, message, isSuccess) {
    element.textContent = message;
    element.className = `result ${isSuccess ? 'success' : 'error'}`;
    element.style.display = 'block';
}

// Очистка результата
function clearResult(element) {
    element.textContent = '';
    element.style.display = 'none';
}

// Создание пользователя
document.getElementById('createUserForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const resultDiv = document.getElementById('createResult');
    clearResult(resultDiv);

    const adminKey = document.getElementById('adminKey').value;
    const email = document.getElementById('email').value;
    const jobTitle = document.getElementById('jobTitle').value;
    const fullName = document.getElementById('fullName').value;
    const password = document.getElementById('password').value;

    const payload = {
        admin_key: adminKey,
        user_data: {
            email,
            job_title: jobTitle,
            full_name: fullName,
            password
        }
    };

    try {
        const response = await fetch(`${API_BASE}/create_user`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        if (response.ok) {
            showResult(resultDiv, data.message || 'Пользователь успешно создан', true);
            document.getElementById('createUserForm').reset();
        } else {
            showResult(resultDiv, data.detail || 'Ошибка при создании пользователя', false);
        }
    } catch (error) {
        showResult(resultDiv, 'Сетевая ошибка: ' + error.message, false);
    }
});

// Аутентификация с ключом
document.getElementById('authKeyForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const resultDiv = document.getElementById('authResult');
    const userInfoDiv = document.getElementById('userInfo');
    clearResult(resultDiv);
    userInfoDiv.classList.add('hidden');

    const email = document.getElementById('authEmail').value;
    const key = document.getElementById('authKey').value;

    const payload = { email, key };

    try {
        const response = await fetch(`${API_BASE}/auth_with_key`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        if (response.ok) {
            showResult(resultDiv, data.message || 'Успешная аутентификация', true);
            // Заполняем данные пользователя
            document.getElementById('userId').textContent = data.id;
            document.getElementById('userEmail').textContent = data.email;
            document.getElementById('userJobTitle').textContent = data.job_title;
            document.getElementById('userFullName').textContent = data.full_name;
            userInfoDiv.classList.remove('hidden');
            document.getElementById('authKeyForm').reset();
        } else {
            showResult(resultDiv, data.detail || 'Ошибка аутентификации', false);
        }
    } catch (error) {
        showResult(resultDiv, 'Сетевая ошибка: ' + error.message, false);
    }
});

// Первый вход (смена пароля)
document.getElementById('firstLoginForm').addEventListener('submit', async (e) => {
    e.preventDefault();
    const resultDiv = document.getElementById('firstLoginResult');
    clearResult(resultDiv);

    const email = document.getElementById('firstLoginEmail').value;
    const newPassword = document.getElementById('newPassword').value;

    const payload = { email, new_password: newPassword };

    try {
        const response = await fetch(`${API_BASE}/first_login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(payload)
        });

        const data = await response.json();

        if (response.ok) {
            showResult(resultDiv, data.message || 'Пароль успешно изменён', true);
            document.getElementById('firstLoginForm').reset();
        } else {
            showResult(resultDiv, data.detail || 'Ошибка при смене пароля', false);
        }
    } catch (error) {
        showResult(resultDiv, 'Сетевая ошибка: ' + error.message, false);
    }
});