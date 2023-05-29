const express = require('express');
const multer = require('multer');
const { v4: uuidv4 } = require('uuid');
const mime = require('mime-types');
const fs = require('fs');
const app = express();
const upload = multer({ dest: 'uploads/' });
var path = require('path');

app.set('view engine', 'ejs');
app.get('/', (req, res) => { //render inicio
  res.render('index');
});

app.get('/upload', (req, res) => { //render upload
  res.render('upload'); 
});

app.use(express.static(path.join(__dirname,'views'))); // Leer CSS

const { spawn } = require('child_process');
app.post('/upload', upload.single('image'), (req, res) => {
  // Verificar si no se seleccionó ninguna imagen
  if (!req.file) {
    res.send('Por favor, selecciona una imagen primero');
    return;
  }

  // Obtener la extensión de archivo
  const extension = mime.extension(req.file.mimetype);

  // Generar un nombre único para el archivo
  const filename = `${uuidv4()}.${extension}`;

  // Mover el archivo a la carpeta "uploads" con el nombre único y la extensión correspondiente
  const imagePath = path.join(__dirname, 'uploads', filename);
  fs.renameSync(req.file.path, imagePath);

  // Ejecutar el script de Python como un servicio y pasar la ruta de la imagen como argumento
  const pythonProcess = spawn('python', ['script.py', imagePath]);

  let output = ''; // Variable para almacenar la salida del script
  
  pythonProcess.stdout.on('data', (data) => {
    output += data.toString(); // Almacenar la salida del script como texto
  });

  pythonProcess.stderr.on('data', (data) => {
    console.error(`Errores del script: ${data}`);
  });

  pythonProcess.on('close', (code) => {
    console.log(`Proceso de Python finalizado con código de salida ${code}`);
    res.render('upload', { output }); // Enviar la salida del script como respuesta al cliente
  });
});

app.listen(3000, () => {
  console.log('Servidor en funcionamiento en el puerto 3000');
});
