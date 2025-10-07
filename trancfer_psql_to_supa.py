from create import read_videos 
from supa import insert_supa
from time import sleep




video_array = []
video_array = read_videos()
print(video_array[15])



for row in video_array:
    print(row)  # optional debug

    data = [{
        'id': row[0],
        'title': row[1],
        'description': row[2],
        'category': row[3],
        'tags': row[4],  # must match Supabase column type
        'duration': row[5],
        'img_url': row[6],
        'video_url': row[7],
        'image': row[8],
        'video': row[9],
    }]

    response = insert_supa(data)
    print(response)
    sleep(2)  # avoid Supabase rate limits


