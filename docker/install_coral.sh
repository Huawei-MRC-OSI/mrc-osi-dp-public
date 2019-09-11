#!/bin/sh

mkdir /tmp/coral
cd /tmp/coral

set -e -x

pip3 install pillow
apt-get install -y usbutils
wget https://dl.google.com/coral/edgetpu_api/edgetpu_api_latest.tar.gz \
  -O edgetpu_api.tar.gz --trust-server-names
tar xzf edgetpu_api.tar.gz
sed -i 's/$(uname -v)/Ubuntu/g' edgetpu_api/install.sh
sed -i 's/\(^.*edgetpu-accelerator.rules.*$\)/# \1/g' edgetpu_api/install.sh
sed -i 's/\(^.*sudo udevadm control --reload-rules && udevadm trigger.*$\)/# \1/g' edgetpu_api/install.sh
sed -i 's/python3-pip//g' edgetpu_api/install.sh
sed -i 's/python3-pil//g' edgetpu_api/install.sh
sed -i 's/python3-numpy//g' edgetpu_api/install.sh
yes | edgetpu_api/install.sh

# Testing stuff
wget \
  https://dl.google.com/coral/canned_models/mobilenet_v2_1.0_224_inat_bird_quant_edgetpu.tflite\
  https://dl.google.com/coral/canned_models/inat_bird_labels.txt \
  https://coral.withgoogle.com/static/docs/images/parrot.jpg

cat >test.sh <<EOF
#!/bin/sh
cd /usr/local/lib/python3.6/dist-packages/edgetpu/demo
python3 classify_image.py \
  --model /tmp/coral/mobilenet_v2_1.0_224_inat_bird_quant_edgetpu.tflite \
  --label /tmp/coral/inat_bird_labels.txt \
  --image /tmp/coral/parrot.jpg
EOF
chmod +x test.sh
