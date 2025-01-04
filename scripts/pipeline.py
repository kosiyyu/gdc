from extract_world_backup import main as extract_world_backup
from run import main as run
from create_world_backup import main as create_world_backup
from transfer_world import main as transfer_world

def pipeline():
    extract_world_backup()
    run()
    create_world_backup()
    transfer_world()