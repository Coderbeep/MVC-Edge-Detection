import cv2
import matplotlib.pyplot as plt
import numpy as np
from scipy.ndimage import gaussian_filter
from skimage.filters import hessian, sato, meijering, prewitt, farid
from skimage.feature import canny
from skimage import filters

def hessian_filter(image, black_ridges=False, sigmas=10):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    hessian_result = hessian(
        image, sigmas=(1, sigmas), black_ridges=black_ridges)

    # Image normalization
    hessian_result = hessian_result - np.min(hessian_result)
    hessian_result = hessian_result / np.max(hessian_result)
    hessian_result = (hessian_result * 255).astype(np.uint8)
    hessian_result = cv2.equalizeHist(hessian_result)
    
    return hessian_result

def sobel_filter(image, kernel_size=3, direction="combined"):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    convolved = None
    match direction:
        case "combined":
            sobel_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=kernel_size)
            sobel_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=kernel_size)

            gradient_magnitude = np.sqrt(sobel_x**2 + sobel_y**2)
            gradient_magnitude = cv2.normalize(
                gradient_magnitude, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U
            )
            convolved = gradient_magnitude

        case "vertical":
            sobel_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=kernel_size)
            sobel_x = cv2.normalize(sobel_x, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
            convolved = sobel_x

        case "horizontal":
            sobel_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=kernel_size)
            sobel_y = cv2.normalize(sobel_y, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
            convolved = sobel_y

    filtered_image = convolved
    return filtered_image

def scharr_filter(image, direction="combined"):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    convolved = None
    match direction:
        case "combined":
            sobel_x = cv2.Scharr(image, cv2.CV_64F, 1, 0)
            sobel_y = cv2.Scharr(image, cv2.CV_64F, 0, 1)

            gradient_magnitude = np.sqrt(sobel_x**2 + sobel_y**2)
            gradient_magnitude = cv2.normalize(
                gradient_magnitude, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U
            )
            convolved = gradient_magnitude

        case "vertical":
            sobel_x = cv2.Scharr(image, cv2.CV_64F, 1, 0)
            sobel_x = cv2.normalize(sobel_x, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
            convolved = sobel_x

        case "horizontal":
            sobel_y = cv2.Scharr(image, cv2.CV_64F, 0, 1)
            sobel_y = cv2.normalize(sobel_y, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U)
            convolved = sobel_y

    filtered_image = convolved
    return filtered_image

def cv_ridge_filter(image, settings):
    cv_filter = cv2.ximgproc.RidgeDetectionFilter_create()  # here are the parameters
    ridges = cv_filter.getRidgeFilteredImage(image)
    return ridges

def canny_edge_detection(image, threshold1, threshold2, sigma=3):
    # If the image is already in grayscale, skip this step
    if image.ndim == 3:
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
    edges = canny(image, sigma=sigma, 
                  low_threshold=threshold1, 
                  high_threshold=threshold2, 
                  use_quantiles=True)
    edges = edges.astype(np.uint8)
    edges *= 255
    return edges

def sato_filter(image, black_ridges=False, sigmas=10):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    sato_result = sato(
        image, sigmas=(1, sigmas), black_ridges=black_ridges)

    # Image normalization
    sato_result = sato_result - np.min(sato_result)
    sato_result = sato_result / np.max(sato_result)
    sato_result = (sato_result * 255).astype(np.uint8)
    sato_result = cv2.equalizeHist(sato_result)
    
    return sato_result

def meijering_filter(image, black_ridges=False, sigmas=10):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    meijering_result = meijering(
        image, sigmas=(1, sigmas), black_ridges=black_ridges)

    # Image normalization
    meijering_result = meijering_result - np.min(meijering_result)
    meijering_result = meijering_result / np.max(meijering_result)
    meijering_result = (meijering_result * 255).astype(np.uint8)
    meijering_result = cv2.equalizeHist(meijering_result)
    
    return meijering_result

def prewitt_filter(image, direction='combined'):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    convolved = None
    match direction:
        case "combined":
            filtered = prewitt(image)
            gradient_magnitude = cv2.normalize(
                filtered, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U
            )
            convolved = gradient_magnitude

        case "vertical":
            filtered = prewitt(image, axis=1)
            gradient_magnitude = cv2.normalize(
                filtered, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U
            )
            convolved = gradient_magnitude

        case "horizontal":
            filtered = prewitt(image, axis=0)
            gradient_magnitude = cv2.normalize(
                filtered, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U
            )
            convolved = gradient_magnitude

    filtered_image = convolved
    return filtered_image

def farid_filter(image, direction='combined'):
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    convolved = None
    match direction:
        case "combined":
            filtered = farid(image)
            gradient_magnitude = cv2.normalize(
                filtered, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U
            )
            convolved = gradient_magnitude

        case "vertical":
            filtered = farid(image, axis=1)
            gradient_magnitude = cv2.normalize(
                filtered, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U
            )
            convolved = gradient_magnitude

        case "horizontal":
            filtered = farid(image, axis=0)
            gradient_magnitude = cv2.normalize(
                filtered, None, 0, 255, cv2.NORM_MINMAX, cv2.CV_8U
            )
            convolved = gradient_magnitude

    filtered_image = convolved
    return filtered_image

if __name__ == '__main__':
    image = cv2.imread('img/messi.jpg', cv2.IMREAD_GRAYSCALE)
    # image1 = canny(image, 3, 0.2, 0.85, use_quantiles=True) # good choice
    
    image1 = canny_edge_detection(image, 0.6, 0.9, 1)
    image2 = canny_edge_detection(image, 0.7, 0.9, 1)
    image3 = canny_edge_detection(image, 0.82, 0.9, 1)
    
    fig, axes = plt.subplots(2, 2, figsize=(8,8))
    
    axes[0,0].imshow(image, cmap='gray')
    axes[0,1].imshow(image1, cmap='gray')
    axes[1,0].imshow(image2, cmap='gray')
    axes[1,1].imshow(image3, cmap='gray')
    
    plt.tight_layout()
    plt.savefig('./transform_testing/canny_test.png', dpi=300)
    plt.show()
    
def display_images_in_grid(images, titles, grid_shape=(2, 2)):
    fig, axes = plt.subplots(grid_shape[0], grid_shape[1], figsize=(8, 8))

    for i, (img, title) in enumerate(zip(images, titles)):
        ax = axes[i // grid_shape[1], i % grid_shape[1]]
        ax.imshow(img, cmap="gray", interpolation="nearest")
        ax.set_title(title)
        ax.axis("off")

    plt.tight_layout()
    plt.savefig("./transform_testing/hessian_test3.png", dpi=300)
    plt.show()

def hessian_scale_space(image, sigmas): 
    max_output = float("-inf")
    max_sigma = None
    max_hessian = None

    for sigma in sigmas:
        # Apply Gaussian filter to the image with the current sigma
        smoothed_image = gaussian_filter(image, sigma=sigma)

        # Compute second derivatives
        f_xx = np.gradient(np.gradient(smoothed_image, axis=0), axis=0)
        f_yy = np.gradient(np.gradient(smoothed_image, axis=1), axis=1)
        f_xy = np.gradient(np.gradient(smoothed_image, axis=0), axis=1)

        # Initialize Hessian matrix for each pixel
        hessian = np.empty((image.shape[0], image.shape[1], 2, 2))

        # Fill the Hessian matrix
        hessian[..., 0, 0] = f_xx
        hessian[..., 0, 1] = f_xy
        hessian[..., 1, 0] = f_xy
        hessian[..., 1, 1] = f_yy

        # Compute eigenvalues of the Hessian
        eigenvalues = np.linalg.eigvalsh(hessian)

        # Get the maximum eigenvalue
        i1 = eigenvalues[..., 0]
        max_i1 = np.max(i1)

        # Check if the current output is greater than the maximum output so far
        if max_i1 > max_output:
            max_output = max_i1
            max_sigma = sigma
            max_hessian = hessian

    # Show the filtered image with the maximum sigma
    plt.imshow(gaussian_filter(image, sigma=max_sigma), cmap="gray")
    plt.title(f"Filtered Image (Sigma = {max_sigma})")
    plt.axis("off")
    plt.show()

    return max_output, max_hessian