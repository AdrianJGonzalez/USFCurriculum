**Project Overview**:
  The curriculum is designed using Python 3.10.11 to assist students, particularly those in engineering programs at USF, in planning their academic curriculum. The application provide a visual interface to create a semester by semester courses flowchart, track completed courses from transcript, explore different tracks and department advising. This application uses a combination of GUI libraries and PDF processing libraries. It is designed to be more user-friendly and visually appealing compared to the current curriculum. Key features of the program will include:
   1. **Transcript Parsing** - Allow user to upload transcript, then will process to extract completed course related to major and display them in the flowchart.
   2. **Flowchart** - Create a visual flowchart of completed courses through semester and allow user to plan for upcoming semester with ability to add, remove, and view course details.
   3. **Track Selection** - Able to choose different electrical engineering track to guide course planning
   4. **Advising Information** - Access deparment-specific advising pages for information.
   5. **Course Management** - User are able to manage course data like pre-req or coreq through visual interface.
   6. **Course Information Display** - Able to view all courses' information including description of the course, pre-req, coreq and credit hours

**Libraries**:
  These are the libraries that are necesssary for the application of our program:
  
    1. pygame - Provide the main graphical interface for the application
                Installation: 
                **Thonny** - Tool > Manage Package > search pygame > install

    2. pymupdf - Read and extract text from PDF file
                Installation: 
                **Thonny** - Tool > Manage Package > search pymupdf > install

    3. Pillow - Used to load, resize and display the background image
                Installation - should automatically included in thonny but if not can use 
                      Tool > Manage Package > search pillow > install
                      
    4. tkinter - Provide GUI components for file dialogs 
                Installtion - Included in thonny 

    5. json - Used to save text data, similar to text file but in json format which is easier to implement into the program
              Installation - Included in thonny 

    6. re - Used for regular expression matching to extract courses from transcript
            Installation - included in thonny 

    7. os - Used to interact with the operating system
            Installation - included in thonny 

    8. importlib - Used to dynamically import depatmnet-specific advising 
                    Installation - included in thonny 

    9. sys - Handle system specific parameters and exit the application when the user closes the window.
              Installation - inclued in thonny 

    10. pygame.locals - Provide constant for event handling in pygame interface 
              Installation - included in pygame libraries 

    11. PYPDF2 - Used to extract content from PDF files 
              Installation 
              **Thonny** - Tool > Manage Package > search pypdf2 > install
    12. webbrowser - Provides a high-level interface to open web pages in the user's default web browser
              Installation - included in thonny 

**What's Left**:
1. Adding Prereq and Coreq arrows into the flowchart
2. Making the transcipt courses go into the flowchart.
3. Add the Advising Department selection feature into the FAQ for department specfic FAQ sections
4. Make the Welcome page more general and not EE focus. Figure out what to put there.
5. Make the About this program be more general and remove the EE stuff.
6. Make the program look visually better and add more ease of access.
7. Add the Admin tools to add, delete, and modify courses in the courses.pygame
8. Add the feature to save the flowchart for later and so that an advisor can easly open it up.
9. Add IOS/Andriod Support maybe even make it a website.
