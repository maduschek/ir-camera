import os
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
from pathlib import Path


# run the irb2txt.exe and load the resulting txt file here:
'''
data = np.genfromtxt("AA060500.txt", delimiter='    ', dtype=float)
data_img = np.reshape(data[:,3], [384,288])
img = Image.fromarray(data_img)
img.save("out.png")
'''


def read_txt_file(file_path):
    try:
        data = np.genfromtxt(file_path, delimiter='    ', dtype=float)
        data_img = np.reshape(data[:, 3], [288, 384])
        data_img -= np.min(data_img)
        data_img /= np.max(data_img) / 255
        # plt.imshow(data_img, cmap='magma')
        # plt.show()
        img = Image.fromarray(data_img.astype(int))
        img = img.convert("RGB")
        img.save(file_path[:-4] + ".png")
        return data_img

    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None


def find_and_read_txt_files(root_folder):
    txt_files = []

    for foldername, subfolders, filenames in os.walk(root_folder):
        for filename in filenames:
            if filename.endswith(".irb"):
                file_path = os.path.join(foldername, filename)
                source_path = Path(__file__).resolve()
                if not os.path.isfile(file_path[:-4] + ".txt"):
                    os.system(os.path.dirname(source_path) + "/irb2txt/irb2txt.exe " + file_path)
                data = read_txt_file(file_path[:-4] + ".txt")
                if data is not None:
                    txt_files.append(data)

    return txt_files



if __name__ == "__main__":
    folder_path = "C:/TEMP/IRB_Images/"  # Replace with the path to your root folder
    txt_data_list = find_and_read_txt_files(folder_path)