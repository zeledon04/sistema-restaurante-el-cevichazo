// Bar chart --> Ventas por Empleado (Gráfico de Barras)
fetch('/api/productos_mas_vendidos/')
    .then(res => res.json())
    .then(data => {
        console.log(data);

        const bctx = document.getElementById('barChartProductos').getContext("2d");

        // Altura del gráfico, puedes ajustar si necesitas más precisión
        const chartHeight = 400;

        // Generar degradados individuales por barra
        const backgroundColors = data.labels.map(() => {
            const r = Math.floor(Math.random() * 100 + 100); // 100–200
            const g = Math.floor(Math.random() * 100 + 150); // 150–250
            const b = Math.floor(Math.random() * 100 + 200); // 200–300

            const gradient = bctx.createLinearGradient(0, 0, 0, chartHeight);
            gradient.addColorStop(0, `rgba(${r}, ${g}, ${b}, 0.98)`); // Top
            gradient.addColorStop(1, `rgba(${r}, ${g}, ${b}, 0.1)`); // Bottom
            return gradient;
        });

        new Chart(bctx, {
            type: 'bar',
            data: {
                labels: data.labels,
                datasets: [{
                    label: 'Top 10 Productos más vendidos',
                    data: data.datos,
                    backgroundColor: backgroundColors,
                    borderColor: 'rgba(0, 0, 0, 0.1)',
                    borderWidth: 1
                }]
            },
            options: {
                responsive: true,
                scales: { y: { beginAtZero: true } }
            }
        });


    });