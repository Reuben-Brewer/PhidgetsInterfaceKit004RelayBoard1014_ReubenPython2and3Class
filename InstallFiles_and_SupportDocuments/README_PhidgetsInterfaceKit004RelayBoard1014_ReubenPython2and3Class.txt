########################  
PhidgetsInterfaceKit004RelayBoard1014_ReubenPython2and3Class

Wrapper (including ability to hook to Tkinter GUI) to control Phidgets four-relay controller 1014 (non VINT).

From Phidgets' website:
"The 1014 has 4 Relay Outputs for switching AC or DC power; the relays are Single Pole Double Throw (SPDT). The PhidgetInterfaceKit 0/0/4 allows you to control high power devices such as incandescent light bulbs, fans, and pumps by electronically switching power on and off."

PhidgetInterfaceKit 0/0/4
ID: 1014_2B
https://www.phidgets.com/?prodid=1020

Reuben Brewer, Ph.D.

reuben.brewer@gmail.com

www.reubotics.com

Apache 2 License

Software Revision G, 09/21/2022

Verified working on: 
Python 2.7, 3.8.
Windows 8.1, 10 64-bit
Raspberry Pi Buster 
(no Mac testing yet)

*NOTE THAT YOU MUST INSTALL BOTH THE Phidget22 LIBRARY AS WELL AS THE PYTHON MODULE.*

########################  

########################### Python module installation instructions, all OS's

PhidgetsInterfaceKit004RelayBoard1014_ReubenPython2and3Class, ListOfModuleDependencies: ['future.builtins', 'Phidget22']
PhidgetsInterfaceKit004RelayBoard1014_ReubenPython2and3Class, ListOfModuleDependencies_TestProgram: ['MyPrint_ReubenPython2and3Class']
PhidgetsInterfaceKit004RelayBoard1014_ReubenPython2and3Class, ListOfModuleDependencies_NestedLayers: ['future.builtins']
PhidgetsInterfaceKit004RelayBoard1014_ReubenPython2and3Class, ListOfModuleDependencies_All: ['future.builtins', 'MyPrint_ReubenPython2and3Class', 'Phidget22']

https://pypi.org/project/Phidget22/#files

To install the Python module using pip:
pip install Phidget22       (with "sudo" if on Linux/Raspberry Pi)

To install the Python module from the downloaded .tar.gz file, enter downloaded folder and type "python setup.py install"

###########################

########################### Library/driver installation instructions, Windows

https://www.phidgets.com/docs/OS_-_Windows

###########################

########################### Library/driver installation instructions, Linux (other than Raspberry Pi)

https://www.phidgets.com/docs/OS_-_Linux#Quick_Downloads

###########################

########################### Library/driver installation instructions, Raspberry Pi (models 2 and above)

https://www.phidgets.com/education/learn/getting-started-kit-tutorial/install-libraries/

curl -fsSL https://www.phidgets.com/downloads/setup_linux | sudo -E bash -
sudo apt-get install -y libphidget22
 
###########################