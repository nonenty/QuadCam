# QuadCam

A proof of conpect of camera API for Microsoft Flight Simulator 2020

**Only tested on the microsoft store version**

# Principle

Inject value to the calculated address based on the offset defined in `definitions.json`

# Where do these offsets come from?

1. Install Cheat Engine
2. In developer mode -> Aircraft, turn on Camera Blend
3. Switch to the showcase camera.
4. Search memory for the values displayed on the left-bottom corner. Try to move your camera to narrow the results.
5. Try to change the value of these address. Hopefully you will find the only one that will move the camera.
6. Find base address and offsets to that address.