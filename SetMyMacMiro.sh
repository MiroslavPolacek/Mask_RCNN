##First install anaconda3
#Then
conda install nb_conda #to integrate conda with jupyter notebook

##Install basic environment

#Create environment
conda create -n TreeRingCNN python=3.7
conda activate TreeRingCNN
#install requirements and packages for TreeRingCNN
cd /Users/miroslav.polacek/Dropbox\ \(VBC\)/'Group Folder Swarts'/Research/CNNRings/Mask_RCNN

pip install -r requirements.txt

##Install environment to experiment with plaidml

conda create -n envplaidml python=3.6
conda activate envplaidml

pip install plaidml-keras plaidbench
plaidml-setup
plaidbench keras mobilenet
plaidbench --batch-size 16 keras --train mobilenet

cd /Users/miroslav.polacek/Dropbox\ \(VBC\)/'Group Folder Swarts'/Research/CNNRings/Mask_RCNN

pip install -r requirements.txt