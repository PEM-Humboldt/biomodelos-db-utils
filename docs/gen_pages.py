import os
import yaml
import mkdocs_gen_files

template_path = os.path.join("docs", "commands.md")

commands_dir = os.path.join("docs", "commands")

summary_lines = ["- [Inicio](index.md)\n"]

command_groups = {
    "Setup": [
        "setup.yml",
        "setup api.yml",
        "setup geoserver.yml",
        "setup mongo.yml",
        "setup postgres.yml",
    ],
    "Stats": [
        "stats.yml",
        "stats downloads.yml",
        "stats groups.yml",
        "stats models.yml",
        "stats users.yml",
    ],
    "Records": [
        "records.yml",
        "records validate.yml",
        "records upload.yml",
    ],
    "Models": [
        "models.yml",
        "models ecovars.yml",
        "models editions.yml",
        "models fix_metadata.yml",
        "models geoserver_upsert.yml",
        "models ratings.yml",
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

            with open(yml_path, "r", encoding="utf-8") as yml_file:
                yml_data = yaml.safe_load(yml_file)

            if yml_data and "title" in yml_data:
                title = yml_data["title"].replace("Comando ", "")
                display_name = title.replace("-", " ")

            with mkdocs_gen_files.open(md_file, "w") as f:
                f.write(f"---\ntitle: {display_name}\n---\n\n")
                f.write(template_content)

            summary_lines.append(
                f"    - [{display_name}]({md_file})\n"
            )

    with mkdocs_gen_files.open("summary.md", "w") as f:
        f.writelines(summary_lines)

gen_files()
