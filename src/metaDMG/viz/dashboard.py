from typing import Optional
from pathlib import Path
from metaDMG.viz import app, viz_utils


def start_dashboard(
    results_dir: Optional[Path] = None,
    debug: bool = False,
    host: str = "0.0.0.0",
    port: int = 8050,
):

    if results_dir is None:
        raise Exception(f"Has to be specified.")

    if not debug:
        viz_utils.open_browser_in_background(port)

    dashboard_app = app.get_app(results_dir)

    dashboard_app.run_server(
        debug=debug,
        host=host,
        port=str(port),
        use_reloader=False,
    )
