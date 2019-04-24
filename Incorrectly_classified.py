from shutil import copyfile
import csv
import os


input_file = 'Predictions.csv'
fieldnames = ['id','confidence_level']

# Creating directories to hold incorrectly classified images
mode = 0o777
os.makedirs('incorrect_predictions/false_positives', mode=mode)
os.makedirs('incorrect_predictions/false_negatives', mode=mode)


with open(input_file, 'r') as f:

    # Reader object containes all csv values
    reader = csv.reader(f)
    # row = a python list of all values in single row
    for row in reader:
        image_id_path = row[0]
        confidence_val = float(row[1])
        
        
        if 'not' in image_id_path and confidence_val >= .5:
            img_id = image_id_path.replace('not_your_feature/', '')
            dest = 'incorrect_predictions//false_positives//' + img_id + '_' + str(confidence_val) + '.jpg'
        elif 'not' not in image_id_path and confidence_val < .5:
            img_id = image_id_path.replace('your_feature/', '')
            dest = 'incorrect_predictions//false_negatives//' + img_id + '_' + str(confidence_val) + '.jpg'
        else:
            continue
                    
        src = 'island_images_336x224//test//' + image_id_path
        
        copyfile(src, dest)
