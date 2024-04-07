import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from utils.file_utils import read_movie_file, load_properties
import datetime

def get_online_evaluation_statistics():
    """
    Returns: The macro_precision, macro_recall, micro_precision, micro_recall values of online recommendation data
    """
    config = load_properties()
    print("Running Online evaluation service")
    movies_watched_data = read_movie_file(config.get('MOVIES_WATCHED_FILE_PATH').data)
    movies_recommended_data = read_movie_file(config.get('MOVIES_RECOMMENDED_FILE_PATH').data)
    macro_precision, macro_recall, micro_precision, micro_recall, total_recommendations, total_movies_watched = 0, 0, 0, 0, 0, 0
    at_least_one_recommended_watched = 0

    for user in movies_recommended_data:
        recommendations = set(movies_recommended_data[user])
        movies_watched = set(movies_watched_data.get(user, []))
        precision_intersection = len(recommendations.intersection(movies_watched))
        recall_intersection = len(movies_watched.intersection(recommendations))
        precision, recall = 0, 0

        if len(recommendations):
            precision = precision_intersection / len(recommendations)

        if len(movies_watched):
            recall = recall_intersection / len(movies_watched)

        if precision_intersection > 0:
            at_least_one_recommended_watched += 1

        macro_precision += precision
        macro_recall += recall

        micro_precision += precision_intersection
        micro_recall += recall_intersection
        total_recommendations += len(recommendations)
        total_movies_watched += len(movies_watched)

        current_time = datetime.datetime.now()
        if current_time.minute >= 55:
            break

    macro_precision = macro_precision / len(movies_recommended_data)
    macro_recall = macro_recall / len(movies_recommended_data)

    if total_recommendations:
        micro_precision = micro_precision / total_recommendations
    else:
        micro_precision = 0

    if total_movies_watched:
        micro_recall = micro_recall / total_movies_watched
    else:
        micro_recall = 0

    recommendation_adoption = at_least_one_recommended_watched / len(movies_recommended_data)

    return macro_precision, macro_recall, micro_precision, micro_recall, recommendation_adoption
