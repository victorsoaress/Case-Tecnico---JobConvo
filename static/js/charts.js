document.addEventListener('DOMContentLoaded', function() {
    const ctxVagas = document.getElementById('vagasCriadasChart').getContext('2d');
    const ctxCandidatos = document.getElementById('candidatosRecebidosChart').getContext('2d');

    // Fetch data and create charts
    fetch('/empresa/api/vagas_criadas_por_mes/')
        .then(response => response.json())
        .then(data => {
            const labels = Object.keys(data);
            const values = Object.values(data);
            const maxValue = Math.max(...values);
            const suggestedMax = maxValue + (maxValue*0.5)

            new Chart(ctxVagas, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Vagas Criadas por Mês',
                        data: values,
                        backgroundColor: 'rgba(54, 162, 235, 0.2)',
                        borderColor: 'rgba(54, 162, 235, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true,
                            suggestedMax: suggestedMax,
                            ticks:{
                                stepSize:1
                            }
                        }
                    },
                }
            });
        });

    fetch('/empresa/api/candidatos_recebidos_por_mes/')
        .then(response => response.json())
        .then(data => {
            const labels = Object.keys(data);
            const values = Object.values(data);
            const maxValue = Math.max(...values);
            const suggestedMax = maxValue + (maxValue*0.5)

            new Chart(ctxCandidatos, {
                type: 'bar',
                data: {
                    labels: labels,
                    datasets: [{
                        label: 'Candidatos Recebidos por Mês',
                        data: values,
                        backgroundColor: 'rgba(255, 99, 132, 0.2)',
                        borderColor: 'rgba(255, 99, 132, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true,
                            suggestedMax: suggestedMax,
                            ticks:{
                                stepSize:1
                            }
                        }
                    }
                }
            });
        });
});
