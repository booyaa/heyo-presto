# Heyo Presto

## Scripts

### Audio

Starting to experiment with the built in piezo speaker. It's not very powerful, but if you keep the lower frequences and don't try to complicated 

#### Volume control

code: [audio-volume.py](./audio-volume.py)

Using duty cycle to increase volume of simple frequency range. Borrowed heavily from [Sam Galope's][pwmAudioGuideLink] ESP32 PWM audio post.

#### Playing samples badly

code: [audio-samples.py](./audio-samples.py)

This is inspired by antirez (yes of Redis fame)

I grabbed the original wav files from GitHub:

- [R2D2 cheerful][r2d2CheerfulAudio]
- [Imperial march][imperialMarchAudio]

Converted them to pcm (raw) files using ffmpeg

```sh
ffmpeg -i some-sound.wav -ar 8000 -acodec pcm_u8 -f u8 some-sound.raw
```

It took a bit of tinkering to work out how to slow down the samples, but to be honest it felt like guess work. I should probably reread antirez's post.

The samples are very quiet (well on my Presto it sounds quiet on mine).

> ![IMPORTANT]
> You'll need to copy the raw files over to the Presto using `mpremote cp` even if you use `mpremote run` to run the script locally.

### Scaled text

code: [heyo-presto.py](./heyo-presto.py)

Displays text at varying scale using the 8-bit font and Pico Graphics

code: [heyo-vecto.py](./heyo-vecto.py)

Displays text at varying scale using Pico Vectors


### Display web image

code: [display-web-image.py](./display-web-image.py)

How to display an image from the internet without saving.

> [!WARNING]
> The image needs to be small enough to load into RAM

### Sleeper

code: [sleeper.py](./sleeper.py)

A very poor attempt at power saving. It works by turning the backlight off and goes into a loop that runs between idle/light sleep. Copy this to your presto and pick it from the launcher. I've not measure how much power draw this is compared to running a regular app. If you're really paranoid you could just unplug the presto.

### Presto bridge

code: [presto_bridge.py](./presto_bridge.py)

This is a small flask app to handle sending and receive messages to meshtastic.
We only send to a specific person (in my case my mobile node).

```sh
export MESHTASTIC_HOST='1.2.3.4' # IP address of your node
export MESHTASTIC_DEFAULT_SENDER='!deadbeef' # user id
flask --debug --app presto_bridge run --port 5050 --host 0.0.0.0                                                
```

### Meshtastic console

code [meshtastic_console.py](./meshtastic_console.py)

This is a Presto app that allows you to send and receive messages from 
meshtastic. It requires the Presto bridge to work.

Upload it you Presto and change the `HOST_BASE_URL` to match the IP address 
and URI scheme where your Presto bridge is running on.

## Others

- The [tweaked](./tweaked/) folder is where I've taken existing examples and made small changes like backlight.
- The [examples-from-others](./examples-from-others/) folder is stuff I've found on the internet that I want to keep for reference.

## Resources

### Reading

- [Shop](https://shop.pimoroni.com/products/presto?variant=54894104019323) - specs of the Presto
- [Learn](https://learn.pimoroni.com/article/getting-started-with-presto#writing-your-own-code) - the getting started guide for the Presto
- [Docs](https://github.com/pimoroni/presto/tree/main/docs) - the documentation folder for the Presto code examples
  - [Pico Graphics](https://github.com/pimoroni/pimoroni-pico/blob/main/micropython/modules/picographics/README.md) - the documentation for the Pico Graphics module. Also contains details of how to use BitBank's [JPEGDEC](https://github.com/bitbank2/JPEGDEC)

### Software / Tools

- [Presto](https://shop.pimoroni.com/products/presto?variant=54894104019323) (shop link)
- [Thonny](https://thonny.org/) IDE to easily connect to the presto
- [mpremote](https://docs.micropython.org/en/latest/reference/mpremote.html) when you're ready to hit the terminal
  - [mpr](https://github.com/bulletmark/mpr) - a wrapper around mpremote to use wildcards and cross compiled runs
  
### Thonny set up

- Make sure your Presto is connected to your computer via the USB data cable that came with the kit
- Set your interpreter to "MicroPython (Raspberry Pi Pico)" (`Tools > Options > Interpreter tab`)
- Select the correct USB serial device mine was "Board CDC @ COM4" you may have a different USB device name and serial port number (COM)
- Check "Interrupt working program on connect", this will stop the launch and go into dev mode
- You can then use file open and select "Raspberry Pi Pico" to open files on the Presto
- You can press the Play butto to start programs

### mpremote

I use [uv](https://docs.astral.sh/uv/) as my all in one python tool. If you don't use uv, you should be able to reuse these commands by removing uv.

```sh
uv venv
# activate environment .venv/bin/activate (*nix) .\.venv\Scripts\activate
# TODO: uv pip install -r requirements
uv pip install mpremote
mpremote ls
# to move files on the remote file system
mprmote cp :some_file_on_remote_fs.py :some_dir_on_remote_fs/
mprmote rm :some_file_on_remote_fs.py
```

> [!Note]
> `:` indicates remote file system

### Miscellany tips

#### Convert your square images into 240x240 px. This assumes they're in the directory

```sh
mkdir converted
ls -tp | xargs -I{} ffmpeg -i {} -vf scale=240:240 "converted/{}"
mpremote cp converted/. :gallery/
```

#### Create new icons

Source: [pimoroni](https://learn.pimoroni.com/article/getting-started-with-presto#adding-your-own-examples-to-the-launcher)

- Search for [icon](https://fonts.google.com/icons?selected=Material+Symbols+Outlined:piano:FILL@0;wght@400;GRAD@0;opsz@24&icon.query=piano&icon.size=24&icon.color=%23e3e3e3)
- Select icon
- Scroll down right panel nav until you see code point

> [!Important]
> You need to download the materials symbol font from the source repo

```sh
# Piano codepoint is e521
cd examples-from-others
python font2picovector.py --font MaterialSymbolsOutlined-Regular.ttf --size 40x40 e521
```


[pwmAudioGuideLink]: https://www.samgalope.dev/2025/01/08/pwm-based-audio-generation-with-esp32-a-simple-guide-to-sound-creation/
[r2d2CheerfulAudio]: https://github.com/CoderDojoTC/robot-media/blob/master/wav-8k/r2d2-cheerful.wav
[imperialMarchAudio]: https://github.com/CoderDojoTC/robot-media/blob/master/wav-files/imperial_march.wav