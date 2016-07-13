# M-Track
A new software for automated detection of grooming trajectories in mice.

Please review the terms and conditions of the license in the LICENSE_NPOSL-3.0 section of this repository before downloading the M-Track software. By downloading the M-Track software from this site you agree to be legally bound by the terms and conditions of the Open Source Initiative Non-Profit Open Software License 3.0 (NPOSL-3.0; https://tldrlegal.com/license/non-profit-open-software-license-3.0-(nposl-3.0)).
    
**OVERVIEW**  
M-Track has been created by Sheldon L. Reeves (sheldonreeves316@gmail.com; sheldonreeves@icloud.com) and Annalisa Scimemi (scimemia@gmail.com; ascimemi@albany.edu). M-Track is designed to detect the location of mice and of their labelled forepaws from video files. M-Track is compatible with Microsoft Windows and Mac OS X operating systems, debian and non-debian Linux installations. M-Track uses the Python language and the Open CV and PyQt libraries.  

Two executable standalone versions of M-Track for Linux OS are currently available: one of them allows the user to visualize the orientation of the mouse body (MTrack_Qt_v1r1), the other does not have this feature (MTrack_Qt_v1r2).  

***Linux:***    
MTrack_Qt_v1r1 - The user can visualize the orientation of the mouse body       
MTrack_Qt_v1r2 - The user cannot visualize the orientation of the mouse body 

***Mac OS X: COMING SOON***  
MTrack_Qt_v2r1 - The user can visualize the orientation of the mouse body       
MTrack_Qt_v2r2 - The user cannot visualize the orientation of the mouse body 

***Microsoft Windows: COMING SOON***  
MTrack_Qt_v3r1 - The user can visualize the orientation of the mouse body       
MTrack_Qt_v3r2 - The user cannot visualize the orientation of the mouse body 

Two sample video files are included in the M-Track folder acquired on a C57BL/6 (black fur) and on a Swiss Webster mouse (white fur). Running M-Track on these sample Video files generates a plain text output file, like the ones included here, named “Sample Data Output c57BL/6” and "Sample_Video_White_Mice.MOV". The following settings were used to generate this sample output file in each one of the two mice:   

***Optimized settings to track grooming in the black-fur mouse on the left-hand side of "Sample_Video_Black_Mice.MOV"***  

***Body Color Mask***      
L Hue = 0                             
L Sat = 0   
L Val = 0   
U Hue = 180     
U Sat = 255     
U Val = 98       
Dilation = 1          
Min Box Size = 200   
Collision Detect = ON   

***LF Color Mask***     
L Hue = 60   
L Sat = 5   
L Val = 86   
U Hue = 110     
U Sat = 115     
U Val = 120       
Dilation = 1          
Min Box Size = 20   

***RF Color Mask***     
L Hue = 106   
L Sat = 178   
L Val = 150   
U Hue = 145     
U Sat = 220     
U Val = 195       
Dilation = 1   
Min Box Size = 20   

***Optimized settings to track grooming in the white-fur mouse on the left-hand side of "Sample_Video_White_Mice.MOV"***  

***Body Color Mask***     
L Hue = 0                             
L Sat = 0   
L Val = 113   
U Hue = 180     
U Sat = 255     
U Val = 255       
Dilation = 1          
Min Box Size = 700      
Collision Detect = ON   

***LF Color Mask***     
L Hue = 15   
L Sat = 21   
L Val = 63   
U Hue = 65     
U Sat = 124     
U Val = 138       
Dilation = 1   
Min Box Size = 100   

***RF Color Mask***     
L Hue = 0   
L Sat = 110   
L Val = 122   
U Hue = 180     
U Sat = 255     
U Val = 255       
Dilation = 1    
Min Box Size = 60   

**INSTALL M-Track FROM SOURCE CODE**  
The M-Track source code can be run by executing MTrack_Qt with Python 3. The installation instructions for different OS are reported below. 

***Required packages for Linux installs (tested for Ubuntu 14.04.1 LTS)***   

 1. Open CV 3.0.0 
 2. Qt 5.0.2  
 3. PyQt 5.4.2
 4. GCC 4.4.x or later   
 5. CMake 2.8.7 or higher    
 6. Git  
 7. GTK+2.x or higher, including headers (libgtk2.0-dev) 
 8. pkg-config   
 9. Python 3.4.x and Numpy 1.5 or later with developer packages (python-dev, python-numpy)  
 10. ffmpeg or libav development packages: libavcodec-dev, libavformat-dev, libswscale-dev   
 11. [optional] libtbb2 libtbb-dev   
 12. [optional] libdc1394 2.x    
 13. [optional] libjpeg-dev, libpng-dev, libtiff-dev, libjasper-dev, libdc1394-22-dev    

***Installation instructions for Linux (tested for Ubuntu 14.04.1 LTS)***     
 1. Install packages required for Open CV install*        
    *[compiler] sudo apt-get install build-essential*       
    *[required] sudo apt-get install cmake git libgtk2.0-dev pkg-config libavcodec-dev libavformat-dev libswscale-dev*  
    *[optional] sudo apt-get install python-dev python-numpy libtbb2 libtbb-dev libjpeg-dev libpng-dev libtiff-dev libjasper-dev libdc1394-22-dev*     

 2. Download latest stable open CV version from https://sourceforge.net/projects/opencvlibrary/ 
 3. Launch Git client and clone Open CV repository
    *cd ~/<my_working _directory>*  
    *git clone https://github.com/Itseez/opencv.git*    
 3. Build Open CV from source
    *cd ~/opencv*   
    *mkdir release* 
    *cd release*    
    *cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local ..*   
    *make*  
    *sudo make install*     
 4. Download Qt on Ubuntu       
   *wget http://download.qt.io/official_releases/qt/5.0/5.0.2/qt-linux-opensource-5.0.2-x86-offline.run*  
 5. Install and adjust permission    
   *chmod +x qt-linux-opensource-5.0.2-x86-offline.run*   
   *./qt-linux-opensource-5.0.2-x86-offline.run*  
 6. Install g++    
   *sudo apt-get install build-essential* 
 7. Install OpenGL libraries 
   *sudo apt-get install mesa-common-dev*  
   *sudo apt-get install libglu1-mesa-dev -y*     
 8. Set file association with pro files    
   Create a file named “Qt-Creator.desktop”, including the following code, and place it in home/usr/share/applications: 
    
   *[Desktop Entry]*  
   *Version=1.0*  
   *Encoding=UTF-8*   
   *Type=Application* 
   *Name=QtCreator*   
   *Comment=QtCreator*    
   *NoDsiplay=true*   
   *Exec=(Install folder of QT)/Tools/QtCreator/bin/qtcreator %f* 
   *Icon=(Install folder of QT)/5.4/Src/qtdoc/doc/images/landing/icon_QtCreator_78x78px.png*  
   *Name[en_US]=Qt-Creator*     
   
   Edit a file named “defaults.list” in the same directory by adding the following line:    
   *text/qtcreator=Qt-Creator.desktop;*   

   Open file mimeapps.list and add the following line, if it is not present:    
   *application/vnd.nokia.qt.qmakeprofile=qtcreator.desktop*  

   Run the following command:   
   *sudo update-mime-database /usr/share/mime*

 9. Install pyQt5        
   *sudo apt-get install python3-pyqt5*

***Required packages for Mac OS X (tested for Mac OS X 11.11.4)***   

1. Open CV 3.0.0 
2. Qt 5.0.2  
3. PyQt 5.4.2
4. GCC 4.4.x or later   
5. CMake 2.8.7 or later    
6. Git  
7. GTK+2.x or higher, including headers (libgtk2.0-dev) 
8. pkg-config   
9. Python 3.4.x and Numpy 1.5 or later with developer packages (python-dev, python-numpy)  
10. ffmpeg or libav development packages: libavcodec-dev, libavformat-dev, libswscale-dev   
11. [optional] libtbb2 libtbb-dev   
12. [optional] libdc1394 2.x    
13. [optional] libjpeg-dev, libpng-dev, libtiff-dev, libjasper-dev, libdc1394-22-dev 
14. An IDE of choice (e.g. XCode 7.2 or later)  

***Installation instructions for Mac OS X (tested for Mac OS X 11.11.4)***  


***Required packages for Microsot Windows installs (tested for Microsoft Windows 10)***  

1. Open CV 3.1.0   
2. Qt 5.6.0   
3. PyQt 5.6   
4. CMake 3.6.0 or higher    
5. Git for Windows 2.9.0
6. TortoiseGit 2.1.0.0
7. Python 3.4.x and Numpy 1.5 or later with developer packages (python-dev, python-numpy)  
8. Intel Threading Building Blocks (TBB)
9. Intel Integrated Performance Primitives (IPP)  	
10. Intel IPP Asynchronous C/C++
11. Eigen
12. CUDA Toolkit
13. OpenEXR
14. OpenNI Framework
15. Miktex
16. Sphinx
17. An IDE of choice (e.g. Visual Studio 14.0.25123.00 Update 2)

***Installation instructions (tested for Microsoft Windows 10)***  
The instructions to install Open CV 3.1.0 can be found here:     (http://docs.opencv.org/3.1.0/d3/d52/tutorial_windows_install.html#gsc.tab=0) and are summarized below:         
 1. Download Open CV 3.1.0 from http://opencv.org/downloads.html    
 2. Set the Open CV environment variable to the directory where you have the Open CV binaries and add it to the systems path. You may have different platforms or compiler types, so replace the names as appropriate    
  *setx -m OPENCV_DIR D:\opencv\build\x64\vc14*  
 3. Go to Control Panel\System Properties\Environment Variables and set a new system variable to the bin folder of Open CV:    
  *%OPENCV_DIR%\bin*   
 4. Download and install a working IDS with a valid compiler (e.g. Visual Studio 14.0.25123.00 Update 2)      
 5. Install CMake, Git and TortoiseGit         
 6. Download and install the Python libraries, Sphinx, Numpy, Miktex, TBB, Intel IPP Asynchronous C/C++, Eigen, Open EXR 
 7. Install the development build and the PrimeSensor Module for OpenNI Framework    
 8. Install the CUDA Toolkit and the CUDA Tools SDK with a "complete" option     
 9. Download the source files for the Qt framework to build the binary files         
 10. Use the Visual Studio COmmand Prompt to locate the  folder containing the Install and Make files    
 11. Enter the following commands:    
   *configure.exe -release -no-webkit -no-phonon -no-phonon-backend -no-script -no-scripttools -no-qt3support -no-multimedia -no-ltcg* *nmake*     
   *setx -m QTDIR D:/OpenCV/dep/qt/qt-everywhere-opensource-src-4.7.3*      
 12. Use the Path Editor to add the built binary files path to the system path   
 13. Start the CMake GUI and press COnfigure      
 14. Select the parts of Open CV that need to be built (i.e. BUILD_DOCS, BUILD_EXAMPLES, BUILD_PACKAGE, BUILD_SHARED_LIBS, BUILD_TESTS, BUILD_PERF_TESTS, BUILD_opencv_python)  
 15. Press "Configure"   
 16. Set the OpenCV enviroment variable and add it to the systems path   
   *setx -m OPENCV_DIR D:\OpenCV\Build\x64\vc14     (for Visual Studio 2015 - 64 bit Windows)*      
 17. In the Path Editor, set:      
   *%OPENCV_DIR%\bin*       
 18. Save it to the registry


**GUI DESCRIPTION**     
 ***Load Video*** = Load video file for grooming analysis (.AVI, .MOV, .MPEG, .MP4, .SEQ, .TIFF)     
 ***Save Path*** = Set the path to the directory where you want to save the output files. M-Track exits if no directory is selected                
 ***Start CAM*** = Start Continuously Adaptive Meanshift algorithm       
 ***Exit*** = Close M-Track GUI      
 ***Draw Cage*** = Draw the perimeter of the bounding box in which you want M-track to perform the tracking analysis   
 ***Draw LF ROIs*** = Draw the perimeter of the box representing the region of interest (ROI) where M-Track tracks the position of the left foot, for each mouse being analyzed      
 ***Draw RF ROIs*** = Draw the perimeter of the box representing the ROI for the right foot, for each mouse being analyzed. To draw the right foot ROI, click the left mouse button on one corner or the ROI, drag the mouse and release the left button once the ROI has the desired size.   
 ***Detect Mice*** = Allows the user to set the HSV mask to detect the mouse body     
 ***Detect LF*** = Allows the user to set the HSV mask to detect the mouse left foot        
 ***Detect RF*** = Allows the user to set the HSV mask to detect the mouse right foot       
    ***# Mice*** = Number of mice to be tracked (1, 2, 4)         
 ***Execute*** = Start the analysis   
 ***Pause*** = Pause the analysis     
 ***Viewing Mode*** = Allows the user to view the video in its acquisition format (Original), in the HSV color space (HSV) or in three distinct mask modes that allow the user to set the upper and lower limits to detect the body (Body Color Mask), left foot  (Left Foot Color Mask) and right foot (Right Foot Color Mask)       
 ***L Hue*** = Sets the lower limit for hue       
 ***L Sat*** = Sets the lower limit for saturation       
 ***L Val*** = Sets the lower limit for value       
 ***U Hue*** = Sets the upper limit for hue       
 ***U Sat*** = Sets the upper limit for saturation       
 ***U Val*** = Sets the upper limit for value       
 ***Dilation*** = Enlarges the size of the body and feet color masks        
 ***Min Box Size*** = Minimum number of pixels contained in the left/right foot ROI    
 ***Collision Detect*** = This option allows M-track to detect only one body color mask per mouse        
 ***Noise Reduction*** = Removes noise in the image by using a non-local means denoising algorithm, using the selected denoise value     
 ***Denoise Val*** = Regulates the strength of the noise reduction  
 ***Zoom*** = Zoom within the cage area     

**VIDEO ANALYSIS INSTRUCTIONS**         
 1.  Press ***Load Video*** to upload the video file to be analyzed. M-Track analyzes 8-bit .AVI, .MOV, .MPEG, .MP4, .SEQ, .TIFF video files          
 2.  Press ***Save Path*** to select the directory where M-Track saves the output data. By default, M-Track saves the output file in the same folder containing the video file to be analyzed    
 3.  Press ***# Mice*** to select the number of mice to be analyzed (1, 2, 4)      
 4.  Press ***Draw Cage*** to draw the perimeter of the enclosure where M-Track performs the tracking analysis. If the analysis is  performed on only one mouse, M-Track expects the perimeter of the enclosure to be shaped as a box. This box is drawn with three consecutive click-and-release steps using the left button of the computer mouse. If the analysis is  performed on more than one mouse (i.e. 2 or 4), M-Track allows the user to first draw the perimeter of the bounding box as described above. Next, a pop-up message requests the user to ***Now draw a line for each dividing wall***. Only one line needs to be drawn when analyzing two mice, whereas two lines need to be drawn when analyzing four mice. The lines are drawn by clicking and dragging the left mouse button.    
 5.  Press ***Draw LF ROIs*** to draw a box representing the ROI where M-Track tracks the position of the left foot. To draw the left foot ROI, click the left mouse button on one corner or the ROI, drag the mouse and release the left button once the ROI has the desired size.   
 6.   Press ***Draw RF ROIs*** to draw a box representing the ROI where M-Track tracks the position of the right foot. To draw the right foot ROI, click the left mouse button on one corner or the ROI, drag the mouse and release the left button once the ROI has the desired size.   
 7.   In ***Viewing Mode***, select the option ***Body Color Mask*** and set the upper (U) and lower (L) limits for the HSV settings to isolate the mouse body area from that of the recording enclosure. The ***Dilation*** button allows to enlarge the area of the Body Color Mask. The ***Min Box Size*** can be used to set a lower threshold for the number of pixels within the Body Color Mask ROI. This is useful to reduce tracking errors when other pixels, in the enclosure, have the same HSV settings as the fur.     
 8.  In ***Viewing Mode***, select the option ***LF Color Mask*** and set the upper (U) and lower (L) limits for the HSV settings to isolate the left foot area. The ***Dilation*** button allows to enlarge the selected foot area. The ***Min Box Size*** can be used to set a lower threshold to the number of pixels within the left foot ROI. This is useful to reduce tracking errors when other pixels, in the enclosure, have the same HSV settings as the left foot.  
 9.  In ***Viewing Mode***, select the option ***RF Color Mask*** and set the upper (U) and lower (L) limits for the HSV settings to isolate the right foot area. The ***Dilation*** button allows to enlarge the selected foot area. The ***Min Box Size*** can be used to set a lower threshold to the number of pixels within the right foot ROI. This is useful to reduce tracking errors when other pixels, in the enclosure, have the same HSV settings as the right foot.  
 10.  In ***Viewing Mode***, select the option ***Original***. Press ***Detect Mouse***, ***Detect LF***, ***Detect RF*** to check that all HSV settings are optimally tailored for accurate grooming analysis by tracking the position of the mouse body, left and right foot, respectively.     
 11.  As a final step, press ***Execute*** to run the M-Track analysis and ***Pause*** to pause the M-track analysis and reset the detection parameters if needed.     
 12.  The ***Start CAM*** option allows the user to initiate the Continuously Adaptive Meanshift algorithm, through which M-Track rotates and rescales the LF and RF ROIs to locate the position of the mice LFs and RFs.  
 13.  Press ***Exit*** to close M-Track

