from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from gpt_prompt import Story
import logging

# set up logging
logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app, origins=[
   'http://localhost:3000', 
   'http://localhost:8000'
  ])

@app.route('/', methods=["GET"])
def verify_connection():
  response = jsonify({"msg": "Connected!"})
  return response, 200

@app.route('/test-foo', methods=["POST"])
@cross_origin()
def create_playlist():
    data = request.get_json()
    test = data.get('test')  # Get blendLink from request

    if test is not None:
        logging.info(test)
        #response = jsonify({'playlistID': playlistID}) # Return playlist ID as a response
        return test, 200
    else:
        # TODO: implement better error handling with correct http response
        raise ValueError 


@app.route('/generate-book', methods=["POST"])
@cross_origin()
def get_grovy_events():
  #Skipping validation for now
  logging.info('In generate book')
  data = request.get_json()

  # Extracting values from the data received
  age = data.get('age')
  lesson = data.get('lesson')
  topic = data.get('topic')
  hero = data.get('hero')
  characteristics = data.get('characteristics')

  if age and lesson and topic and hero and characteristics:
      logging.info(f'Form Passed successfully : {data}')
  else:
      # TODO implement validation and return message if incorrect
      logging.info('Skipping validation for now')

  try:
      logging.info('Returning response')
      logging.info(data)

      # Creating the story object using the extracted values
      story_description = f"{hero} with {characteristics} characteristics"
      story = Story(
          child_age=int(age.split(' ')[0]),  # Extracting the age number from the age string
          hero_description=story_description,
          story_topic=topic,
          image_composition=f"{lesson} lesson, {topic} story"
      )
      story_1 = story.add_story_prompt("Story Title: Adventure of the Little Hero")
      return jsonify({'response': story_1}), 200
  except Exception as e:
      logging.error(f"Error occurred: {e}")
      return jsonify({'error': 'An error occurred while generating the story'}), 500


if __name__ == '__main__':
  app.run(debug=True, port=4000)
