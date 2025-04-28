async function inicializarPerfil() {
    const params = new URLSearchParams(window.location.search);
    const username = params.get('username');

    if (!username) {
        alert('Nenhum usuário informado!');
        window.location.href = 'index.html';
        return;
    }

    try {
        const response = await fetch('http://localhost:8000/analyze', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username: username })
        });

        if (!response.ok) {
            throw new Error('Erro ao consultar a API');
        }

        const data = await response.json();

        // Atualizar nome, @ e foto
        document.getElementById('profile-name').textContent = username;
        document.getElementById('profile-username').textContent = `@${username}`;
        document.getElementById('profile-photo').src = data.profile_photo;

        // Definir tipo de fã com base na porcentagem
        let categoria = '';
        if (data.furia_percent >= 75) {
            categoria = "ENGAJADO";
        } else if (data.furia_percent >= 50) {
            categoria = "MODERADO";
        } else if (data.furia_percent >= 25) {
            categoria = "POUCO ENGAJADO";
        } else {
            categoria = "DESENGAJADO";
        }

        // Atualizar o círculo neon dinamicamente
        const furiaPercent = data.furia_percent;
        const circle = document.querySelector('.circle');

        circle.style.background = `conic-gradient(
            #8000ff 0% ${furiaPercent}%,
            #333 ${furiaPercent}% 100%
        )`;

        // Atualizar tipo de fã
        document.getElementById('fan-type').textContent = `${categoria}`;

        // Atualizar indicador circular (pode ser ajustado para sentimento também)
        document.getElementById('main-percentage').innerHTML = `
            ${data.furia_percent}%<br><span>Positivo</span>
        `;

        // Atualizar gráfico de jogos com estilo moderno
        const labels = data.games.map(game => game.label);
        const values = data.games.map(game => game.percent);

        const ctx = document.getElementById('pieChart').getContext('2d');
        new Chart(ctx, {
            type: 'doughnut', // Rosquinha para ficar mais moderno como o círculo que você mostrou
            data: {
                labels: labels,
                datasets: [{
                    data: values,
                    backgroundColor: [
                        '#8000ff', '#00b894', '#0984e3', '#fdcb6e', '#d63031',
                        '#6c5ce7', '#fab1a0', '#e17055', '#00cec9', '#ffeaa7'
                    ],
                    borderColor: '#1e1e1e', // Borda escura para dar "peso"
                    borderWidth: 4, // Deixa bem nítido e "recortado"
                    hoverOffset: 15
                }]
            },
            options: {
                responsive: true,
                cutout: '65%', // Espaço interno para parecer com o círculo neon
                plugins: {
                    legend: {
                        position: 'bottom',
                        labels: {
                            color: '#fff', // Letras brancas
                            font: {
                                size: 14,
                                weight: 'bold'
                            },
                            boxWidth: 20,
                            padding: 15
                        }
                    },
                    tooltip: {
                        backgroundColor: '#1e1e1e',
                        titleColor: '#fff',
                        bodyColor: '#ccc',
                        borderColor: '#8000ff',
                        borderWidth: 1,
                        callbacks: {
                            label: function(context) {
                                const label = context.label || '';
                                const value = context.parsed;
                                return `${label}: ${value}%`;
                            }
                        }
                    }
                },
                layout: {
                    padding: 20
                },
                animation: {
                    animateRotate: true,
                    duration: 1500,
                    easing: 'easeOutBounce'
                }
            }
        });

    } catch (error) {
        console.error(error);
        alert('Erro ao carregar dados do perfil.');
    }
}

window.onload = inicializarPerfil;