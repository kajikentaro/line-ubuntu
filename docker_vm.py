# %%
import docker
import os
import tarfile
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
        F_NAME = "exe.sh"
        TAR_NAME = "tmp.tar"
        with open(F_NAME, "w") as file:
            file.write(cmd)

        with tarfile.open(TAR_NAME, "w") as tar:
            tar.add(F_NAME)
        
        with open(TAR_NAME, "rb") as data:
            try:
                self.container.put_archive(path="/", data=data)
            except docker.errors.APIError as e:
                self.start()
                return "コンテナが起動していません。再起動中です。"

        command = "bash /{}".format(F_NAME)
        exec_res = self.container.exec_run(command, user="user")
        return exec_res.output.decode("utf-8").rstrip('\n')

    def stop(self):
        self.container.stop()