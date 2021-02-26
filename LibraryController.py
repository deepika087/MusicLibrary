__author__ = 'deepika'

import simplejson as json
import jsonpickle

import MixTape
from MixTape import PlayLists
import sys, getopt



def addExtension(arg):
    if not arg.endswith(".json"):
        arg += ".json"
    return arg

def processArguments(argv):
    raw_file_path = "data/mixtape-data.json"
    raw_file_path_to_changes = "data/changes.json"
    output_file_path = 'output.json'

    try:
        opts, args = getopt.getopt(argv,"i:c:o:", ["input=", "changes=", "output="])

    except getopt.GetoptError:
        print('LibraryController.py -i <inputfile> -c <changesfile> -o <outputfile>')
        sys.exit(2)

    for opt, arg in opts:
        if opt == '-h':
            print('LibraryController.py -i <inputfile.json> -c <changesfile.json> -o <outputfile.json>')
            sys.exit()
        elif opt in ("-i", "--input"):
            raw_file_path = addExtension(arg)
        elif opt in ("-o", "--output"):
            output_file_path = addExtension(arg)
        elif opt in ("-c", "--changes"):
            raw_file_path_to_changes = addExtension(arg)

    return raw_file_path, raw_file_path_to_changes, output_file_path

class LibraryController(object):

    def __init__(self):

        self.Users = None
        self.PlayLists = None
        self.Songs = None

        self.__raw_data__ = None
        self.__deserializer__ = MixTape.CustomDeserializer()
        self.__basicChangeHandler__ = MixTape.BasicChangeHandler()
        self.__changes__ = None

    def read(self, raw_file_path):

        with open(raw_file_path, "r") as read_file:
            self.__raw_data__ = json.load(read_file)

    def deserialize(self):

        if self.__raw_data__ != None:
            self.Users, self.PlayLists, self.Songs = self.__deserializer__.deserialise(self.__raw_data__)

    def loadChanges(self, file_path):
        with open(file_path, "r") as read_file:
            self.__raw_data__ = json.load(read_file)

        self.__changes__ = self.__basicChangeHandler__.classifyChanges(self.__raw_data__)

    def validateSongCollection(self, song_ids):

        if len(song_ids) < 1:
            return False

        for song in song_ids:
            if len(filter(lambda x: x.id == song, self.Songs)) > 0:
                continue
            else:
                return False
        return True


    def applyChanges(self):

        for change in self.__changes__:
            filtered_result = list(filter(lambda x: x.id == change.playlist_id and x.user_id == change.user_id, self.PlayLists))
            if change.type == "Delete":
                if len(filtered_result) == 1:
                    self.PlayLists.remove(filtered_result[0])
                else:
                    print("Delete request to delete playlist: " + str(change.playlist_id) + " is not processed. Make sure to check that you passed the correct user id")
            else:
                if not self.validateSongCollection(change.song_ids):
                    print("You are either passing no songs in your Playlist " + str(change.playlist_id) + " or your playlist is trying to add the songs that are not supported by us. ")

                if change.type == "Add":
                    if len(filtered_result) == 0:
                        self.PlayLists.append(PlayLists(change.playlist_id, change.user_id, change.song_ids))
                    else:
                        print("Can't add playlist: " + str(change.playlist_id) + " as you already have it in your collection. Please try to update the playlist!" )
                elif change.type == "Update":
                    if len(filtered_result) == 0:
                        print("You are trying to update a Playlist " + str(change.playlist_id) + " that doesn't exist or you are not the owner of this playlist")
                    else:
                        update_index = self.PlayLists.index(filtered_result[0])

                        for song in change.song_ids:
                            if song not in self.PlayLists[update_index].song_ids:
                                self.PlayLists[update_index].song_ids.append(song)
                        break
                else:
                    print("The operation type: " + change.type + " is not supported!")

    def generateOutput(self, output_file_path):
        mx = MixTape.MixTape(self.Users, self.PlayLists, self.Songs)
        with open(output_file_path, 'w+') as f:
            f.write(jsonpickle.encode(mx, unpicklable=False))

        print("Your output has been saved in " + output_file_path)

if __name__ == "__main__":

    raw_file_path, raw_file_path_to_changes, output_file_path = processArguments(sys.argv[1:])
    controller = LibraryController()
    controller.read(raw_file_path)
    controller.deserialize()

    controller.loadChanges(raw_file_path_to_changes)
    controller.applyChanges()
    controller.generateOutput(output_file_path)


