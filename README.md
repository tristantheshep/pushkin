### Pushkin ###

Implementation of a survey/questionnaire website back-end/RESTful web service in Django. Born of utter frustration with SurveyGizmo's open-text analysis tagging system and REST API.

### Motivation ###

My friend was tasked with reading and tagging ~18,000 open-text responses to a survey in SurveyGizmo. I undertook this project mainly as a proof of concept, as well as an excuse to practice some Django. The main annoyances they had:

 * SurveyGizmo has no sensible way of managing tags. When browsing responses you (the survey owner) have the option of adding a tag, which can either be typed into a text box or selected from a list of recent tags. As there were ~80 tags in use and only about 10 recent tags were available to select/click, this meant using the text box for the most-part. This makes it *incredibly* easy to screw things up to a nearly irreparable state. What if you make a typo? What if you copy and paste the tag text from a document, and sometimes include a trailing space? Or end up with a mixture of hyphens, n-dashes, and m-dashes? Nothing, until you analyze your data and find that you have 5,000 answers tagged with "Foo" and another 5,000 with "Foo ". And no way of fixing it, short of clicking through all 18,000 responses and manually editing the tags. That is, of course, unless you a) know how to use a REST API and b) have the combined patience of a proper old-school Church of England village vicar, which you will still exhaust trying to figure out how to add tags with a post request. /rant
 * SurveyGizmo has a pretty limited search functionality.
 * The REST API, as mentioned above, is terrible (pretty much everything about it from a useabilitywise)
 * Exporting data is a pain. You can export CSVs and spreadsheets but it takes really quite a long time to do so, and once you have, the data layout doesn't seem to make much sense
 * Several front-end buggy interface problems that I might eventually try and better, if I get around to adding a front end.

 Most of the above can be easily solved with a simple and clean REST API and database, which is what I wish to achieve here.

### Django Details ###

 * Django 1.8.5
 * Underpinned by a neat REST API (using djangorestframework 3.3.2)

### Roadmap ###

Short term:

 * Add ability to query answers for each tag (/surveys/1/tags/1/questions)

Long term:

 * Add questions that allow responses other than open text (choices, x/10, ordering)
 * Friendly front end

### The API ###

The query paths are as simple as :

	/surveys/                                - the list of surveys for an authenticated user.
	         <id>/                           - the survey for a particular id (unique across all surveys)
	              tags/                      - the list of tags for the survey
	              questions/                 - the list of questions in the survey
	                        <N>/             - the Nth question in that survey
	              responses/                 - the list of responses
	                        <N>/             - the Nth response
	                            answers/     - the answers in the Nth response
	                                    <M>/ - the answer to the Nth question in the Mth response

The usual set of requests are available on each path (get/post on lists, get/put/delete on objects) with a few specifics:

  * The survey owner is pretty much the only person that can read or write anything, except for responses.
  * answers/ only supports GET. Answers are added automatically when posting on responses/, populated by an `answer_strings` field.
  * A survey has to be in the published state before responses can be created, after which the survey questions cannot be modified. A survey cannot be unpublished.
  * Note that the default Django behavior for object access in views is to use the PK. We only key off of PK in the survey case - after than, we use an ordinal number i.e. /surveys/1/questions/4 gives you the 4th question for survey 1.

#### Example useage ####

Adding a response to a survey

    POST /surveys/<id>/responses {'answer_strings':['answer1', 'answer2']}

Getting the response (assuming it was the first added)

    GET /surveys/<id>/responses/1

    => {'answer_strings' : ['answer1', 'answer2']}

Getting the Nth answer to the Mth question:

    GET /surveys/<id>/responses/N/answers/M

    => {'answer_text' : 'answerM'}

Getting general details on a survey:

    GET /surveys/123

    =>    {
              "id": 123,
              "name": "My Survey",
              "questions": [
                  "What?",
                  "Why?",
                  ...
              ],
              "tag_options": [
                  "Boring answer",
                  "Interesting answer",
                  ...
              ],
              "response_count": 100,
              "published": true
          }

### Serialization ###

Details of the various serialized objects:

 * Survey - id, name, date created, questions, tags, response count, and published state. The questions and tags appear simply as a list of strings
 * Question - question text
 * Tag - tag text
 * Response - a list of answers
 * Answer - an answer text and associated tags

### Authentication ###

Designed and unit-tested to provide survey owner access only, except for response postings (see API details below). The website includes login and registration pages (probably the beef of my front end work so far here) and supports token authentication.

### Database design ###

Some notes on the database laylout, which closely mirrors the RESTful URI choices:

	         Survey
	_______________________
	|          |          |
	Questions  Responses  Tags
	           |
	           Answers

The Survey object is, obviously, the top-level object of an entire survey. As well as an owner (user), it is associated with a list of questions created before the survey is published, and a list of responses, each added when a respondent takes the survey. Lastly, the Survey is associated with a set of tags, which are added/modified by the survey owner (not necessarily before publishing the survey).

Each response houses a list of individual Answers, which contain the textual response. If a Survey is published with N questions, each response generated automatically has N answers, to be filled in by the participant. Each answer is also foreign keyed to a Tag object. Crucially, this means that when associating an individual answer with a tag, that tag has to be predeclared on the survey. Tags can then be edited trivially without trawling through individual responses.
