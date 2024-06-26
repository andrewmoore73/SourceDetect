import numpy as np

class PrfBuild:
    """Create a training or test set of simulated TESS images containing both 'real' and 'false' sources"""

    def __init__(self,Xtrain,ytrain,run=True):
        """
        Initialise
        ------
        Parameters
        ------
        Xtrain : str
            filename of the true/false TESS prf arrays to be added into the training/test sets  
        ytrain : str
            filename of the labels for the TESS prf arrays to be added into the training/test sets 
            (positive/negative sources can either share a label or have different labels)
        ------
        Options
        ------
        run : bool
            if true (default) then the training/test set will be built upon calling PrfBuild rather 
            than just defining the prfs and corresponding labels 
        """
        self.x_prfs = np.load(Xtrain,allow_pickle=True)
        self.y_prfs =  np.load(ytrain,allow_pickle=True)
        if run==True:
            self.make_data()


    def make_labels(self,X,y,num):
        """Places true/false sources into the training/test array with randomly assigned positions and updates
           the label arrays accordingly (this is called once per training/test image)
        ------
        Parameters
        ------
        X : array
            training/test dataset template with background but no sources 
        y : array
            training/test dataset labels template (np.zeros array)
        num : int
            maximum number of true/false sources in each image
        ------
        Returns
        ------
        positions : list
            list of tuples corresponding to the coordinates of the true/false sources
        """
        positions = []

        for _ in range(num):
            idx = np.random.randint(len(self.x_prfs))
            number = self.x_prfs[idx]
            class_ = int(self.y_prfs[idx])
            px, py = np.random.randint(2,int(self.x_shape[0]-2)), np.random.randint(2,int(self.x_shape[1]-2))
            mx, my = (px+2) // self.grid_size, (py+2) // self.grid_size
            output = y[my][mx]

            if output[0] > 0:
                continue

            output[0] = 1.0
            output[1] = px - (mx * self.grid_size)  # x1
            output[2] = py - (my * self.grid_size)  # y1
            output[3] = 3.0  
            output[4] = 3.0   
            output[5 + class_] = 1.0

            X[py-1:py+2,px-1:px+2] = number*np.max((np.random.rand()*2.5)+0.5)
            if class_ != 2:
                positions.append((py,px))

        return positions
        

    def make_data(self,x_shape=(16,16),y_shape=(4,4),size=64,num=2):
        """Creates the template training/test dataset and label arrays and saves the positions of the real/false sources.
        ------
        Parameters
        ------
        x_shape : tuple (default (16,16))
            shape of the training/test images 
        y_shape : tuple (default (4,4))
            shape of the object position/size/label output 
        size : int (default 64) 
            number of training/test images
        num : int (default 2)
            maximum number of true/false sources in each image
        ------
        Outputs
        ------
        sources : list
            positions (as tuples) of the sources in the image
        X : array
            training/test images
        y : array
            labels corresponding to the training/test images (labels for object position, size, likelihood, and probability of positive/negative/false source)
        """
        self.x_shape = x_shape
        self.y_shape = y_shape
        self.grid_size = int(x_shape[0]/y_shape[0])

        X = np.zeros((size, self.x_shape[0], self.x_shape[1], 1), dtype=np.float32)
        y = np.zeros((size, self.y_shape[0], self.y_shape[1], 8), dtype=np.float32)
        positions = []

        for i in range(size):
            X[i] += np.random.normal(0,np.random.rand()*0.2+0.4,(x_shape[0], x_shape[1], 1))
            positions.append(self.make_labels(X[i],y[i],num=num))
            
        self.sources = sorted(positions)[0]
        self.X = X
        self.y = y