from pytube import YouTube

def Download():
    print("Put your YouTube link here:")
    link = input()
    youtubeObject=YouTube(link)
    youtubeObject=youtubeObject.streams.get_highest_resolution()

    try:
        youtubeObject.download(filename = "downloaded")
    except:
        print("There has been an error in downloading this video")

    print("Download Successful!")

# link = input("Put your YouTube link here:")
# Download(link)

# Ask for User Input in Function
# https://stackoverflow.com/questions/12758491/how-to-ask-for-user-input-in-a-function-python-related

# Change FileName
# https://stackoverflow.com/questions/47649536/python-download-youtube-with-specific-filename