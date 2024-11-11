# Pico-glitcher

![2024-04-24-21-50-46-538](https://github.com/user-attachments/assets/e14faa53-ffcb-4fcf-bea4-1d29d3760d72)
[click here to see the voltage glitching in progress :-)](https://github.com/user-attachments/assets/83b4dde9-f6ae-445b-a65e-2d5682e1be58)

Pico-glitcher is a set of tools used to perform a voltage glitching attack on CCxxxx Texas Instruments wireless chips. The attack can overcome a debugging lock check and allows the attacker to dump the device firmware from a locked chip.

I reproduced the findings from the [original blogpost](https://zeus.ugent.be/blog/22-23/reverse_engineering_epaper/) about this vulnerability  and added some improvements to the code.

## Fork information

In this fork, I reproduced Jaspers voltage glitching experiments on CC2510 and I extended the pico-glitcher functionality.

- I sped up considerably voltage glitch parameter upload function (`update_waveform()`) used in `explore.py` and `exploit.py`. This means it is much faster to update the glitch parameters and find the correct ones using grid search. It is also viable to tune the parameters during the attack (firmware dump) phase.
- I added a hillclimber algorithm to the `exploit.py` script so that the glitch locations improve on-the-fly, as the optimal locations change through time due to temperature change and other factors. 
- You can find the glitch parameters I found effective in `analyze.py`.
- `analyze.py` plots few more plots. `exploit.py` plots a heatmap of succesful glitch locations.
- tools to verify memory dump (`check_data.py`) and convert it into binary file (`csv_to_bin.py`)

## Build instructions

Install [pico-sdk](https://github.com/raspberrypi/pico-sdk). Then clone the repo and run the following commands:

```bash
mkdir build
cd build
cmake ..
make
```

To flash the firmware, connect the board and copy the `.uf2` file to the board.

## Soldering instructions

As described in the [original blogpost](https://zeus.ugent.be/blog/22-23/reverse_engineering_epaper/), to successfully glitch CC2510, one needs to desolder the decoupling capacitor on the DCOUPL pin. I used the IRFHS8342 MOSFET and it worked as well as Jaspers MOSFET choice. 
As this was the first time doing the crowbar attack, I was not completely sure about the MOSFET connections. The correct connections are: mosfet source -> ground, mosfet drain -> DCOUPL, mosfet gate -> raspberry. 

![MOSFET_EINK](https://github.com/user-attachments/assets/fa4eb0f5-745f-477f-9a43-edc6bb5b3623)

## Finding the glitch position

My glitch positions were quite different to Jaspers. To quickly find the right position, I recommend using a voltage analyzer and tuning the position parameter so that the glitch locations match approximately Jaspers logic analyzer trace:
![View of the debug sequence on a logic analyser. Orange lines separate the different debug instructions, red lines are the timings of the glitches](https://pics.zeus.gent/db5veC76CU7sK4k0m9W86zcwVybp01DvG5x8ARIx.png)

## Successful attack

I successfully dumped firmware from two devices using this method. The firmware download took around 10 hours to complete for each attempt.

## Original README:

Most information is in the blogpost: https://zeus.ugent.be/blog/22-23/reverse_engineering_epaper/

This is a voltage glitching exploit tool that works against the CC2510, and probably also against other CCxxxx Texas Instruments wireless chips that contain an 8051 core and the ChipCon debugging protocol.

It runs on a Raspberry Pi Pico chip. To start working on an exploit for your device, get a development board (or a spare device) and run the following steps on a separate computer, without moving or touching the board the CC2510 chip is on too much:

1. Check if readout protection is enabled using `serial_number.py`
2. If not, you're in luck, use `reader.py` to read out the firmware
3. If it is, wipe the development board and run `explore.py` (without the MOSFET soldered) to make sure the debug sequence works. Then write to it (`writer.py`) and lock it again (`locker.py`).
3. Solder the MOSFET and use `explore.py` with a wide range and low iterations count (100) to find the approximate location of both glitch locations. In `analyze.py` are some estimations that worked on my board.
4. Narrow the glitch locations and duration down with 10000 iterations and a smaller range (~50)
5. Verify you can read out data with `exploit.py` (you'll need to modify the params)
5. Solder the MOSFET on the second board, and redo the parameter tuning, and re-run `exploit.py`. This is best done in a tmux session, since it will take a long time.

I used the IRLML6246TRPBF MOSFET, but other fast N-channel MOSFETs should also work.
