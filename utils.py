import os 
from datetime import datetime 

def write_log(message, exception=None):
    """
        Escribe errores en el log del reporte.
    """
        
    LOG_DIR = "logs/prod_report"
    
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    
    LOG_FILE = os.path.join(
    LOG_DIR,
        f"log_rp_prod_{timestamp}.txt"
    )

    os.makedirs(LOG_DIR, exist_ok=True)

    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(f"[{timestamp}] {message}\n")
        f.write("-" * 20 + "\n")
        if exception:
            f.write(f"Exception: {str(exception)}\n")

   