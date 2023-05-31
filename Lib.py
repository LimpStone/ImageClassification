import numpy as np
import cv2 

def flatten_matrix(matrix):
    vector = np.reshape(matrix, -1)
    return vector

def plot_color_histogram(image):
    # Cargar la imagen en modo HSV
    image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Extraer el canal de saturación
    saturation = image_hsv[:, :, 1]

    # Calcular el histograma de saturación
    hist = cv2.calcHist([saturation], [0], None, [256], [0, 256])

    # Normalizar el histograma si es necesario
    hist /= hist.sum()
    return flatten_matrix(hist)   
 
def plot_intensity_histogram(image):
    # Convertir la imagen a escala de grises
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Calcular el histograma de intensidad
    hist = cv2.calcHist([gray_image], [0], None, [256], [0, 256])

    # Normalizar el histograma si es necesario
    hist /= hist.sum()
    return flatten_matrix(hist)

def plot_hog_histogram(image):
    # Calcular el descriptor HOG
    hog = cv2.HOGDescriptor()
    descriptors = hog.compute(image)

    # Calcular el histograma de los descriptores HOG
    hist = cv2.calcHist([descriptors], [0], None, [256], [0, 256])

    # Normalizar el histograma si es necesario
    hist /= hist.sum()
    return flatten_matrix(hist) 

def normalize_vector(vector, method):
    if method == 1:
        # Normalización min-max
        min_val = np.min(vector)
        max_val = np.max(vector)
        normalized_vector = (vector - min_val) / (max_val - min_val)
        return normalized_vector
    elif method == 2:
        # Normalización Z-score
        mean_val = np.mean(vector)
        std_val = np.std(vector)
        normalized_vector = (vector - mean_val) / std_val
        return normalized_vector
    else:
        raise ValueError("El método debe ser 1 para normalización min-max o 2 para normalización Z-score.")
    
def extract_features_from_images(image_paths):
    features = []
    for image_path in image_paths:
        #print(image_path)
        images=cv2.imread(image_path)        
        Vec = plot_color_histogram(images) 
        Vec2 = plot_hog_histogram(images)
        Vec3 = plot_intensity_histogram(images)  
        feature_vector = np.array([normalize_vector(Vec,2), normalize_vector(Vec2,2), normalize_vector(Vec3,2)]).reshape(-1)
        features.append(feature_vector)
    features = np.array(features)
    return features

def load_array_from_file(file_path):
    """
    Lee los valores de un archivo de texto y los carga en un arreglo.

    Args:
        file_path: La ruta del archivo que contiene los datos.

    Returns:
        El arreglo de datos leído desde el archivo.
    """
    data_array = np.loadtxt(file_path)
    return data_array

def predict(theta_list, X, y):
    y_uniq = list(set(y.flatten()))
    y_hat = [0]*len(y)
    for i in range(0, len(y_uniq)):
        y_tr = y_change(y, y_uniq[i])
        # y1 = sigmoid(x, theta_list[i])
        y1 = sigmoid(np.dot(X, theta_list[i]))
        for k in range(0, len(y)):
            if y_tr[k] == 1 and y1[k] >= 0.5:
                y_hat[k] = y_uniq[i]
    return y_hat

def y_change(y, cl):
    """
    Creates an independent y vector that only holds 1's for
    the selected class and zero for the rest
    
    Args:
      y (ndarray (m,)) : target values
      cl (scalar)      : The class we are studying.
      
    Returns:
      y_pr (ndarray (n,))   : Array holding only 1's for the 
                              analyzed class.
    """
    y_pr=[]
    for i in range(0, len(y)):
        if np.array_equal(y[i], cl):
            y_pr.append(1)
        else:
            y_pr.append(0)
    return y_pr

def sigmoid(z):
    """
    Compute the sigmoid of z

    Parameters
    ----------
    z : array_like
        A scalar or numpy array of any size.

    Returns
    -------
     g : array_like
         sigmoid(z)
    """
    z = np.clip(z, -500, 500)           # protect against overflow
    g = 1.0/(1.0+np.exp(-z))

    return g