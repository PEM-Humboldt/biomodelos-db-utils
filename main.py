def define_env(env):

    import os, yaml, subprocess

    base_path = os.path.join(env.project_dir, "docs", "commands")

    def get_help(cmd):
        result = subprocess.run(
            cmd + ["--help"],
            capture_output=True,
            text=True,
        )
        return result.stdout
    
    @env.macro
    def command():
        """
        Returns the YAML corresponding to the current page name.
        """
        page_name = env.page.title.lower()

        yml_file = os.path.join(base_path, f"{page_name}.yml")

        if os.path.exists(yml_file):
            with open(yml_file, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
            for note in data.get("notes", []):
                if note.get("auto_help"):
                    cmd = ["bmdbutils"] + page_name.split()
                    note["description"] = f"```text\n{get_help(cmd)}\n```"
            return data
        else:
            return {"error": f"{page_name}.yml doesn't exist"}