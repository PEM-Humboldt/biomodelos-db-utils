import requests


class Biomodelos:
    def __init__(self, url):
        self.url = url

    def update_model_layer(self, model_id, layer):
        r = requests.put(
            f"{self.url}/tools/models/{model_id}/layer", data={"layer_name": layer}
        )
