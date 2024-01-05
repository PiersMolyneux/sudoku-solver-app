import torch
import torchvision
import torchvision.transforms as transforms
from torch.utils.data import DataLoader, random_split
from torch.optim.lr_scheduler import ReduceLROnPlateau
import torch.optim as optim
from model import sudokuCNN


def main():
    # Configuration
    BATCH_SIZE = 4
    NUM_EPOCHS = 30
    TRAIN_SPLIT = 0.9

    # Transform to convert images to PyTorch tensors and normalize them
    transform = transforms.Compose([transforms.ToTensor(), transforms.Normalize((0.5,), (0.5,))])

    # Load and preprocess the MNIST dataset
    trainset_full = torchvision.datasets.MNIST(root='./data', train=True, download=True, transform=transform)
    testset_full = torchvision.datasets.MNIST(root='./data', train=False, download=True, transform=transform)

    # Filter out digit 0 and adjust labels to remove 
    # Adjust the labels to 0-8, as this is what our model expects
    trainset = [(img, label-1) for img, label in trainset_full if label != 0]
    testset = [(img, label-1) for img, label in testset_full if label != 0]

    # Split dataset into training and validation sets
    train_size = int(TRAIN_SPLIT * len(trainset))
    val_size = len(trainset) - train_size
    train_dataset, val_dataset = random_split(trainset, [train_size, val_size])

    # Data loaders for training, validation, and test sets, drop_last=True due to error arising from batch normalization of last data val
    trainloader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True, num_workers=2, drop_last=True)
    valloader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False, num_workers=2, drop_last=True)
    testloader = DataLoader(testset, batch_size=BATCH_SIZE, shuffle=False, num_workers=2, drop_last=True)

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
