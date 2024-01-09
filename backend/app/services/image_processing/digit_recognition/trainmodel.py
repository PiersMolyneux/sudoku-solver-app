import torch
import torchvision
import torchvision.transforms as transforms
from torch.utils.data import DataLoader, random_split, ConcatDataset
from torch.optim.lr_scheduler import ReduceLROnPlateau
from torchvision.datasets import ImageFolder, MNIST
import torch.optim as optim
from model import sudokuCNN

def main():
    # Configuration
    BATCH_SIZE = 4
    NUM_EPOCHS = 30
    TRAIN_SPLIT = 0.9
    CUSTOM_DATA_PATH = './digit_recognition_data'  # Custom dataset path

    # Define transformations
    transform = transforms.Compose([
        transforms.Resize((28, 28)),  
        transforms.Grayscale(),       # Convert to grayscale if not already
        transforms.ToTensor(),
        transforms.Normalize((0.5,), (0.5,))  
    ])

    # Load and preprocess the MNIST dataset
    mnist_trainset = MNIST(root='./data', train=True, download=True, transform=transform)
    mnist_testset = MNIST(root='./data', train=False, download=True, transform=transform)

    # Load your custom dataset
    custom_dataset = ImageFolder(root=CUSTOM_DATA_PATH, transform=transform)

    # Combine datasets
    combined_trainset = ConcatDataset([mnist_trainset, custom_dataset])
    test_dataset = mnist_testset  

    # Split combined dataset into training and validation sets
    train_size = int(TRAIN_SPLIT * len(combined_trainset))
    val_size = len(combined_trainset) - train_size
    train_dataset, val_dataset = random_split(combined_trainset, [train_size, val_size])

    train_dataset = [(img, label-1) for img, label in train_dataset if label != 0]
    val_dataset = [(img, label-1) for img, label in val_dataset if label != 0]
    test_dataset = [(img, label-1) for img, label in test_dataset if label != 0]

    # Data loaders for training, validation, and test sets
    trainloader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True, num_workers=2, drop_last=True)
    valloader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False, num_workers=2, drop_last=True)
    testloader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False, num_workers=2, drop_last=True)

    # Model, loss function, optimizer, and learning rate scheduler initialization
    model = sudokuCNN()
    criterion = torch.nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)
    scheduler = ReduceLROnPlateau(optimizer, 'min', factor=0.2, patience=2)

    # Training loop
    for epoch in range(NUM_EPOCHS):
        model.train()
        running_loss = 0.0
        for i, (inputs, labels) in enumerate(trainloader):
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            running_loss += loss.item()

        # Validation phase
        model.eval()
        val_loss = 0.0
        with torch.no_grad():
            for inputs, labels in valloader:
                outputs = model(inputs)
                loss = criterion(outputs, labels)
                val_loss += loss.item()

        val_loss /= len(valloader)
        scheduler.step(val_loss)
        print(f'Epoch {epoch + 1}/{NUM_EPOCHS}, Loss: {running_loss / len(trainloader)}, Val Loss: {val_loss}')

    # Testing phase
    correct = 0
    total = 0
    with torch.no_grad():
        for images, labels in testloader:
            outputs = model(images)
            _, predicted = torch.max(outputs.data, 1)
            total += labels.size(0)
            correct += (predicted == labels).sum().item()

    print(f'Accuracy on test images: {100 * correct / total}%')
    
    # Save only the state dictionary
    torch.save(model.state_dict(), 'sudoku_cnn_state_dict.pth')



# Required if using multiple workers 
if __name__ == '__main__':
    main()
