document.getElementById('video-form').onsubmit = function(event) {
    event.preventDefault();
    const formData = new FormData(this);

    const fileInput = document.getElementById('video-file');
    const file = fileInput.files[0];

    if (!file) {
        alert('Por favor, selecciona un video.');
        return;
    }

    fetch('/procesar', {
        method: 'POST',
        body: formData
    }).then(response => response.json())
      .then(data => {
          if (data.error) {
              alert(data.error);
          } else {
              window.location.href = '/resultados';
          }
      })
      .catch(error => {
          alert('Ocurrió un error procesando el video. Intenta de nuevo.');
          console.error(error);
      });
};
