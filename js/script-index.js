function validarEAvancar() {
    const input = document.querySelector('.input-group input');
    const valor = input.value.trim();
    const username = valor.startsWith('@') ? valor.slice(1) : valor;

    // Regra do X.com: letras, números e underline, até 15 caracteres
    const regex = /^[A-Za-z0-9_]{1,15}$/;

    if (!regex.test(username)) {
        input.classList.add('is-invalid');
        return;
    }

    input.classList.remove('is-invalid');

    // Redireciona com ?username=
    window.location.href = `menu.html?username=${encodeURIComponent(username)}`;
}