import logging
import grpc 
import image_pb2
import image_pb2_grpc
import concurrent.futures as futures
import grpc_reflection.v1alpha.reflection as grpc_reflect
import os
import time
import json

INPUT_DIR = "./extracted_zip_files/"
OUTPUT_DIR = "./received_images/"
DELAY = 2
_SERVICE_NAME = 'ImageServerService'

class ImageServer(image_pb2_grpc.ImageServerServiceServicer):

    def __init__(self) -> None:
        super().__init__()
        self.input_dir = INPUT_DIR
        self.output_dir = OUTPUT_DIR
        if os.listdir(self.input_dir) != []:
            self.max_input_sub_dir = int(max(os.listdir(self.input_dir)))
        else:
            self.max_input_sub_dir = -1

    def new_input_sub_dir(self) -> int:
        """
        Returns smallest new sub directory if it exists
        """

        subdirs = [int(i) for i in os.listdir(self.input_dir) if os.path.isdir(os.path.join(self.input_dir, i))]
        iterator = filter(
            lambda x: x > self.max_input_sub_dir,
            subdirs
        )

        l = list(iterator)
        if l == []:
            return -1
        else:
            return min(l)

    def GetImageStream(self, request, context):
        has_json = False

        while True:
            temp = self.new_input_sub_dir()
            if temp > self.max_input_sub_dir:
                self.max_input_sub_dir = temp
                #print("Found new dir in input.. going to send it")
                break
            else:
                time.sleep(DELAY)
                #print("Sleeping - no new dirs in input")
        
        time.sleep(10)
        new_path = self.input_dir + "/" + str(self.max_input_sub_dir)
        imgs = os.listdir(new_path)
        logging.info(f"Number of files in folder: {len(imgs)}")
        
        for img in imgs:
            if ".json" in img:
                has_json = True
                with open(os.path.join(new_path, img)) as f:
                    json_file = json.load(f)

        for img in imgs:
            if img.lower().endswith(('.png', '.jpg', '.jpeg')):
                with open(new_path+"/"+img, "rb") as f:
                    img_bytes = f.read()
                    if not has_json:
                        yield image_pb2.Image(data=img_bytes, name=img, is_last=imgs[-1]==img)
                    else:
                        _id = img.split(".")[0].split("_")[-1]
                        yield image_pb2.Image(data=img_bytes, name=img, is_last=imgs[-1]==img, aux=json.dumps(json_file[_id]))
                    logging.info(f" Sent image {img}...")
                    #time.sleep(0.1)

    def PostImage(self, request, context):

        data, name = request.data, request.name
        current_time = str(time.time()).replace(".", "")[:13]
        os.mkdir(self.output_dir+"/"+current_time)

        if name == "":
            name = current_time

        with open(self.output_dir+"/"+current_time+"/"+name, "wb") as f:
            f.write(data)

        return image_pb2.Empty()


def serve():
    server = grpc.server(futures.ThreadPoolExecutor())
    image_pb2_grpc.add_ImageServerServiceServicer_to_server(
        ImageServer(),
        server)
    SERVICE_NAME = (
        image_pb2.DESCRIPTOR.services_by_name[_SERVICE_NAME].full_name,
        grpc_reflect.SERVICE_NAME
    )
    grpc_reflect.enable_server_reflection(SERVICE_NAME, server)
    server.add_insecure_port('[::]:8061')
    
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
