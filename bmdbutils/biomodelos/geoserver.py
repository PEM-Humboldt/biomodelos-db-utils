from geo.Geoserver import Geoserver as Gs


class Geoserver:
    def __init__(self, gs_url, gs_user, gs_pass):
        GS_URL = gs_url
        GS_USER = gs_user
        GS_PASS = gs_pass

        self.geo = Gs(GS_URL, username=GS_USER, password=GS_PASS)

    def create_ws(self, name):
        try:
            self.geo.create_workspace(workspace=name)
        except Exception as e:
            if e.args[0] != "The workspace already exist":
                raise

    def load_layer(self, layer_name, file_path, workspace_name):
        self.geo.create_coveragestore(
            layer_name=layer_name, path=file_path, workspace=workspace_name
        )

    def upsert_workspaces_rules(
        self, workspace: str, permission: str, role_name: str, mode: str
    ):
        self.geo.upsert_workspaces_rules(
            workspacePattern=workspace,
            permission=permission,
            role=role_name,
            mode=mode,
        )
