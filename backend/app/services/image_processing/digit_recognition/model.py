# Model inspired by this article: https://towardsdatascience.com/going-beyond-99-mnist-handwritten-digits-recognition-cfff96337392

import torch
import torch.nn as nn
import torch.nn.functional as F

class sudokuCNN(nn.Module):
    def __init__(self):
        super(sudokuCNN, self).__init__()

        # Convolutional Layers
        # Layer 1: Convolutional layer with Batch Normalization
        self.conv1 = nn.Conv2d(in_channels=1, out_channels=32, kernel_size=5, stride=1, padding=2)
        self.bn1 = nn.BatchNorm2d(32)
        
        # Layer 2: Convolutional layer with Batch Normalization and Max Pooling
        self.conv2 = nn.Conv2d(in_channels=32, out_channels=32, kernel_size=5, stride=1, padding=2, bias=False)
        self.bn2 = nn.BatchNorm2d(32)
        self.pool1 = nn.MaxPool2d(kernel_size=2, stride=2)
        self.dropout1 = nn.Dropout(0.25)
        
        # Layer 3: Convolutional layer with Batch Normalization
        self.conv3 = nn.Conv2d(in_channels=32, out_channels=64, kernel_size=3, stride=1, padding=1)
        self.bn3 = nn.BatchNorm2d(64)

        # Layer 4: Convolutional layer with Batch Normalization and Max Pooling
        self.conv4 = nn.Conv2d(in_channels=64, out_channels=64, kernel_size=3, stride=1, padding=1, bias=False)
        self.bn4 = nn.BatchNorm2d(64)
        self.pool2 = nn.MaxPool2d(kernel_size=2, stride=2)
        self.dropout2 = nn.Dropout(0.25)

        # Dynamically calculate the input features for the linear layer
        # This ensures compatibility with the input size to the fully connected layer
        with torch.no_grad():
            self._to_linear = None
            self._calculate_to_linear(torch.zeros(1, 1, 28, 28))  # Using a dummy input of size 1x28x28

        # Fully Connected (Dense) Layers
        # Layer 5: First fully connected layer with Batch Normalization
        self.fc1 = nn.Linear(self._to_linear, 256, bias=False)
        self.bn5 = nn.BatchNorm1d(256)
        
        # Layer 6: Second fully connected layer with Batch Normalization
        self.fc2 = nn.Linear(256, 128, bias=False)
        self.bn6 = nn.BatchNorm1d(128)
        
        # Layer 7: Third fully connected layer with Batch Normalization
        self.fc3 = nn.Linear(128, 84, bias=False)
        self.bn7 = nn.BatchNorm1d(84)
        
        # Layer 8: Output layer with 9 units for digits 1-9
        self.fc4 = nn.Linear(84, 9)

    def _calculate_to_linear(self, x):
        # Helper function to pass input through convolutional layers
        # Used to dynamically determine the flattened size for the first dense layer
        x = self.pool2(self.conv4(self.conv3(self.pool1(self.conv2(self.conv1(x))))))
        
        if self._to_linear is None:
            self._to_linear = x[0].shape[0] * x[0].shape[1] * x[0].shape[2]
        
        return x  # Make sure to return the processed tensor



    def forward(self, x):
        # Forward pass through the network

        # Convolutional layers
        x = self._calculate_to_linear(x)

        # Flatten the output for the dense layers
        x = x.view(-1, self._to_linear)
        
        # Fully connected layers
        x = F.relu(self.bn5(self.fc1(x)))
        x = F.relu(self.bn6(self.fc2(x)))
        x = F.relu(self.bn7(self.fc3(x)))
        x = self.dropout2(x)
        
        # Output layer with log softmax activation
        x = F.log_softmax(self.fc4(x), dim=1)
        
        return x