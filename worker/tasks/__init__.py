from tasks.pull_active_tournaments import task_pull_active_tournaments
from tasks.pull_logged_in import task_pull_logged_in
from tasks.push_bets import task_push_bets
from processing import process


task_director = {
    "pull_active_tournaments": task_pull_active_tournaments,
    "push_bets": task_push_bets,
    "pull_logged_in": task_pull_logged_in,

    # Add more tasks here...

    "default": process, # noqa  # Default task to run if none of the above match the task name provided by the user. noqa
}


tasks = [
    task_pull_active_tournaments,
    task_push_bets,
    task_pull_logged_in,
]
