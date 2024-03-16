from wandb_wrapper import WandBIntegration
from opts import parse_opts

def initialize_wandb():
    opt = parse_opts()
    Agent = WandBIntegration(
        project_name='baseline-modal',
        id=opt.wandb_run_id,
        config={},
        entity=opt.wandb_entity,
        save_code=False,
        reinit=False,
        tags=['baseline'],
        api_key=opt.wandb_api_key
    )
    Agent.init_run()
    return Agent

