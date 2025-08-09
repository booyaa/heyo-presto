# Heyo Presto

## Scripts

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

## Resources
- [Presto](https://shop.pimoroni.com/products/presto?variant=54894104019323) (shop link)
- [Thonny](https://thonny.org/) IDE to easily connect to the presto
- [mpremote](https://docs.micropython.org/en/latest/reference/mpremote.html) when you're ready to hit the terminal
  - [mpr](https://github.com/bulletmark/mpr) - a wrapper around mpremote to use wildcards and cross compiled runs
  
## Thonny set up

- Make sure your Presto is connected to your computer via the USB data cable that came with the kit
- Set your interpreter to "MicroPython (Raspberry Pi Pico)" (`Tools > Options > Interpreter tab`)
- Select the correct USB serial device mine was "Board CDC @ COM4" you may have a different USB device name and serial port number (COM)
- Check "Interrupt working program on connect", this will stop the launch and go into dev mode
- You can then use file open and select "Raspberry Pi Pico" to open files on the Presto
- You can press the Play butto to start programs

## mpremote

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

## Miscellany tips

### Convert your square images into 240x240 px. This assumes they're in the directory

```sh
mkdir converted
ls -tp | xargs -I{} ffmpeg -i {} -vf scale=240:240 "converted/{}"
mpremote cp converted/. :gallery/
```

### Create new icons

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
