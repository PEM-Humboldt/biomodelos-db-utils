from geo.Geoserver import Geoserver as Gs

class Geoserver:
    def __init__(self, url, user, password):
        GS_URL=url
        GS_USER=user
        GS_PASS=password

        self.geo = Gs(GS_URL, username=GS_USER, password=GS_PASS)

    def create_ws(self, name):
        try:
            self.geo.create_workspace(workspace=name)
        except Exception as e:
            if e.args[0] != 'The workspace already exist':
                raise

    def load_layer(self,layer_name, file_path, workspace_name):
        self.geo.create_coveragestore(
            layer_name=layer_name,
            path=file_path,
            workspace=workspace_name
        )
