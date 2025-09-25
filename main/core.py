import os
import tkinter as tk
import subprocess
import chardet
import img2pdf
from PyPDF2 import PdfReader
from pdf2image import convert_from_path
from translation import translate_text
from super_sampling import super_sample_images_in_directory
import argparse
import shutil

class Illuminate:
    def __init__(self, pdf_path, output_path):
        self.pdf_path = pdf_path
        self.output_path = output_path
        self.images_path = os.path.splitext(pdf_path)[0]
        self.output_transcript_cache, self.ocr_transcript_cache = '', ''
        self.ocr_path = 'C:\Program Files\Tesseract-OCR'
        self.ocr_transcription_folder_name = 'transcription'
        self.transcript_file_name = 'pdf_transcript_translated'
        self.original_transcript_file_name = 'pdf_transcript_original'
        self.ocr_input_lang = 'lat'
        self.ocr_output_lang = 'eng'
        self.ocr_extra_params = '-c tessedit_do_invert=0'
        self.max_pages = 0
        self.progress = 0

    def set_temp_dependencies(self):
        poppler_directory = os.path.join(os.getcwd(), 'poppler', 'Library', 'bin')
        os.environ["PATH"] += os.pathsep + poppler_directory

    def validate_file(self):
        if not os.path.isfile(self.pdf_path):
            raise FileNotFoundError(self.pdf_path)
        _, file_extension = os.path.splitext(self.pdf_path)
        if file_extension != ".pdf":
            raise ValueError(file_extension)

    def get_pictures_from_dir(self, dir):
        return [f for f in os.listdir(dir) if f.endswith('.png')]

    def scan_and_recover(self):
        os.makedirs(self.images_path, exist_ok=True)
        with open(self.pdf_path, 'rb') as file:
            pdf_reader = PdfReader(file)
            num_pages = len(pdf_reader.pages)
            self.max_pages = num_pages
            files_from_output = self.get_pictures_from_dir(self.images_path)
        
            for page_num in range(num_pages):
                image_name = 'page_{}.png'.format(page_num)
                
                if not image_name in files_from_output:
                    images = convert_from_path(self.pdf_path, first_page=page_num+1, last_page=page_num+1)
                    self.set_scan_progress(page_num)
                    
                    # Save only the first image from each page
                    image = images[0]
                    image_path = os.path.join(self.images_path, image_name)
                    image.save(image_path, 'PNG')
                    print(f'[Illuminate]: Picture for page {page_num} was created with name {image_name}')
                else:
                    print(f'[Illuminate]: Picture for page {page_num} was already found, skipping...')

    def set_scan_progress(self, current_page):
        self.progress = (current_page / self.max_pages) * 100
    
    def prepare_transcript(self):
        self.ocr_transcription_folder_name = 'transcription'
        os.chdir(self.ocr_path)
        os.makedirs(self.ocr_transcription_folder_name, exist_ok=True)
        # Insert into cache
        self.output_transcript_cache = self.insert_transcriptions_into_cache(f'{self.output_path}\{self.ocr_transcription_folder_name}')
        self.ocr_transcript_cache = self.insert_transcriptions_into_cache(f'{self.ocr_path}\{self.ocr_transcription_folder_name}')
    
    def finish_transcript(self):
        target_dir = f'{self.output_path}\{self.ocr_transcription_folder_name}'
        if not os.path.isdir(target_dir):
            print('Transcription folder not found in output, moving from OCR to OUTPUT')
            shutil.move(f'{self.ocr_path}\{self.ocr_transcription_folder_name}', self.output_path)
            
        os.chdir(self.output_path)
        self.translate_transcripts(f'{self.output_path}\{self.ocr_transcription_folder_name}')
    
    def page_separator(self):
        return ('\n---' * 30)
    
    def is_text_valid(self, text):
        return isinstance(text, str) and text.strip() != ''

    def get_encoding(self, file_path):
        with open(file_path, 'rb') as f:
            result = chardet.detect(f.read())
        return result['encoding']

    def translate_transcripts(self, folder_path):
        # Get all .txt files in the folder
        all_files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
        # all_files.sort(key=lambda f: int(f.split('.')[0]))

        # Get the files that have already been transcribed and remove the transcribed files from the list of all files
        files_to_translate = all_files # - self.output_transcript_cache #TODO fix??

        for file in files_to_translate:
            full_path = os.path.join(folder_path, file)
            # Get the encoding of the current file
            original_transcript_encoding = self.get_encoding(full_path)
            translated_encoding = 'utf-32'    
            
            with open(self.original_transcript_file_name, 'a', encoding=original_transcript_encoding) as original_transcript:
                with open(self.transcript_file_name, 'a', encoding=translated_encoding) as main_transcript:
                    with open(full_path, 'r', encoding=original_transcript_encoding) as transcript:
                        original_page = transcript.read()
                        if self.is_text_valid(original_page):
                            print('Valid text found, translating it, file [{}]'.format(file))
                            transcribed_text = translate_text(original_page, 'la')
                            original_transcript.write(original_page)
                            main_transcript.write(transcribed_text)
                            main_transcript.write(self.page_separator())


    def insert_transcriptions_into_cache(self, folder):
        if not os.path.isdir(folder):
            return set()

        # Check what files were already created so that we can skip it
        transcript_files = [f for f in os.listdir(folder) if f.endswith('.txt')]
        return set(transcript_files)

    def create_transcript_from_images(self, image_path, page_index):
        file_name = f'{page_index}.txt'
        # Check if the file has already been created
        if file_name in self.ocr_transcript_cache or file_name in self.output_transcript_cache:
            print(f'Transcription already exists for {image_path}')
            return file_name

        ocr_command = f'tesseract.exe "{image_path}" "{page_index}" --oem 1 {self.ocr_extra_params}' # --oem 1 -l {self.ocr_input_lang}
        # Note: This will only work if the script is run with administrator privileges
        process = subprocess.Popen(ocr_command, shell=True, stdout=subprocess.PIPE)
        process.wait()

        # print(process.stdout.read().decode()) # Debug
        print(f'Transcription created for {image_path}')
        return file_name

    def get_image_files(self, files_dir):
        image_files = [f for f in os.listdir(files_dir) if f.endswith('.png')]
        image_files.sort(key=lambda f: int(f.split('_')[1].split('.')[0]))
        return image_files

    def create_transcripts(self, image_files, files_dir):
        current_page = 0
        self.prepare_transcript()
        for f in image_files:
            path = os.path.join(files_dir, f)
            transcript_file = self.create_transcript_from_images(path, current_page)
            file_path = self.ocr_path
            
            if transcript_file in self.output_transcript_cache:
                file_path = self.output_path
            
            destination_path = os.path.join(file_path, self.ocr_transcription_folder_name, transcript_file)
            # Check if the transcript file already exists in the destination folder
            if not os.path.isfile(destination_path):
                shutil.move(transcript_file, f'{self.ocr_path}\{self.ocr_transcription_folder_name}')
            current_page += 1

    def images_to_pdf(self, files_dir):
        print('All images finished, creating transcriptions...')
        image_files = self.get_image_files(files_dir)
        self.create_transcripts(image_files, files_dir)
        self.finish_transcript()
        print('Transcription finished, reassembling images to pdf...')
        self.reassemble_to_pdf([os.path.join(files_dir, f) for f in image_files], self.output_path)


    def reassemble_to_pdf(self, image_paths, pdf_path):
        temp_pdf_path = 'temp.pdf'
        with open(temp_pdf_path, 'wb') as f:
            f.write(img2pdf.convert(image_paths))
            
        final_pdf_path = os.path.join(os.path.dirname(pdf_path), 'Illuminate - ' + os.path.basename(pdf_path))
        shutil.move(temp_pdf_path, final_pdf_path)

    def super_sample_images(self):
        super_sample_images_in_directory(self.images_path, self.output_path)
        self.images_to_pdf(self.output_path)

    def clean_up(self):
        print('Supposed to clean up {}'.format(self.images_path))
        root = tk.Tk()
        root.destroy()
        # shutil.rmtree(self.images_path)

def parse_args():
    parser_info = {
        'description': "Illuminate can enhance a PDF file, you can recover old and destroyed books. This a research tool, magic should be freely available for the right people.",
        'arguments': {
            '--pdf': { 'type': str, 'description': 'The book path in which you want to recover, the book should be in a ".pdf" format.' },
            '--output': { 'type': str, 'description': 'The path where the new PDF file should be saved.' }
        }
    }

    parser = argparse.ArgumentParser(description=parser_info['description'])
    for argument in parser_info['arguments']:
        current_argument = parser_info['arguments'][argument]
        parser.add_argument(argument, type=current_argument['type'], help=current_argument['description'])

    return parser.parse_args()

def start_illuminate(illuminate):
    illuminate.set_temp_dependencies()
    illuminate.validate_file()
    illuminate.scan_and_recover()
    illuminate.super_sample_images()
    illuminate.clean_up()