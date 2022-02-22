#ClimatePrisms

##Intoduction

In order to present an interesting, interactive experience with a set of content about some subject matter, users should be able to interact with the content, navigating the content in a path reflecting their interest.  Rather than being constrained to a fixed path through the content designed by a curator, the user should be able to express their interest in particular items from the content, then be able to a) dive deeper into that sub-subject matter and b) be presented with related content that he might also be interested in.   

ClimatePrisms is a framework that allows content data to be organized for such exploration and then provide an interface for the interactive experience of the content.   

##Experience

Using ClimatePrisms, a user is initially presented with an introductory image with buttons for different *themes*, and witin each theme, *stories*.  Themes are effectively sub-subjects of the overall material that address a particular aspect of the material, while stories are curated subsets of theme contents.   The user selects a theme or a story, and a new page is presented with content from that story line - a page continaing five or so content items tiling the frame.  The user can then select any of these items for further exploration; when a content item is selected, a new set of related content is chosen and a new page is created with the selected item taking a predominant position in the frame, along with loosely related content.  The user can then select the predominant content to do a deeper dive into that subject matter, or select a neighboring item to change direction in their exploration of the story line.

Content items are images or movies.   Movies are not initally run; the user is presented an initial frame with a 'run' button that expands the content to fill the screen and run as a movie.  Other content - particularly images with fine detail not easily visible in a small portion of the screen - includes an 'expand-me' button that causes the content to fill the screen for a better look.   Many of the content items will have a short description included; an icon allows the user to see this as a popup.   At any time a 'home' button is available to return to the initial frame and allow the user to select a new story line.   This will automatically occur after some period of idleness.

##Content

ClimatePrisms depends on a body of *content* - a potentially large set of images and movies, and a *database*, containing the interrelationships of the content items.  

Content is simply a directory containing all the images and videos that are present.  

The database is a Mongo DB that can be queried by primary attributes (story line, level within that story line) and other characteristics enabling the choice of material that will mesh well aesthetically with other selected content.   Finally, each database entry contains a pointer to the actual content - a file in the content directory.

For reasons of convenience, the database is externally represented by one or more Excel spreadsheets.  At system initialization time, these are read and inserted into the Mongo DB.  The first row of each of these spreadsheets contains the attribute names; the remainder contain the corresponding attribute values for each item of content.

##System Architecture

Ultimately, ClimatePrisms consists of two functional components:

+ Web Service.  The web service that a) serves static content and b) presents a restful API that processes requests for content from the web page.  Currently, the web service consists of a simple Python Web server, enabling easy implementation of API functions and easy access to the Mongo DB.

+ Web Page.  A dynamic web page that runs in a local browser to present the ClimatePrisms user interface.   Based on the user's actions, the web page queries the web server to identify new content, then modifies itself to present the new content.

##Fillers

In order to format a page containing multiple client items without clipping them or distorting their aspect ratios, a set of *filler* images is reqired.   These images are *intended* to be clipped and scaled to fill any remaining space after the content items have been placed.   These are held in _content/fillers_.

#Project Directory

To set up a ClimatePrisms instance, the user provides several items in one input *project directory*:

### A *setup.json* file 

The setup.json file contains the information necessary to create the initial webpage.   This file contains the title of the project, the contents of the homepage title section, and the theme/story structure of the data.

The setup.json file consists of a JSON dictionary containing a title for the project, strings for the initial page, and an array of *themes*. The themes correpond to the columns of options on the homepage.   Each theme has a title, an introductory videp, a tag, and an array of *stories*. Each story has a title, an introductory video and a tag.
	
### One or more Excel xlsx files *describing* the instance content.   

The first row in an xlsx file contains column titles.   

* **include** a flag that should be
* **folder**  where, relative to the project *static/content* directory where the primary content resides
* **filename** the filename in the aforementioned folder
* **theme** the theme that the content pertains to
* **story** the story within the aforementioned theme that the content pertains to
* **text** 1 if the content includes text; 0 otherwise
* **provenance** where the content came for, if available
* **enlarge_image** whether the content can/should be enlarged in the displat
* **content** If the content has a backing video, the file containing the video
* **caption** a caption for the image

### A *static* directory

The static directory contains static data used by the project.   One vital subdirectory of *static* is *content*, which (perhaps needless to say) is the actual content.  The content directory should contain subdirectories and files as per the folder and filename fields of the **xlsx** files, as well as a video file named **attract_video.mp4** which will be shown when the system is idle, and a **fillers** directory containing images that can be cropped to fill gaps in the layouts.

#Docker

The ClimatePrisms server is presented as a Docker image.   There are two ways this image can be created; one in which hich the content is bundled into the image, and one in which the content is linked to the image at run time.   The Dockerfile is set up for the latter form; commented-out code in there show how the content can be embedded.

The simplest method of running the ClimatePrisms server is to attach the content to the server at run time.  This can be done by using **docker://gregabram/cp-ext**.

If you want to build a bundled ClimatePrisms image, you will need to clone the ClimatePrisms source from GitHub, modify the Dockerfile in the root directory and run: 

	docker build -it {imagename} .
	
You can push this image to DockerHub if you wish, enabling users to access a fully bundled image.

#Running Climate Prisms Server


The ClimatePrisms server is run by a Docker command line:

	docker run -p 127.0.0.1:{host port}:1337/tcp -id {docker image}
	
where:

* {host port} is the port to attach the browser to on the host - I use 1337.
* {docker image} may be docker::gregabram/cp-ext for a pre-built image that one attaches content to, or a locally-built image that contains bundled content. 
	
If content is to be attached to the server at run time, the content is attached using Docker's **-v** flag:

	docker run -p 127.0.0.1:{host port}:1337/tcp -v {directory}:/ClimatePrisms.Content -id {docker image}

where:

* {directory} is the fully qualified path name of the content on the host

TO discover whether there is a ClimatePrisms container running:

	docker container ls
	
If a container is running, it can be stopped and removed:

	docker stop {container ID}
	docker rm {container ID}

where {container ID} is the ID from the previous step.

The ClimatePrisms source root directory contains example scripts to start and stop the server container.

#Running Climate Prisms

Once the ClimatePrisms server is running, start a browser on the host desktop and point it at: **localhost:{port}/static/index.html**  where {port} is the port number specified when starting the server.