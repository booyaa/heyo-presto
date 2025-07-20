# Heyo Presto

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

Convert your square images into 240x240 px. This assumes they're in the directory

```sh
mkdir converted
ls -tp | xargs -I{} ffmpeg -i {} -vf scale=240:240 "converted/{}"
mpremote cp converted/. :gallery/
```