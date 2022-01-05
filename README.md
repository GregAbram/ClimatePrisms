#ClimatePrisms

##Intoduction

In order to present an interesting, interactive experience with a set of content about some subject matter, users should be able to interact with the content, navigating the content in a path reflecting their interest.  	Rather than being presented a fixed path through the content designed by a curator, the user should be able to express their interest in particular items from the content, then be able to a) dive deeper into that sub-subject matter and b) be presented with related content that he might also be interested in.   

ClimatePrisms is a framework that allows content data to be organized for such exploration and then provide an interface for the interactive experience of the content.   

##Experience

Using ClimatePrisms, a user is initially presented with an introductory image with buttons for different *stories*.  Stories are effectively sub-subjects of the overall material that address a particular aspect of the material.   The user selects a story, and a new page is presented with content from that story line - a page continaing five or so content items tiling the frame.  The user can then select any of these items for further exploration; when a content item is selected, a new set of related content is chosen and a new page is created with the selected item taking a predominant position in the frame, along with loosely related content.  The user can then select the predominant content to do a deeper dive into that subject matter, or select a neighboring item to change direction in their exploration of the story line.

Content items are images or movies.   Movies are not initally run; the user is presented an initial frame with a 'run' button that expands the content to fill the screen and run as a movie.  Other content - particularly images with fine detail not easily visible in a small portion of the screen - includes an 'expand-me' button that causes the content to fill the screen for a better look.   Many of the content items will have a short description included; an icon allows the user to see this as a popup.   At any time a 'home' button is available to return to the initial frame and allow the user to select a new story line.   This will automatically occur after some period of idleness.

##Content Data

ClimatePrisms depends on a body of *content* - a potentially large set of images and movies, and a *database*, containing the interrelationships of the content items.  

+ The Database.  The database is a Mongo DB that can be queried by primary attributes (story line, level within that story line) and other characteristics enabling the choice of material that will mesh well aesthetically with other selected content.   Finally, each database entry contains a pointer to the actual content - a file in the content directory.

+ The Content.  A directory containing the content itself.   

For reasons of convenience, the database is externally represented by one or more Excel spreadsheets.  At system initialization time, these are read and inserted into the Mongo DB.  The first row of each of these spreadsheets contains the attribute names; the remainder contain the corresponding attribute values for each item of content.

Content is held in the _content_ directory.   This dirctory should contain four items:

+ DATABASE.  A subdirectory containing the content itself - eg. png's, mpegs...  

##System Architecture

Ultimately, ClimatePrisms consists of two functional components:
j
+ Web Service.  The web service that serves static content and presents a restful API that processes requests from the web page.  Currently, the web service consists of a simple Python Web server, enabling easy implementation of API functions and easy access to the Mongo DB.

+ Web Page.  A dynamic web page that runs in a local browser to present the ClimatePrisms user interface.   Based on the user's actions, the web page queries the web server to identify new content, then modifies itself to present the new content.

##Fillers

In order to format a page containing multiple client items without clipping them or distorting their aspect ratios, a set of *filler* images is reqired.   These images are intendended to be clipped to fill any remaining space after the content items have been placed.   These are held in _content/fillers_.
"
##Ports

ClimatePrisms starts mongod on port 1336 an the web server on 1337

##Database Fields

The fields of the DB are attributes of the content items and are input as columns of the input Excel spreadsheet(s).  Values are not necessarily required; those that are indicated by (R).   

**include** (R) A flag indicating whether the item should be considered.   'x' if so.  
**theme** (R) Which of the main story lines this item belongs to.
**category** (R) Which of the sub-stories of the main story this item belongs to.
**level** (R) A list of three-digit numbers for each item.   The first digit is the __theme__; the second the __category__ it belongs to; the third is a simple categorization of the data.  In the current DB, an '8' connotes that it contains a scientist.
**text** '1' if contains writtern text; 0 otherwise
+ layout
+ category
+ filename
+ tagmain
+ tagmain2
+ context
+ enlarge_image
+ rollover
+ content
+ area
+ folder
+ crop
+ texture
+ caption
+ width
+ height
+ story
+ content_type
+ keyword





#Running Climate Prisms

