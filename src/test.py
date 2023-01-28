from pytube import Playlist

p = Playlist('https://www.youtube.com/watch?v=6yCIDkFI7ew&list=PLTfzGEQsw7fWPaQF0jG8HC8rR2YrQnUt3')
try:
    print(len(p))
except:
    print('Entered URL is not a playlist')