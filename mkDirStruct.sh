#Author: Aaron Hunt

#=============================================
# This script creates a directory structure to
# be used with the ConvCNN
#=============================================

mkdir your_feature
cd your_feature
mkdir test
mkdir train
cd test
mkdir your_feature
mkdir not_your_feature
cd ..
cd train
mkdir your_feature
mkdir not_your_feature
cd ../..
mkdir trained_network_models
cd trained_network_models
mkdir Checkpoints
mkdir Plots
cd Checkpoints
mkdir save_every_epoch
cd ..
cd Plots
mkdir Loss

