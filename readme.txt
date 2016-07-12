Synopsis
A new software for automated detection of grooming trajectories in mice. M-Track is designed to detect the location of mice and of their labelled forepaws from video files.



Package Files
- MTrack_Qt.py      		 %  main function,  GUI
- MTrack.py           		 %  tracking Functionality
- DisplayLabel.py  		     %  display and cage drawing
- RoiLabel.py         		 %  display and roi drawing
- ColorLabel.py       	   	 %  displaying color selector image
- InfoDialog.py        		 %  displaying info messages



Installation

M-Track is compatible with Microsoft Windows, Mac OS X, and Linux. M-Track is written by Python.  OpenCV and PyQt are the major libraries, show as below.

(a) Python2.7

(b) Opencv3.0

(c) PyQt 4.8

(d) numpy 1.10.4

We  recommend install these packages from Anaconda.https://www.continuum.io/downloads




Tests
1. run MTrack_Qt.py
2. load video file in the M-Track folder acquired on a C57BL/6 (black fur) and on a Swiss Webster mouse (white fur). Running M-Track on these sample Video files generates a plain text output file, like the ones included here, named “Sample Data Output c57BL/6” and "Sample_Video_White_Mice.MOV".



Contributors
M-Track has been created by Sheldon L. Reeves (sheldonreeves316@gmail.com; sheldonreeves@icloud.com), Annalisa Scimemi (scimemia@gmail.com; ascimemi@albany.edu), and Lin Zhang (linzhang0529@gmail.com; lzhang22@albany.edu)

History
The first version of  MTracker had been created by Sheldon Reeves and Annalisa Scimemi on 6/24/15. It was relied on Python 3,OpenCV3, and PyQt5. Since 06/20/16, Lin Zhang and Annalisa Scimemi rewritten it based on Python 2.7,OpenCV3, and PyQt4.  Also,  several bugs are fixed, add more functions, and extend to more platforms.

License
Please review the terms and conditions of the license in the LICENSE_NPOSL-3.0 section of this repository before downloading the M-Track software. By downloading the M-Track software from this site you agree to be legally bound by the terms and conditions of the Open Source Initiative Non-Profit Open Software License 3.0 (NPOSL-3.0; https://tldrlegal.com/license/non-profit-open-software-license-3.0-(nposl-3.0)).
