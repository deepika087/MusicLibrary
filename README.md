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
- Update only adds the songs to the playlist. 
- No functionality will just remove the songs from the playlist. We can delete playlist and create a new one though. 

# Validations
- The user who initally stated the playlist is trying to add, update or delete the playlist. 
- If the user just passes the name of the files. "json" extension is atuomatically added to the file name
- The input arguments should be of the form -i -c -o
- Can't add the playlist you already are the owner of, however you can update that Playlist. 
- Any operation other than Add, Delete, Update will be shown to the user as an error message. 

# Improvements
- AI based changes.json. Say, the user doesn't specify the operation. The code figures out the operation to be performed. For instance, if the user inputs a valid playlist id and no songs. Then this operation will be taken as an attempt to delete the Playlist. 
- If the user, tries to add/update playlist with unknown song. Then the user is prompted to provide song information rather than rejecting that change. 
- Better handling aroudn if the files are empty. Say, the user passes a valid path and the file is empty. May be copy the default data to that file to keep the system running. The motivation here to minimize the errors seen.
- As of now, the system uses strings such as Add, Delete, Update to identify thetye of action. It could be replaced with enum kind of structure so that one change in a string here or there doesn't break the entire pipeline

# How to run the code. 
The code has minimal dependencies. 

The user can give the input such as 
python LibraryController.py -i data/mixtape-data -c data/changes -o output
Your output has been saved in output.json

In this case .json is automatically appended to the file names or the user can also pass the command line argument such as
python LibraryController.py -i data/mixtape-data.json -c data/changes.json -o output.json 

To see help 
python LibraryController.py -h
LibraryController.py -i <inputfile> -c <changesfile> -o <outputfile>
  
or if the user passes invalid or unknown the same help will be printed. 

# Data structure Used
The Library makes heavy use of serialization and deserialization concepts to read the data via JSON and output the JSON data. 
All the objects used can be found in MixTape.json

```
class MixTape:

    def __init__(self, users, pl, songs):
        self.users = users
        self.playlists = pl
        self.songs = songs
```
Each Users, Playlist, songs are List of objects in it self

#Design choice for changes.json
The way I have modelled changes.json is such that each change consists of the user (actor), playlist(model), type(action), songs(metadata). There are other ways to model also, for example I could have chosen for type, metadata where metadata contains the user, playlist, songs. 
Other way to model could have been. All types grouped together, for instance. Json consists of 3 high level list. Each list corresponds to ADd, delete, update respectively. Then each of this list would just contain user, playlist, songs(not applicable for delete case).

# Scalability challenges
Now, this system is not built in a way to be taken to production. In order to take this production there are a number of steps we need to do. A few of them might be
- Exposing the functionality via the REST APIs
- Have a data plane to save the data in hard disk against in-memory operations as of now. 
- Extensive logging
- A unique guid to identify each request
- Metric analysis, dashboards,
- Capture the avergae time taken to respond + 99 percentile of time taken to serve the requests

If there were a system where we had a large mixtape-data.json. In other words, we have the large dataset and large number of changes are coming on top of it. 
To ingest the data
  - I would suggest use json streaming capability to save the data to persistent store. Assuming the same data model, it is a good candidate for SQL kind of storage as we have a fixed data model.
  - Or if we don't want to go with standard json, we could even use normal string parser to break the file into 3 components namely, playlist, songs, user and different machine read each of these Lists and save them in separate DB. 

If if TB of data. We definietly want think in terms of sharding and maintaining replication copies of the data. We can split the playlists data into multiple shards. For instance, We can maintain the mappings that playlist 1 to 100000 are in Data center 1. We will need a partition manager which will not only maintain the sharded info but will also be reponsible to gather heartbeat from the distributed sections and spawn up new nodes if the old ones fail. 

To handle way to many changes. Say, changes.json is way too big
  - One approach will be to using a messaging queue as the order of the updates is important. We can't afford to jumble up the changes say user adds a song to the playlist and then delete the playlist. But if we reverse the order we will first delte the playlist and then add songs to the playlist. 
  -  Say the changes are producers and consumers will be worker node. Each of these nodes will pick a change from change queues and do the respective action on the data model. I would go for a row level lock such that if I am updating a playlist no other thread should update that playlist. 
  -  May be to make the system further intelligent, we can even squish the changes. for instance, update playlist 1 with songs [201, 301] can be combined with update playlist 1 with songs [202, 402] such that we have one change request update playlist 1 with updates [201, 301, 202, 402]
  -  This will reduce the number of operations on the playlist.
