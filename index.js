const express = require('express');
const multer = require('multer');

const app = express();
const upload = multer({ dest: 'uploads/' });
var path = require('path');

app.set('view engine', 'ejs');

app.get('/', (req, res) => {
  res.render('index');
});

app.use(express.static(path.join(__dirname,'views'))); // Leer CSS

app.post('/upload', upload.single('image'), (req, res) => {
  // Verificar si no se seleccionó ninguna imagen
  if (!req.file) {
    res.send('Por favor, selecciona una imagen primero');
    return;
  }

  // Aquí puedes agregar el código para procesar la imagen si lo deseas
    
  // Ejecutar el script de Python como un servicio
  exec('python script.py', (error, stdout, stderr) => {
    if (error) {
      console.error(`Error al ejecutar el script: ${error}`);
      return;
    }
    console.log(`Salida del script: ${stdout}`);
    console.error(`Errores del script: ${stderr}`);
  });

  res.send('Imagen subida y script en ejecución');
});

app.listen(3000, () => {
  console.log('Servidor en funcionamiento en el puerto 3000');
});
