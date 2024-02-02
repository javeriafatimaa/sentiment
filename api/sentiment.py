from flask import Blueprint, jsonify, request
from textblob import TextBlob

sentiment = Blueprint('sentiment', __name__)


@sentiment.route('/analyze_sentiment', methods=['POST'])
def analyze_sentiment():
    try:
        data = request.get_json()

        comments = data.get('comments', [])
        print(comments)
        positive_comments = []
        negative_comments = []

        for comment in comments:
            blob = TextBlob(comment)

            # Perform sentiment analysis
            sentiment_polarity = blob.sentiment.polarity
            sentiment_subjectivity = blob.sentiment.subjectivity

            result = {
                'comment': comment,
                'sentiment_polarity': sentiment_polarity,
                'sentiment_subjectivity': sentiment_subjectivity
            }

            if sentiment_polarity > 0:
                positive_comments.append(result)
            elif sentiment_polarity < 0:
                negative_comments.append(result)

        return jsonify({
            'positive_comments': positive_comments,
            'negative_comments': negative_comments
        })

    except Exception as e:
        return jsonify({'error': str(e)})
        
@sentiment.route('/analyze', methods=['POST'])
def analyze():
    try:
        data = request.json

        if 'arrayOfQuestions' not in data:
            return jsonify({"error": "Invalid input format"}), 400

        array_of_questions = data['arrayOfQuestions']

        total_responses = len(array_of_questions)
        total_sentiment_score = 0
        total_responses_for_most_selected = 0

        results_questions = []
        results_most_selected = []

        for question in array_of_questions:
            most_selected_option = question.get("mostSelected", None)
            options = question.get("options", [])
            label = question.get("label", "")

            # Perform sentiment analysis for the question
            question_blob = TextBlob(label)
            question_sentiment_polarity = question_blob.sentiment.polarity
            question_sentiment_subjectivity = question_blob.sentiment.subjectivity
            question_sentiment_score = question_sentiment_polarity * 100
            total_sentiment_score += question_sentiment_score

            result_question = {
                "label": label,
                "options": options,
                "question_sentiment_polarity": question_sentiment_polarity,
                "question_sentiment_subjectivity": question_sentiment_subjectivity,
                "question_sentiment_score": question_sentiment_score
            }

            results_questions.append(result_question)

            # Check if most selected option is available and analyze its sentiment
            if most_selected_option:
                most_selected_blob = TextBlob(most_selected_option)
                most_selected_sentiment_polarity = most_selected_blob.sentiment.polarity
                most_selected_sentiment_subjectivity = most_selected_blob.sentiment.subjectivity
                most_selected_sentiment_score = most_selected_sentiment_polarity * 100

                # Increment the total responses for the most selected option
                total_responses_for_most_selected += 1

                result_most_selected = {
                    "most_selected_option": most_selected_option,
                    "most_selected_sentiment_polarity": most_selected_sentiment_polarity,
                    "most_selected_sentiment_subjectivity": most_selected_sentiment_subjectivity,
                    "most_selected_sentiment_score": most_selected_sentiment_score
                }

                results_most_selected.append(result_most_selected)

        # Calculate the average sentiment score for questions
        average_sentiment_score = total_sentiment_score / total_responses

        # Calculate the percentage of people who selected the most positive option
        percentage_positive_most_selected = (total_responses_for_most_selected / total_responses) * 100

        # Multiply the sentiment scores by 100 as requested
        for result in results_questions:
            result["question_sentiment_score"] *= 100

        for result in results_most_selected:
            result["most_selected_sentiment_score"] *= 100

        return jsonify({
            "total_responses": total_responses,
            "average_sentiment_score": average_sentiment_score,
            "percentage_positive_most_selected": percentage_positive_most_selected,
            "results_questions": results_questions,
            "results_most_selected": results_most_selected
        })

    except Exception as e:
        return jsonify({'error': str(e)})
