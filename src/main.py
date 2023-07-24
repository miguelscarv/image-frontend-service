import subprocess
import grpc_server
import logging

SL_PORT = 8080
logging.basicConfig(
        format="[ %(levelname)s ] %(asctime)s (%(module)s) %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        level=logging.INFO)

logging.info(f"Starting Streamlit server at port {SL_PORT}")
subprocess.Popen(["streamlit", "run" , "src/streamlit/ZIP_Uploader.py", 
    "--server.maxUploadSize", "500",
    "--server.port", str(SL_PORT)],
    stdout=subprocess.DEVNULL)

logging.info('Starting gRPC server at [::]:8061')
grpc_server.serve()