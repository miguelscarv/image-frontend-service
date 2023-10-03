import grpc
import io
import matplotlib.pyplot as plt

from PIL import Image
import image_pb2
import image_pb2_grpc

def display_image(image):
    img = Image.open(io.BytesIO(image.data))
    print(image.name)
    print(image.aux)
    ax = plt.gca()
    ax.imshow(img)
    plt.show()

if __name__ == "__main__":

    with grpc.insecure_channel("localhost:8061") as channel:
        stub = image_pb2_grpc.ImageServerServiceStub(channel)

        try:
            for image in stub.GetImageStream(image_pb2.Empty()):
                display_image(image)
        except grpc.RpcError as rpc_error:
            print('An error has occurred:')
            print(f'  Error Code: {rpc_error.code()}')
            print(f'  Details: {rpc_error.details()}')
