## Custom code for Yahboom G1 Tank

- [product ref](https://category.yahboom.net/collections/rp-robotics/products/g1tank)
- [product wiki](http://www.yahboom.net/study/G1-T-PI)

### Implementation with PS4 Controller

#### Metadata

- ** /boot/config.txt **:

> ```
framebuffer_width=1280
framebuffer_height=720

hdmi_force_hotplug=1

dtparam=i2c_arm=on
dtparam=spi=on

dtparam=audio=on

camera_auto_detect=1

display_auto_detect=1

dtoverlay=vc4-kms-v3d
max_framebuffers=2

arm_64bit=1

disable_overscan=1

[cm4]
otg_mode=1

[all]

[pi4]
arm_boost=1

[all]
enable_uart=1
hdmi_enable_4kp60=1
> ```

