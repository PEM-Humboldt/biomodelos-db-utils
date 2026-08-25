import os
import yaml
import mkdocs_gen_files

template_path = os.path.join("docs", "commands.md")

commands_dir = os.path.join("docs", "commands")

summary_lines = ["- [Inicio](index.md)\n"]

command_groups = {
    "Setup": [
        "setup_api.yml",
        "setup_geoserver.yml",
        "setup_mongo.yml",
        "setup_postgres.yml",
    ],
    "Stats": [
        "stats_downloads.yml",
        "stats_groups.yml",
        "stats_models.yml",
        "stats_users.yml",
    ],
    "Records": [
        "records_validate.yml",
        "records_upload.yml",
    ],
    "Models": [
        "models_ecovars.yml",
        "models_editions.yml",
        "models_ratings.yml",
        "models_fix_metadata.yml",
        "models_geoserver_upsert.yml",
    ],
}

def gen_files():
    """
    Generate md files from yml files.
    """

    with open(template_path, "r", encoding="utf-8") as tpl:
        template_content = tpl.read()

    for group_name, files in command_groups.items():
        summary_lines.append(f"- {group_name}\n")

        for fname in files:
            if not fname.endswith(".yml"):
                continue

            name = os.path.splitext(fname)[0]
            md_file = f"{name}.md"

            display_name = name.replace("_", " ").title()

            yml_path = os.path.join(commands_dir, fname)

            if os.path.exists(yml_path):
                with open(yml_path, "r", encoding="utf-8") as f:
                    data = yaml.safe_load(f) or {}
                display_name = data.get(
                    "title",
                    display_name
                )
            
            with mkdocs_gen_files.open(md_file, "w") as f:
                f.write(f"---\ntitle: {display_name}\n---\n\n")
                f.write(template_content)

            summary_lines.append(
                f"    - [{display_name}]({md_file})\n"
            )
    
    with mkdocs_gen_files.open("summary.md", "w") as f:
        f.writelines(summary_lines)

gen_files()
