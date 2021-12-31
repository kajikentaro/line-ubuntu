# %%
import docker
import os
from dotenv import load_dotenv
load_dotenv()


class DockerEnv:
    client = None

    def start(self):
        client = docker.from_env()
        image_name = os.getenv('sandbox_image_name')
        self.container = client.containers.run(
            image_name , "/bin/bash", remove=True, detach=True, tty=True)

    def __init__(self):
        self.start()

    def exec(self, cmd):
        try:
            exec_res = self.container.exec_run(
                "bash -c '" + cmd + "'", user="user")
        except docker.errors.APIError as e:
            print("コンテナが起動していません。再起動中です。")
            self.start()
            return
        if(exec_res.exit_code == 0):
            print("成功しました")
            print(exec_res.output.decode("utf-8"))
        else:
            print("失敗しました")
            print(exec_res.output.decode("utf-8"))

    def stop(self):
        self.container.stop()


# %%
dockerenv = DockerEnv()
# %%
#dockerenv.exec("set -o pipefail")
#dockerenv.exec("echo yes | unminimize")
# dockerenv.stop()
# %%
dockerenv.exec("man db")

# %%
