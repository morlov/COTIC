import torch.nn as nn

class Kernel(nn.Module):
    """
    Simple MLP Kernel, takes x of shape (*, in_channels), returns kernel values of shape (*, in_channels, out_channels)
    """
    def __init__(self, hidden1, hidden2, hidden3, in_channels, out_channels):
        super().__init__()
        self.args = [hidden1, hidden2, hidden3, in_channels, out_channels]

        self.layer_1 = nn.Linear(in_channels, hidden1)
        self.relu_1 = nn.ReLU()
        self.layer_2 = nn.Linear(hidden1, hidden2)
        self.relu_2 = nn.ReLU()
        self.layer_3 = nn.Linear(hidden2, hidden3)
        self.relu_3 = nn.ReLU()
        self.layer_4 = nn.Linear(hidden3, in_channels * out_channels)
        self.in_channels = in_channels
        self.out_channels = out_channels

    def recreate(self, in_channels):
        args = self.args.copy()
        args[3] = in_channels
        return type(self)(*args)

    def forward(self, x):
        shape = list(x.shape)[:-1]
        shape += [self.in_channels, self.out_channels]
        x = self.relu_1(self.layer_1(x))
        x = self.relu_2(self.layer_2(x))
        x = self.relu_3(self.layer_3(x))
        x = self.layer_4(x)
        x = x.reshape(*shape)

        return x


class LinearKernel(nn.Module):
    """
    One layer Kernel, takes x of shape (*, in_channels), returns kernel values of shape (*, in_channels, out_channels)
    """
    def __init__(self, in_channels, out_channels, dropout=0):
        super().__init__()
        self.layer = nn.Linear(in_channels, in_channels * out_channels)
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        shape = list(x.shape)[:-1]
        shape += [self.in_channels, self.out_channels]
        x = self.dropout(self.layer(x))
        x = x.reshape(*shape)

        return x
