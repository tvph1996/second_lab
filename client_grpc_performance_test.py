import grpc
import requests
import time
import logging
import proto.myitems_pb2 as myitems_pb2
import proto.myitems_pb2_grpc as myitems_pb2_grpc


# CONFIGURATIONS

NUM_CALLS = (1, 4, 16, 64, 256, 1024, 4096, 16384, 65536, 262144)
NUM_STRINGS = (1, 4, 16, 64, 256, 1024, 4096, 16384, 65536, 262144)

""" NUM_CALLS = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
NUM_STRINGS = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10) """

ITEM_ID_TO_REQUEST = 100000

GRPC_SERVER_URL = 'localhost:50051'

REST_ENDPOINT_URL = "http://localhost:8000/items/" 

NEW_MAX_MESSAGE_SIZE = 10 * 1024 * 1024

scenario = (
    (NUM_STRINGS[0], NUM_CALLS[0]),
    (NUM_STRINGS[0], NUM_CALLS[1]),
    (NUM_STRINGS[0], NUM_CALLS[2]),
    (NUM_STRINGS[0], NUM_CALLS[3]),
    (NUM_STRINGS[0], NUM_CALLS[4]),
    (NUM_STRINGS[0], NUM_CALLS[5]),
    (NUM_STRINGS[0], NUM_CALLS[6]),
    (NUM_STRINGS[0], NUM_CALLS[7]),
    (NUM_STRINGS[0], NUM_CALLS[8]),
    (NUM_STRINGS[0], NUM_CALLS[9]),

    (NUM_STRINGS[1], NUM_CALLS[0]),
    (NUM_STRINGS[2], NUM_CALLS[0]),
    (NUM_STRINGS[3], NUM_CALLS[0]),
    (NUM_STRINGS[4], NUM_CALLS[0]),
    (NUM_STRINGS[5], NUM_CALLS[0]),
    (NUM_STRINGS[6], NUM_CALLS[0]),
    (NUM_STRINGS[7], NUM_CALLS[0]),
    (NUM_STRINGS[8], NUM_CALLS[0]),
    (NUM_STRINGS[9], NUM_CALLS[0]),

    (2, 2),
    (4, 4),
    (8, 8),
    (16, 16),
    (32, 32),
    (64, 64),
    (128, 128),
    (256, 256),
    (512, 512)
)



baseString = "HochschuleAnhalt"

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')




def RunPerformanceTest():
    
    for case in scenario:
        sentString = baseString * case[0]
          
        ### gRPC block start ###
        
        client_options = [
            ('grpc.max_receive_message_length', NEW_MAX_MESSAGE_SIZE),
            ('grpc.max_send_message_length', NEW_MAX_MESSAGE_SIZE),
        ]

        channel = grpc.insecure_channel(GRPC_SERVER_URL, options=client_options)
        stub = myitems_pb2_grpc.ItemServiceStub(channel)
        
        stub.AddItemPerformanceTest(myitems_pb2.ItemInfo(itemId=ITEM_ID_TO_REQUEST, itemName=sentString))
        #logging.info(f"*** gRPC: Added string * {case[0]}\n")
 
        successfulCalls = 0
        failedCalls = 0
        
        startTime = time.perf_counter()

        for _ in range(case[1]):
            GetItemByIdMethodResponse = stub.GetItemById(myitems_pb2.ItemIdRequest(itemId=ITEM_ID_TO_REQUEST)) 
            
            if GetItemByIdMethodResponse and GetItemByIdMethodResponse.itemId == ITEM_ID_TO_REQUEST:
                successfulCalls += 1
            else:
                failedCalls += 1 
                
        endTime = time.perf_counter()
        totalDuration = endTime - startTime
        averageTimePerCall = totalDuration / case[1]

        logging.info(f"+++ Current scenario: String * {case[0]} and {case[1]} Calls +++\n")

        logging.info(f"----- gRPC Performance Results ---")
        logging.info(f"Total calls made: {case[1]}")
        logging.info(f"Successful calls: {successfulCalls}")
        logging.info(f"Failed calls: {failedCalls}")
        logging.info(f"Total time for {case[1]} calls: {totalDuration:.6f} second(s)")
        logging.info(f"Average time per call: {averageTimePerCall:.6f} second(s)\n")

        channel.close() 
        ### gRPC block end ###

    
        ### REST block start ### 
    
        with requests.Session() as session:

            itemPayloadRest = {
                    "id": ITEM_ID_TO_REQUEST,
                    "name": sentString     
            }

            session.post(REST_ENDPOINT_URL, json=itemPayloadRest)

            #logging.info(f"*** REST: Added string * {case[0]}\n")
            
            successfulCalls = 0
            failedCalls = 0

            startTime = time.perf_counter()

            for _ in range(case[1]):
                try:
                    response = session.get(REST_ENDPOINT_URL + str(ITEM_ID_TO_REQUEST))     
                    successfulCalls += 1

                except requests.exceptions.RequestException:
                    failedCalls += 1
                    
            endTime = time.perf_counter()

            totalDuration = endTime - startTime
            averageTimePerCall = totalDuration / case[1]

            logging.info(f"----- REST API Performance Results ---")
            logging.info(f"Total calls made: {case[1]}")
            logging.info(f"Successful calls: {successfulCalls}")
            logging.info(f"Failed calls: {failedCalls}")
            logging.info(f"Total time for {case[1]} calls: {totalDuration:.6f} second(s)")
            logging.info(f"Average time per call: {averageTimePerCall:.6f} second(s)\n")

            logging.info("+++ Finished current scenario +++\n\n\n")

        ### REST block end ###


if __name__ == '__main__':  
    RunPerformanceTest()      
    logging.info("===== All Performance Comparison Tests Finished =====\n")
    
