document.getElementById('boton-ejecutar').addEventListener('click', async () => {
    try {
        const respuesta = await fetch('http://127.0.0.1:5000/api/ejecutar_funcion', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' }
        });
        const data = await respuesta.json();
        document.getElementById('resultado').textContent = data.mensaje;
    } catch (error) {
        console.error('Error al ejecutar función:', error);
    }
});


// Función para cargar y procesar el archivo CSV
async function cargarCSV(url) {
    const response = await fetch(url);
    const data = await response.text();
    
    // Procesar el CSV: separar filas y columnas
    const filas = data.split('\n').map(fila => fila.split(','));
    const etiquetas = filas[0]; // Primera fila como etiquetas
    const valores = filas.slice(1).map(fila => fila.map(Number));
  
    return { etiquetas, valores };
  }
  
  // Crear el gráfico con Chart.js
  async function crearGrafico() {
    const datos = await cargarCSV('../estadisticas_journal.csv'); // Archivo CSV
    const etiquetas = datos.etiquetas.slice(1); // Evitar la columna de nombre en etiquetas
    const valores = datos.valores.map(fila => fila.slice(1)); // Valores numéricos
    
    // Crear dataset para el gráfico
    const datasets = valores.map((val, index) => ({
      label: datos.valores[index][0], // Nombre de cada fila
      data: val,
      borderColor: `hsl(${index * 30}, 70%, 50%)`,
      backgroundColor: `hsla(${index * 30}, 70%, 50%, 0.4)`,
      fill: false,
    }));
    
    // Configuración de Chart.js
    const ctx = document.getElementById('myChart').getContext('2d');
    new Chart(ctx, {
      type: 'line', // Cambia a 'bar' para un gráfico de barras, etc.
      data: {
        labels: etiquetas,
        datasets: datasets,
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            position: 'top',
          },
          title: {
            display: true,
            text: 'Gráfico desde CSV'
          }
        }
      }
    });
  }
  
  // Llama a la función para crear el gráfico
  crearGrafico();
  