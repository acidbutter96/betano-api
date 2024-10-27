from worker.tasks.pull_active_players import task_pull_active_players
from worker.tasks.pull_logged_in import task_pull_logged_in
from worker.tasks.push_bets import task_push_bets


tasks = [
    task_pull_active_players,
    task_pull_logged_in,
    task_push_bets,
]
