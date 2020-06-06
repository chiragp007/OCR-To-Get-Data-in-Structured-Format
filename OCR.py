import pytesseract
from pytesseract import Output
import cv2
import sys
from subprocess import Popen, PIPE
import pandas as pd
from pdf2image import convert_from_path

def text_model(pdf_path,out_path):
        create_config = r'-c preserve_interword_spaces=1 --oem 1 --psm 1 -l eng+ita'
        pages = convert_from_path(pdf_path, 500)
        for i in range(len(pages)):
            pages[i].convert('L').save(out_path + str(i) + ".jpeg")
            image = cv2.imread(out_path+str(i)+".jpeg")
            image = cv2.resize(image, (2000, 2000))
            text = pytesseract.image_to_data(image, config=create_config, output_type=Output.DICT)
            my_df = pd.DataFrame(text)
            final_df = my_df[(my_df.conf != '-1') & (my_df.text != ' ') & (my_df.text != '')]

            sorted_blocks = final_df.groupby('block_num').first().sort_values('top').index.tolist()
            for block in sorted_blocks:
                curr = final_df[final_df['block_num'] == block]
                sel = curr[curr.text.str.len() > 3]
                char_w = (sel.width / sel.text.str.len()).mean()
                prev_par, prev_line, prev_left = 0, 0, 0
                text = ''
                for ix, ln in curr.iterrows():
                    if prev_par != ln['par_num']:
                        text += '\n'
                        prev_par = ln['par_num']
                        prev_line = ln['line_num']
                        prev_left = 0
                    elif prev_line != ln['line_num']:
                        text += '\n'
                        prev_line = ln['line_num']
                        prev_left = 0

                    added = 0
                    if ln['left'] / char_w > prev_left + 1:
                        added = int((ln['left']) / char_w) - prev_left
                        text += ' ' * added
                    text += ln['text'] + ' '
                    prev_left += len(ln['text']) + added + 1
                text += '\n'

                file1 = open(out_path+"page"+str(i)+".txt", "a+")
                file1.write(text)
                file1.write("\n")
                file1.close()


def remove_lines(img_path,out_path):
    commands = ['convert',img_path, '-type', 'Grayscale','-negate','-define','morphology:compose=darken','-morphology' ,'Thinning','Rectangle:1x80+0+0<','-negate',out_path ]
    process = Popen(commands,stdout=PIPE,stderr=PIPE)
    out,err = process.communicate(timeout=60)


if __name__ =='__main__':
    if sys.argv.__len__() == 3:
        text_model(sys.argv[1], sys.argv[2])
    else:
        remove_lines(sys.argv[1],sys.argv[2])
