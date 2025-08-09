# Stereoscopic timelapses with a microcontroller and an Xreal Beam Pro

Here you find a code example from [Parth3D.co.uk](https://parth3d.co.uk/) that shows how to build a timelapse controller, a.k.a. an intervalometer, from an ESP32 microcontroller for use with Android, iOS and iPadOS devices. It was designed especially to allow making 3D stereoscopic timelapse movies with an Xreal Beam Pro.

* The INO file is used to program an M5Stack AtomS3 Lite microcontroller (which has USB HID hardware) to be an intervalometer (one second but can be changed in code).

* The Python file is an example of how to process and composite the image frames from the Beam Pro as well as of how to rename the files to have their order included in the filename (Beam Pro camera app images are named based on the date and time).

* A Windows batch file illustrating how to use FFMPEG to stitch all the individual image frames (as output by the Python script) into a single MP4 movie file.

The code here was provided in a Parth3D blog post which you can find at the following URL:

[https://parth3d.co.uk/stereoscopic-timelapses-with-a-microcontroller-and-an-xreal-beam-pro](https://parth3d.co.uk/stereoscopic-timelapses-with-a-microcontroller-and-an-xreal-beam-pro)
