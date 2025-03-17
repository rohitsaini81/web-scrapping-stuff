from create import *
from flask import Flask, request, jsonify
app = Flask(__name__)


data = read_videos()
if data:
    for row in data:
        print(f"ID: {row[0]}, Title: {row[1]}, Video URL: {row[3]}")


@app.route("/")
def getAll():
    data = read_videos()
    if data:
        return data
    else:
        return "<p>Hello, World!</p>"


@app.route("/search", methods=["POST"])
def findSearch():
    try:
        data = request.json  # Get JSON data from request body

        if not data:
            # Handle empty body
            return jsonify({"error": "No data provided"}), 400

        title = data.get("title")
        tags = data.get("tags")
        keywords = data.get("keywords")

        print(
            f"Received Data - Title: {title}, Tags: {tags}, Keywords: {keywords}")

        # Perform database search (replace this with your function)
        result = find_video(title=title, tags=tags, keywords=keywords)

        if result:
            return jsonify(result), 200  # Return found videos
        else:
            return jsonify({"message": "No matching videos found"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Handle errors


@app.route("/video/<int:video_id>", methods=["GET"])
def find(video_id):
    print(f"Received Video ID: {video_id}")

    data = find_one(video_id)  # Call the function to fetch video

    if data:
        return jsonify({"success": True, "video": data}), 200
    else:
        return jsonify({"success": False, "error": "Video not found"}), 404




    app.run(host="0.0.0.0", port=5000)
