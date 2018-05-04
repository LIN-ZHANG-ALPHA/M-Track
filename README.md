# M-Track
A new software for automated detection of forepaw trajectories in mice.  

**SYNOPSIS AND MOTIVATION**  
M-Track is a new software that allows automated detection of labelled forepaws in freely behaving in mice. M-Track uses color detection and back projection algorithms to locate the position of color-labelled paws in videos of multiple freely-behaving mice. M-Track has an intuitive graphical user interface and provides a new tool to obtain quantitative information on fine aspects of spontaneous grooming behaviors, to improve the current understanding of the functional properties of brain neuronal circuits in biomedical research studies. 

**OVERVIEW**  
 M-Track is an open-source software designed to detect the location of mice and of their labelled forepaws in video files. M-Track is compatible with debian and non-debian Linux installations, Mac OS X and Microsoft Windows operating systems. M-Track uses the Python language and the OpenCV, PyQt and Numpy libraries.  

Two executable standalone versions of M-Track for Linux and Microsoft Windows platforms are currently available: one of them allows the user to visualize the orientation of the mouse body (v1r1), the other does not have this feature (v1r2).  

***Linux:***    
M-Track_LIN_v1r1 - The user can visualize the orientation of the mouse body       
M-Track_LIN_v1r2 - The user cannot visualize the orientation of the mouse body 

***Microsoft Windows***  
M-Track_WIN_v1r1 - The user can visualize the orientation of the mouse body       
M-Track_WIN_v1r2 - The user cannot visualize the orientation of the mouse body 

The ***Sample videos and output files*** folder contains two sample video files, acquired on a C57BL/6 (black fur) and on a Swiss Webster mouse (white fur). Running M-Track on these sample Video files generates output files like the ones included in this folder, named ***Sample_Video_Black_Mice_Output.txt*** and ***Sample_Video_White_Mice_Output.txt***. 

**INSTALLATION FOR VERSIONS v1r1 and v1r2**      
M-Track requires the following languages and libraries:    
- Python 2.7  
- OpenCV 3.0  
- PyQt 4.8  
- Numpy 1.10.4  

**INSTALLATION FOR VERSIONS v2r1 and v2r2**      
M-Track requires the following languages and libraries:    
- Python 2.7  
- OpenCV 3.2  
- PyQt 4.11  
- Numpy 1.13.1  

In addition, M-Track requires the following package files:   
 - MTrack_Qt.py      		
 - MTrack.py           		 
 - RoiLabel.py         		 
 - ColorLabel.py       	   	 
 - InfoDialog.py        		 

Detailed instructions for software installation and video analysis are provided in the ***Installation*** file in the ***Instructions*** folder. All required package files are in the ***Package files*** folder.   

**TESTS**      
To test M-Track, run ***MTrack_Qt.py***, press ***Load*** to visualize one of the two example files in the folder named ***Sample videos and output files***, proceed through the analysis steps described in the ***GUI and analysis*** file in the ***Instructions*** folder and press ***Execute***.

**CONTRIBUTORS**        
M-Track was created by:         
Lin Zhang         (linzhang0529@gmail.com; lzhang22@albany.edu)  
Sheldon L. Reeves (sheldonreeves316@gmail.com; sheldonreeves@icloud.com)  
Matthew S. Brandon   (592mattbran@gmail.com; mbrandon@albany.edu)
Annalisa Scimemi  (scimemia@gmail.com; ascimemi@albany.edu)    
For support and questions, please contact Annalisa Scimemi (scimemia@gmail.com)   
All work was funded by SUNY Albany, SUNY Albany Research Foundation and SUNY STEM Research Passport Program.   

**HISTORY**   
08-2015 - The first version of M-Track was created by Sheldon L. Reeves and Annalisa Scimemi. This version was compatible with Linux platforms and used Python 3.0, OpenCV 3.0 and PyQt 5.4.  

07-2016 - An updated version of M-Track, available from this repository, was developed by Lin Zhang and Annalisa Scimemi using Python 2.7, OpenCV 3.0 and PyQt 4.8. This version of M-Track has added functionalities and fixes and is compatible with Linux, Mac OS X and Microsoft Windows platforms. 

08-2017 - Anaconda1 is no longer available for new users and Anaconda2 requires using OpenCV 3.2. An updated version of M-Track, available from this repository, was developed by Matthew Brandon and Annalisa Scimemi using Python 2.7, OpenCV 3.2 and PyQt 4.11. This version of M-Track allows it to work with OpenCV 3.2.

**LICENSE**     
Please review the terms and conditions of the license in the LICENSE_NPOSL-3.0 section of this repository before downloading the M-Track software. By downloading the M-Track software from this site you agree to be legally bound by the terms and conditions of the Open Source Initiative Non-Profit Open Software License 3.0         
(NPOSL-3.0; https://tldrlegal.com/license/non-profit-open-software-license-3.0-(nposl-3.0)).
