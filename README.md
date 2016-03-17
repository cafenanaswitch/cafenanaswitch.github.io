# Cafe Nana Switch
Welcome to the project page for the Cafe Nana Switch. 

### How it works
The main script for the Nana Switch is the file `switchcheck.py`
It basically works by checking the status of a switch, then updating LEDs and a [GitHub Pages Repo] (https://pages.github.com/).
This is the file that is run at startup on the Raspberry Pi. The following is a walkthrough of the file.

First, all of the relevant libraries are imported. The threading library is used to loop the `checkstatus()` funtion. The time library is used to append the current time on the website, os is used to run a shell script, and BeautifulSoup is used to edit the HTML file of the website. Finally RPi.GPIO is used to controll the GPIO pins on the Pi.

Next, the GPIO pin labeling system is set to BCM mode. This means that the python file will refer to pins by thier GPIO numbering rather than their physical numbering. Read more about that [here] (https://www.raspberrypi.org/documentation/usage/gpio-plus-and-raspi2/README.md), and find a nice pinout diagram [here] (https://pinout.xyz/).

The GPIO pins are then set as inputs or outputs. If a pin's voltage is to be read, it should be set as an input, and if it is to be changed by the program, it should be set as an output.

Next, relevent parameters are set, including a variable for our desired refresh rate, and the path for the HTML file. 

In the `checkSwitch()` function, cafestatus is declared as global, so the value we just set for it will be carried into the function.
Next, the function call `threading.Timer(pollTime, checkStatus).start()` loops the function every pollTime seconds (in our case, every 2s).

Then, the program reads the state of the switch (pin 17) to see if the cafe is open. If the switch is on the open position, and there is a discrepancy between what the `cafestatus` variable is, and what is should be (1), the program knows that this represents a change in the switch's state, and acts accordingly (This way LED updates and github pushes only happen if they need to). The LED pins (23 and 24) are updated, the `cafestatus` variable is updated to what it should be, and the `updateHTML(statuscode)` function is called to update the website. A similar set of controll statments are used if the switch is in the closed position. 

In the `updateHTML` function, the text of the website is determined by the status code argument. Then, the `index.html` file is opned, and BeautifulSoup is used to track down the string that has to be replaced in the website. BeautifulSoup then generates a new set of HTML, and writes it in the `index.html` file. a call to `os.system` is used to run the `gitpusher.sh` file which adds, commits, and pushes the file to github over SSH for hosting.

To set up SSH keys for github on the Pi, follow these steps:
* [Step 1] (https://help.github.com/articles/checking-for-existing-ssh-keys/)
* [Step 2] (https://help.github.com/articles/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent/)
* [Step 3] (https://help.github.com/articles/adding-a-new-ssh-key-to-your-github-account/)

The general implementation/code for the project was inspired by [this video from DIY Tryin] (https://www.youtube.com/watch?v=ZszlVVY1LXo)






