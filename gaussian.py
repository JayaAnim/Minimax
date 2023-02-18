import numpy as np

def genGaussianBoard(length, sigma=1):
    # Create coordinate grid for the given length
    x, y = np.meshgrid(np.arange(length), np.arange(length))

    # Calculate the center point of the board
    center = (length-1) / 2

    # Calculate the Gaussian distribution
    guassian_board = np.exp(-((x-center)**2 + (y-center)**2) / (2*sigma**2))

    # Normalize the values so they sum to 1
    guassian_board /= np.sum(guassian_board)
    return guassian_board