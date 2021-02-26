# MusicLibrary

This is the Library that can handle the batc inputs to make changes in the PlayList. 

# System Requirements. 
- Python 2.7+
- Libraries: simplejson, jsonpickle

# Assumption
- Only the user who created the PlayList can there by update, add or delete the playlist. Other users won't be authorized to do so. 
- Only the songs that are first present in mixtape-data.json can there by be added the unknown songs can not be added. 
- The user won't get any error if they try to add the song that already exists in their Playlist. 
- We are only dealing with JSON files

# Validations
- The user who initally stated the playlist is trying to add, update or delete the playlist. 
- If the user just passes the name of the files. "json" extension is atuomatically added to the file name
- The input arguments should be of the form -i -c -o
- Can't add the playlist you already are the owner of, however you can update that Playlist. 
- Any operation other than Add, Delete, Update will be shown to the user as an error message. 

# Improvements
- AI based changes.json. Say, the user doesn't specify the operation. The code figures out the operation to be performed. For instance, if the user inputs a valid playlist id and no songs. Then this operation will be taken as an attempt to delete the Playlist. 
- If the user, tries to add/update playlist with unknown song. Then the user is prompted to provide song information rather than rejecting that change. 
