# Allowable libraries:
# - Python 3.10.12
# - Pillow 10.0.0
# - numpy 1.25.2
# - OpenCV 4.6.0 (with opencv-contrib-python-headless 4.6.0.66)

# To activate image processing, uncomment the following imports:
from PIL import Image
import numpy as np


# import cv2

class Agent:
    def __init__(self):
        """
        The default constructor for your Agent. Make sure to execute any processing necessary before your Agent starts
        solving problems here. Do not add any variables to this signature; they will not be used by main().

        This init method is only called once when the Agent is instantiated
        while the Solve method will be called multiple times.
        """
        pass

    def _compare_images(self, img1, img2):
        """
        Compare two images and return a score representing their similarity.

        Args:
            img1, img2: PIL Image objects.

        Returns:
            float: A similarity score (the lower, the more similar).
        """
        # Convert images to grayscale
        img1 = img1.convert("L")
        img2 = img2.convert("L")

        # Convert images to numpy arrays for easier manipulation
        arr1 = np.array(img1)
        arr2 = np.array(img2)

        # Calculate the difference and sum it to get a score
        diff = np.sum(np.abs(arr1 - arr2))

        return diff

    def Solve(self, problem):
        """
        Primary method for solving incoming Raven's Progressive Matrices.

        Args:
            problem: The RavensProblem instance.

        Returns:
            int: The answer (1-6).
        """
        # Load the first three figures
        image_a = Image.open(problem.figures["A"].visualFilename)
        image_b = Image.open(problem.figures["B"].visualFilename)
        image_c = Image.open(problem.figures["C"].visualFilename)

        # Calculate the transformation score from A to B
        ab_score = self._compare_images(image_a, image_b)

        # Initialize the best score and answer
        best_score = float('inf')
        answer = -1

        # Compare C with each option and choose the one with the most similar transformation to A to B
        for i in range(1, 7):
            option_image = Image.open(problem.figures[str(i)].visualFilename)
            score = self._compare_images(image_c, option_image)

            # Calculate the score difference using a larger data type to avoid overflow
            score_difference = np.abs(np.int64(score) - np.int64(ab_score))

            # Check if the transformation is similar to A to B
            if score_difference < best_score:
                best_score = score_difference
                answer = i

            if best_score == 0:
                break

        return answer