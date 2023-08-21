# dawn synths
## code and schematics repo

please take everything here with a grain of salt, currently its much more of a dumping ground for relevent info pieces than a comprehensive guide on how to build these modules. 

if you have any questions feel free to either leave an issue on the repo or send me an email.

### standardization

by not using any exsting standard for modular, i sort of inadvertantly created my own standard. i have some opinions about how i prefer modular systems to work and they'll get incresingly clear as i continue to put this thing together. right now the basics are:

- 0 - 3.3v signal
- 5v input from either micro usb or usb-c
- modules can run at whatever sample rate they want to
- focus on simplicity, only add what you need (https://en.wikipedia.org/wiki/Single-responsibility_principle)
- voltage to hz mapping tbd
- polyphonic standard tbd


IMPORTANT: these modules are incompatable with eurorack or any other modular system. dawn synths designs are based on 3.3v max signal and usb 5v for power. eurorack uses 12v for power and 10v to -10v for signal which will quickly fry one of these modules. the incompatability is for simplicity reasons, the majority of hobbyist electronics stuff is made for 5v and 3.3v. i might do a eurorack compatable analog series of modules later, but for now analog is still scary to me. what's an op amp, i'll never know.
