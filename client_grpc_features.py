import grpc
import time
import logging
import myitems_pb2 as myitems_pb2
import myitems_pb2_grpc as myitems_pb2_grpc


logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def RunClient():
    
    channel = grpc.insecure_channel('localhost:50051')
    
    stub = myitems_pb2_grpc.ItemServiceStub(channel) # object represents grpc, use this to access the methods
    logging.info("*** Client connected to server at localhost:50051\n")


    # 3. Client-streaming
    def AddItemsRequest(): 
        
        newItemsName = [
            "Wireless Mouse",
            "White Board",
            "External SSD"
        ]
        
        for name in newItemsName:
            yield myitems_pb2.ItemNameRequest(itemName=name)
            logging.info(f"Adding item: '{name}'\n")
              
    AddItemsMethodResponse = stub.AddItems( AddItemsRequest() )
    
    logging.info(f"Number of items added: {AddItemsMethodResponse.numberItemsAdded}\n\n")


    # 1. Unary call
    itemsIdToGet = [1, 7, 999] 
    
    for itemIdToGet in itemsIdToGet:
        logging.info(f"Requesting item with ID: {itemIdToGet}\n")
        
        try:
            GetItemByIdMethodResponse = stub.GetItemById( myitems_pb2.ItemIdRequest(itemId=itemIdToGet) )
            logging.info(f"GetItemById: ID={GetItemByIdMethodResponse.itemId}, Name='{GetItemByIdMethodResponse.itemName}'\n")
        
        except grpc.RpcError as error:
            logging.info(f"GetItemById failed for ID {itemIdToGet}: {error.code()} - {error.details()}\n")

    
    # 2. Server-streaming
    logging.info(f"Requesting to list all items\n")
    
    ListAllItemsMethodResponse = stub.ListAllItems( myitems_pb2.Empty() )
    
    for item in ListAllItemsMethodResponse: 
        logging.info(f"Item ID: {item.itemId}, Name: '{item.itemName}'\n")


    # 4. Bidirectional
    def ChatAboutItemsRequested():
        
        chatMessages = [
            "Hello, this is the client speaking.",
            "My name is Hung.",
            "I'm from Vietnam.",
            "This is Distributed Software Architecture course."
        ]
        
        for msgContent in chatMessages:
            logging.info(f"Sending chat message: '{msgContent}'\n")
            yield myitems_pb2.ChatMessage(content=msgContent)
            time.sleep(0.1)
    
    ChatAboutItemsMethodResponse = stub.ChatAboutItems(ChatAboutItemsRequested())
    
    for serverMsg in ChatAboutItemsMethodResponse: 
        logging.info(f"Server replied: {serverMsg.content}\n")
    
    logging.info("Chat finished\n\n")


if __name__ == '__main__':
    RunClient()
    logging.info("*** Client application finished\n")
