import grpc
import os
import time
import image_pb2
import image_pb2_grpc


if __name__ == "__main__":

    with grpc.insecure_channel("localhost:8061") as channel:
        stub = image_pb2_grpc.ImageServerServiceStub(channel)

        test_folder = "extracted_zip_files/1690208762654"

        try:
            for image in os.listdir(test_folder):
                with open(test_folder+"/"+image, "rb") as f:
                    img_bytes = f.read()
                    _ = stub.PostImage(image_pb2.Image(data=img_bytes, name=image))
                    print(f"Sent {image}")
                    time.sleep(0.1)

        except grpc.RpcError as rpc_error:
            print('An error has occurred:')
            print(f'  Error Code: {rpc_error.code()}')
            print(f'  Details: {rpc_error.details()}')
