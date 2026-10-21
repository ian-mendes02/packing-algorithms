def generate_config():
    from os import path, getcwd
    from data import ROOT
    from shutil import copyfile

    root = getcwd()
    config_path = path.join(root, "config.json")
    default_config_path = path.join(ROOT, "default_config.json")

    if path.exists(config_path):
        print(f"Configuration file already exists at {config_path}.")
    else:
        copyfile(default_config_path, config_path)
        print(f"Configuration file created at {config_path}.")
