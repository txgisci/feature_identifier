# Feature Identifier 

The purpose of the CLI script is to automate the process of downloading specified images from https://eol.jsc.nasa.gov/SearchPhotos/ 


## Setup
Step 1. Setup New Anaconda Environment:

From within your user directory run the command:
```
conda create --name ENVNAME
```

Step 2. Activate your Project Environment: 

After activating your environment, you should see the name of your environment in parenthesis on the left of your user name.
```
conda activate ENVNAME
```

Step 3. Install Packages with Conda:

This step may take a minute. 
```
conda install keras matplotlib pillow tensorflow-gpu
```

Step 4. Setup File Directory 

Create a project folder and copy ConvNN_binary.py and mkDirStruct.sh from the repositroy

From your project foldoer, run the mkDirStruct.sh script with: 

```
./mkDirStruct.sh
```

Step 5. Edit the file path to images in ConvNN_binary.py

Line 29: Edit image_dir = "/home/.../project_folder/your_feature"

Step 6. Populate your_feature with the images to be trained and tested.

















