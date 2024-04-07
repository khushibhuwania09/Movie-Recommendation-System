import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from flask import Flask, jsonify, g, render_template
from apscheduler.schedulers.background import BackgroundScheduler
import datetime
from evaluation.online_evaluation import get_online_evaluation_statistics
from utils.file_utils import load_properties

app = Flask(__name__)
scheduler = BackgroundScheduler()

# Online evaluation metrics
macro_precision, macro_recall, micro_precision, micro_recall, recommendation_adoption, value_last_recorded = 0, 0, 0, 0, 0, datetime.datetime.now()

def refresh_online_evaluation_metrics():
    global macro_precision, macro_recall, micro_precision, micro_recall, value_last_recorded, recommendation_adoption
    macro_precision, macro_recall, micro_precision, micro_recall, recommendation_adoption = get_online_evaluation_statistics()
    value_last_recorded = datetime.datetime.now()
    return macro_precision, macro_recall, micro_precision, micro_recall, value_last_recorded, recommendation_adoption


@app.route('/evaluation_dashboard', methods=['GET'])
def evaluation_dashboard():
    metrics = {
        'macro_precision': macro_precision,
        'macro_recall': macro_recall,
        'micro_precision': micro_precision,
        'micro_recall': micro_recall,
        'online_evaluation_time': value_last_recorded,
        'recommendation_adoption': recommendation_adoption
    }
    return render_template('evaluation_dashboard.html', metrics=metrics)

if __name__ == '__main__':
    config = load_properties()
    job = scheduler.add_job(refresh_online_evaluation_metrics, 'cron', minute=int(config.get('ONLINE_EVALUATION_REFRESH_RATE_MINUTES').data))
    scheduler.start()
    app.run(debug=True, port=8087, host='0.0.0.0')