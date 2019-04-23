# Read in a csv of [your/not_your_feature, image_id, confidence]
# not_your_feature = 0, your_feature = 1
# find type of confidence level, convert to string if need be
# place false_predictions.py and Predictions.csv file in the same directory
# that has your islands_images_336x224
# script will create the false_positives and false_negatives directories
# include the confidence level with new image_id name
# if (not_your_feature && confidence > .5) then cp image_id path into false positive directory
# if (your_feature && condfidence < .5) then cp image_id path into false negative directory
# from shutil import copyfile
# copyfile(src, dst)

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





        # using zip() to write 3 columns to csv
        # https://stackoverflow.com/questions/17704244/writing-python-lists-to-columns-in-csv

        # with open(r'img_id_list.csv', 'a', newline='') as csvfile:
        #           writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        #           writer.writerow({'id':new_img_id, 'confidence_level':confidence_val})
