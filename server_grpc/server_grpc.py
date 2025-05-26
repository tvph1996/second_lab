import grpc
from concurrent import futures
import proto.myitems_pb2 as myitems_pb2
import proto.myitems_pb2_grpc as myitems_pb2_grpc
import time
import logging


# CONFIGURATIONS
ENABLE_LOGGING_INTERCEPTOR = False
ENABLE_REFLECTION = False

NEW_MAX_MESSAGE_SIZE = 10 * 1024 * 1024

if ENABLE_REFLECTION:
    from grpc_reflection.v1alpha import reflection

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

itemsData = { # hard coded default items
    1: myitems_pb2.ItemInfo(itemId=1, itemName="Table"),
    2: myitems_pb2.ItemInfo(itemId=2, itemName="Chair"),
    3: myitems_pb2.ItemInfo(itemId=3, itemName="Black Board"),
    4: myitems_pb2.ItemInfo(itemId=4, itemName="Monitor"),
    5: myitems_pb2.ItemInfo(itemId=5, itemName="Projector"),
    6: myitems_pb2.ItemInfo(itemId=6, itemName="PC"),
    7: myitems_pb2.ItemInfo(itemId=7, itemName="Laptop"),
}

nextItemId = 8


class LoggingInterceptor(grpc.ServerInterceptor):
    def intercept_service(self, continuation, handler_call_details):
        method = handler_call_details.method
        logging.info(f"Interceptor Logging: gRPC call: {method}")
        return continuation(handler_call_details)


class ItemServiceServicer(myitems_pb2_grpc.ItemServiceServicer): # Inherit base class from gRPC

    def GetItemById(self, request: myitems_pb2.ItemIdRequest, context): 
        
        logging.info(f"*** GetItemById called for itemId: {request.itemId}\n")
        
        itemIdToFind = request.itemId 
        
        if itemIdToFind in itemsData:
            item = itemsData[itemIdToFind] 
            logging.info(f"Found item: {item}\n")
            return item
        else:
            logging.info(f"Item with itemId {itemIdToFind} not found\n")
            context.set_code(grpc.StatusCode.NOT_FOUND) # send to client
            context.set_details(f"Item with ID {itemIdToFind} not found") # send to client
            return myitems_pb2.ItemInfo()

    
    def ListAllItems(self, request: myitems_pb2.Empty, context): 
        
        logging.info("*** ListAllItems called\n")
        
        if not itemsData:
            logging.info("itemsData is empty. No item to show\n")
            return 
        
        itemIds = list(itemsData.keys())
        
        for itemId in itemIds: 
            item = itemsData[itemId]
            logging.info(f"Item: {item}")
            yield item          
            time.sleep(0.1)


    def AddItems(self, request_iterator, context): 
        
        global nextItemId 
        logging.info("*** AddItems called\n")
        itemsAddedCount = 0 

        for itemReq in request_iterator: 
            logging.info(f"Received item to add: Name='{itemReq.itemName}'\n")

            currentId = nextItemId 
            
            newItem = myitems_pb2.ItemInfo( 
                itemId=currentId,
                itemName=itemReq.itemName,
            )
            
            itemsData[currentId] = newItem
            
            nextItemId += 1
            itemsAddedCount += 1
            
            logging.info(f"Added new item: {newItem}")

        logging.info(f"*** AddItems finished. Total items added: {itemsAddedCount}\n\n")        

        return myitems_pb2.AddItemsMethodResponse(numberItemsAdded=itemsAddedCount)


    def ChatAboutItems(self, request_iterator, context): 
        logging.info("*** ChatAboutItems called\n")
        for clientMessage in request_iterator: 
            logging.info(f"Client says: '{clientMessage.content}'\n")
            
            replyContent = f"Server acknowledges your message: '{clientMessage.content}'" 
            serverReply = myitems_pb2.ChatMessage(content=replyContent) 
            logging.info(f"Reply sent\n")
            yield serverReply

    def AddItemPerformanceTest(self, request: myitems_pb2.ItemInfo, context):
        if request.itemId == 100000:
            itemsData[request.itemId] = request 
            logging.info(f"*** AddItemPerformanceTest called\n")  
        return request


def Serve():

    server_options = [
        ('grpc.max_receive_message_length', NEW_MAX_MESSAGE_SIZE),
        ('grpc.max_send_message_length', NEW_MAX_MESSAGE_SIZE),
    ]
        
    if ENABLE_LOGGING_INTERCEPTOR:
        LoggingInterceptorInstance = LoggingInterceptor()
        logging.info("Logging interceptor is enabled\n")
    else:
        logging.info("Logging interceptor is disabled\n")
    
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10), interceptors=[LoggingInterceptorInstance] if ENABLE_LOGGING_INTERCEPTOR else None, options=server_options)
    
    myitems_pb2_grpc.add_ItemServiceServicer_to_server(ItemServiceServicer(), server)
    
    if ENABLE_REFLECTION:
        logging.info("Reflection is enabled\n")
        SERVICE_NAMES = (myitems_pb2.DESCRIPTOR.services_by_name['ItemService'].full_name, reflection.SERVICE_NAME)
        reflection.enable_server_reflection(SERVICE_NAMES, server)
    else:
        logging.info("Reflection is disabled\n")
    
    port = "50051"
    
    server.add_insecure_port(f"[::]:{port}")
    
    server.start()
    
    logging.info(f"*** gRPC server started with default items loaded. Listening on port {port}\n")
    
    try:
        while True:
            time.sleep(3600)
    except KeyboardInterrupt:
        server.stop(0)
        logging.info("*** Server shut down\n")


if __name__ == "__main__":
    Serve() 