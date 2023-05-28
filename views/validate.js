function validateForm() {
    var fileInput = document.getElementById('image-upload');
    var errorMessage = document.getElementById('error-message');
    if (fileInput.files.length === 0) {
      errorMessage.textContent = 'You need to upload an image first! monky.';
      return false;
    }
    errorMessage.textContent = ''; // Limpiar el mensaje de error si existe
    return true;
  }