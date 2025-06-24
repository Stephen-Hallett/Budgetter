import os

import litserve as ls

from .NearestNeighbours.VotingNN import VotingNN

if __name__ == "__main__":
    nn1_model = VotingNN(api_path="/1nn")
    server = ls.LitServer(lit_api=[nn1_model], accelerator="auto")
    server.run(port=os.environ["MODELS_PORT"])
