import grpc
import io
import matplotlib.pyplot as plt

from PIL import Image
import PIL
import image_pb2
import image_pb2_grpc
import time

def display_image(image):
    img = Image.open(io.BytesIO(image.data))
    ax = plt.gca()
    ax.imshow(img)
    plt.show()

def flip_image(image):
    print(image.is_last)
    img = Image.open(io.BytesIO(image.data))
    img = img.transpose(PIL.Image.Transpose.FLIP_LEFT_RIGHT)
    image_bytes = io.BytesIO()
    img.save(image_bytes, format='png')
    image_bytes = image_bytes.getvalue()
    return image_pb2.Image(data=image_bytes, name=image.name.split(".")[0]+".png")

if __name__ == "__main__":

    with grpc.insecure_channel("localhost:8061") as channel:
        stub = image_pb2_grpc.ImageServerServiceStub(channel)
        image_list = []

        # Get Images
        try:
            for image in stub.GetImageStream(image_pb2.Empty()):
                #display_image(image)
                image_list.append(image)
        except grpc.RpcError as rpc_error:
            print('An error has occurred:')
            print(f'  Error Code: {rpc_error.code()}')
            print(f'  Details: {rpc_error.details()}')

        # Transform Images (in this case if flips them horizontally)
        image_list = [flip_image(i) for i in image_list]
        print("Sleeping for 10 seconds")
        time.sleep(10)
        
        # Send Flipped Images back to server
        try:
            for image in image_list:
                #display_image(image)
                stub.PostImage(image)
        except grpc.RpcError as rpc_error:
            print('An error has occurred:')
            print(f'  Error Code: {rpc_error.code()}')
            print(f'  Details: {rpc_error.details()}')
