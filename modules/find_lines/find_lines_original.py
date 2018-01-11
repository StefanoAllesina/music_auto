import matplotlib
matplotlib.use('TkAgg')
from matplotlib import pyplot as plt
import cv2
import sys
import numpy as np

def find_staves(page, pagenum):
    original = 