import sys
import random
import numpy as np
from Lib import predict, load_array_from_file,extract_features_from_images

image_path = sys.argv[1]


def main():
    image = extract_features_from_images([image_path]);
    message = "Anime!"
    titties = load_array_from_file('tetas.txt')
    Xtest = np.random.random((55, 768))
    Ytest = np.random.randint(0, 2, size=(55,))
    XX = np.vstack((Xtest, image))        #Using random
    Ran = np.random.randint(0, 2)
    YY = np.append(Ytest, Ran)
    y_hat2 = predict(titties, XX, YY)
    randomVal = y_hat2[-1]
      
    if randomVal == 1:
        message = "Anime!"
    elif randomVal == 2:
        message = "Funko!"
    else:
        message = "Real!"
    return message

if __name__ == "__main__":
    print(main())