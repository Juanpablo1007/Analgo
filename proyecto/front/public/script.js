document.addEventListener('DOMContentLoaded', function() {
  // Botón para el contexto
  document.getElementById('boton-contexto').addEventListener('click', function() {
    mostrarSeccion('estadisticas');
    actualizarClaseActive('boton-contexto');
  });

  
  function descargarArchivo() {
    // Cambia la ruta por la ubicación real en tu servidor
    const rutaArchivo = 'resultados/Requerimiento_1/unified_database.csv';

    // Crear un enlace y simular la descarga
    const enlace = document.createElement('a');
    enlace.href = rutaArchivo;
    enlace.download = 'unified_database.csv'; // Nombre del archivo para descargar
    enlace.click();
}


  // Botón para Requerimiento 1
  document.getElementById('boton-requerimiento-1').addEventListener('click', function() {
    mostrarSeccion('requerimiento1');
    actualizarClaseActive('boton-requerimiento-1');
  });

  // Botón para Requerimiento 2
  document.getElementById('boton-requerimiento-2').addEventListener('click', async () => {
    try {
      const respuesta = await fetch('http://127.0.0.1:5000/api/requerimientos/2', {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
      });
      const data = await respuesta.json();
      console.log(data);
    } catch (error) {
      console.error('Error al ejecutar función:', error);
    }
    mostrarSeccion('requerimiento2');
    actualizarClaseActive('boton-requerimiento-2');
  });

  // Botón para Requerimiento 3
  document.getElementById('boton-requerimiento-3').addEventListener('click', async () => {
    try {
      const respuesta = await fetch('http://127.0.0.1:5000/api/requerimientos/3', {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
      });
      const data = await respuesta.json();
      console.log(data);
    } catch (error) {
      console.error('Error al ejecutar función:', error);
    }
    mostrarSeccion('requerimiento3');
    actualizarClaseActive('boton-requerimiento-3');
  });

  // Botón para Requerimiento 4
  document.getElementById('boton-requerimiento-4').addEventListener('click', async () => {
    try {
      const respuesta = await fetch('http://127.0.0.1:5000/api/requerimientos/4', {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
      });
      const data = await respuesta.json();
      console.log(data);
    } catch (error) {
      console.error('Error al ejecutar función:', error);
    }
    mostrarSeccion('requerimiento4');
    actualizarClaseActive('boton-requerimiento-4');
  });

  // Botón para Requerimiento 5
  document.getElementById('boton-requerimiento-5').addEventListener('click', async () => {
    try {
      const respuesta = await fetch('http://127.0.0.1:5000/api/requerimientos/5', {
        method: 'GET',
        headers: { 'Content-Type': 'application/json' }
      });
      const data = await respuesta.json();
      console.log(data);
    } catch (error) {
      console.error('Error al ejecutar función:', error);
    }
    mostrarSeccion('requerimiento5');
    actualizarClaseActive('boton-requerimiento-5');
  });
});

// Función para mostrar una sección específica
function mostrarSeccion(seccionId) {
  // Oculta todas las secciones
  const secciones = document.querySelectorAll('section');
  secciones.forEach(seccion => seccion.style.display = 'none');

  // Muestra la sección seleccionada
  const seccion = document.getElementById(seccionId);
  if (seccion) {
    seccion.style.display = 'block';
  }
}

// Función para actualizar la clase 'active' en el botón clickeado
function actualizarClaseActive(idBoton) {
  // Elimina la clase 'active' de todos los botones
  const botones = document.querySelectorAll('.nav-link');
  botones.forEach(boton => boton.classList.remove('active'));

  // Agrega la clase 'active' al botón clickeado
  document.getElementById(idBoton).classList.add('active');
}
