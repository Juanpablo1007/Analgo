// Realiza petición al back endpoint requerimientos 3
document.getElementById('boton-cargar').addEventListener('click', async () => {
  event.preventDefault();
  try {
      const respuesta = await fetch('http://127.0.0.1:5000/api/ejecutar_funcion', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' }
      });
      const data = await respuesta.json();
      console.log(data)
  } catch (error) {
      console.error('Error al ejecutar función:', error);
  }
});

document.addEventListener('DOMContentLoaded', function() {
  // Asocia cada botón a su respectiva sección
  document.getElementById('boton-contexto').addEventListener('click', function() {
    mostrarSeccion('estadisticas');
    actualizarClaseActive('boton-contexto');
  });

  document.getElementById('boton-requerimiento-1').addEventListener('click', function() {
    mostrarSeccion('requerimiento1');
    actualizarClaseActive('boton-requerimiento-1');
  });

  document.getElementById('boton-requerimiento-2').addEventListener('click', async () => {
    try {
      const respuesta = await fetch('http://127.0.0.1:5000/api/requerimientos/2', {
          method: 'GET',
          headers: { 'Content-Type': 'application/json' }
      });
      const data = await respuesta.json();
      document.getElementById('image_afiliaciones_counts').src = `data:image/jpeg;base64,${data.image_afiliaciones_counts}`;
      document.getElementById('image_articulos_citados_counts').src = `data:image/jpeg;base64,${data.image_articulos_citados_counts}`;
      document.getElementById('image_autor_pais_counts').src = `data:image/jpeg;base64,${data.image_autor_pais_counts}`;
      document.getElementById('image_autor_publisher_counts').src = `data:image/jpeg;base64,${data.image_autor_publisher_counts}`;
      document.getElementById('image_autores_citados_counts').src = `data:image/jpeg;base64,${data.image_autores_citados_counts}`;
      document.getElementById('image_base_autor_counts').src = `data:image/jpeg;base64,${data.image_base_autor_counts}`;
      document.getElementById('image_base_datos_counts').src = `data:image/jpeg;base64,${data.image_base_datos_counts}`;
      document.getElementById('image_journal_articulo_counts').src = `data:image/jpeg;base64,${data.image_journal_articulo_counts}`;
      document.getElementById('image_journals_counts').src = `data:image/jpeg;base64,${data.image_journals_counts}`;
      document.getElementById('image_productos_por_tipo_counts').src = `data:image/jpeg;base64,${data.image_productos_por_tipo_counts}`;
      document.getElementById('image_publicaciones_por_año_counts').src = `data:image/jpeg;base64,${data.image_publicaciones_por_año_counts}`;
      document.getElementById('image_publishers_counts').src = `data:image/jpeg;base64,${data.image_publishers_counts}`;
      document.getElementById('image_tipo_producto_año_counts').src = `data:image/jpeg;base64,${data.image_tipo_producto_año_counts}`;

    } catch (error) {
        console.error('Error al ejecutar función:', error);
    }
    mostrarSeccion('requerimiento2');
    actualizarClaseActive('boton-requerimiento-2');
  });

  document.getElementById('boton-requerimiento-3').addEventListener('click', async () => {
    try {
      const respuesta = await fetch('http://127.0.0.1:5000/api/requerimientos/3', {
          method: 'GET',
          headers: { 'Content-Type': 'application/json' }
      });
      const data = await respuesta.json();
      document.getElementById('image_actitudes_counts').src = `data:image/jpeg;base64,${data.image_actitudes_counts}`;
      document.getElementById('image_computacionales_counts').src = `data:image/jpeg;base64,${data.image_computacionales_counts}`;
      document.getElementById('image_investigación_counts').src = `data:image/jpeg;base64,${data.image_investigación_counts}`;
      document.getElementById('image_estrategia_counts').src = `data:image/jpeg;base64,${data.image_estrategia_counts}`;
      document.getElementById('image_habilidades_counts').src = `data:image/jpeg;base64,${data.image_habilidades_counts}`;
      document.getElementById('image_evaluación_counts').src = `data:image/jpeg;base64,${data.image_evaluación_counts}`;
      document.getElementById('image_herramienta_counts').src = `data:image/jpeg;base64,${data.image_herramienta_counts}`;
      document.getElementById('image_medio_counts').src = `data:image/jpeg;base64,${data.image_medio_counts}`;
      document.getElementById('image_escolaridad_counts').src = `data:image/jpeg;base64,${data.image_escolaridad_counts}`;
      document.getElementById('image_psicométricas_counts').src = `data:image/jpeg;base64,${data.image_psicométricas_counts}`;
    } catch (error) {
        console.error('Error al ejecutar función:', error);
    }
    mostrarSeccion('requerimiento3');
    actualizarClaseActive('boton-requerimiento-3');
  });

  document.getElementById('boton-requerimiento-4').addEventListener('click', async () => {
    try {
      const respuesta = await fetch('http://127.0.0.1:5000/api/requerimientos/4', {
          method: 'GET',
          headers: { 'Content-Type': 'application/json' }
      });
      const data = await respuesta.json();
      document.getElementById('image_wordcloud').src = `data:image/jpeg;base64,${data.image_wordcloud}`;
    } catch (error) {
        console.error('Error al ejecutar función:', error);
    }
    mostrarSeccion('requerimiento4');
    actualizarClaseActive('boton-requerimiento-4');
  });

  document.getElementById('boton-requerimiento-5').addEventListener('click', async () => {
    try {
      const respuesta = await fetch('http://127.0.0.1:5000/api/requerimientos/5', {
          method: 'GET',
          headers: { 'Content-Type': 'application/json' }
      });
      const data = await respuesta.json();
      document.getElementById('image_journal_graph').src = `data:image/jpeg;base64,${data.image_journal_graph}`;
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
