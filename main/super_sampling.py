import os
import time
import torch
from PIL import Image
import numpy as np
from RealESRGAN import RealESRGAN

DEFAULT_EXTENSION = '.png'
IMAGES_DIR_PATH = ''
OUTPUT_PATH = ''
IMAGE_SCALE = 2

def get_pictures_from_dir(dir_path, extension):
    return [f for f in os.listdir(dir_path) if os.path.isfile(os.path.join(dir_path, f)) and f.lower().endswith(extension.lower())]

def is_picture_already_sampled(picture, output_dir, extension):
    return picture in get_pictures_from_dir(output_dir, extension)

# Main
def super_sample_images_in_directory(input_directory, output_directory):
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = RealESRGAN(device, scale=IMAGE_SCALE)
    model.load_weights(f'weights/RealESRGAN_x{str(IMAGE_SCALE)}.pth', download=True)

    os.makedirs(output_directory, exist_ok=True)
    for picture in get_pictures_from_dir(input_directory, DEFAULT_EXTENSION):
        path_to_image = f'{input_directory}/{picture}'
        
        if not is_picture_already_sampled(picture, output_directory, DEFAULT_EXTENSION):
            image = Image.open(path_to_image).convert('RGB')

            start = time.time()
            print(f'Sampling image [{path_to_image}]')

            sr_image = model.predict(image)
            save_to = f'{output_directory}/{picture}'
            sr_image.save(save_to)
            
            print(f'Sampling finished with time: [{str(time.time() - start)}].')


def benchmark_results():
    benchmark_output_path = './benchmark/benchmark_output/new'
    benchmark_input_path = './benchmark/benchmark_input'
    
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    model = RealESRGAN(device, scale=IMAGE_SCALE)
    model.load_weights(f'weights/RealESRGAN_x{str(IMAGE_SCALE)}.pth', download=True)
    
    os.makedirs(benchmark_output_path, exist_ok=True)
    os.makedirs(benchmark_input_path, exist_ok=True)
    
    start_bench_time = time.time()
    for picture in get_pictures_from_dir(benchmark_input_path, DEFAULT_EXTENSION):
        path_to_image = f'{benchmark_input_path}/{picture}'
        
        if not is_picture_already_sampled(picture, benchmark_output_path, DEFAULT_EXTENSION):
            image = Image.open(path_to_image).convert('RGB')

            start = time.time()
            print(f'Sampling image [{path_to_image}]')

            sr_image = model.predict(image)
            save_to = f'{benchmark_output_path}/{picture}'
            sr_image.save(save_to)
            
            print(f'Sampling finished with time: [{str(time.time() - start)}].')

    print('Finished benchmark using the new algorithm with: [{}]'.format(str(time.time() - start_bench_time)))
    time.sleep(3)
    
    print('Starting the next benchmark...')
    benchmark_output_path = './benchmark/benchmark_output/old'
    start_bench_time = time.time()
    for picture in get_pictures_from_dir(benchmark_input_path, DEFAULT_EXTENSION):
        path_to_image = f'{benchmark_input_path}/{picture}'
        
        if not is_picture_already_sampled(picture, benchmark_output_path, DEFAULT_EXTENSION):
            image = Image.open(path_to_image).convert('RGB')

            start = time.time()
            print(f'Sampling image [{path_to_image}]')

            sr_image = model.predict_old(image)
            save_to = f'{benchmark_output_path}/{picture}'
            sr_image.save(save_to)
            
            print(f'Sampling finished with time: [{str(time.time() - start)}].')

    print('Finished benchmark using the old algorithm with: [{}]'.format(str(time.time() - start_bench_time)))
    
# benchmark_results()