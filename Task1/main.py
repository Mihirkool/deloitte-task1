#Import the necessary modules(libraries)
import json, unittest, datetime

#use the open function to open the read the three Json files

with open("./data-1.json", "r") as f:
    jsonData1 = json.load(f)
with open("./data-2.json", "r") as f:
    jsonData2 = json.load(f)
with open("./data-result.json", "r") as f:
    jsonExpectedResult = json.load(f)


#Convert Json data from format 1 to a unified format
def convertFromFormat1(jsonObject):
    #Split the location field using the '/' as the delimeter
    locationParts = jsonObject['location'].split('/')
    #create a dictionary for a unified format
    # IMPLEMENT: Conversion From Type 1
    result = {
        'deviceID': jsonObject['deviceID'],  #extract deviceID 
        'deviceType': jsonObject['deviceType'],  #extract deviceType
        'timestamp': jsonObject['timestamp'],  #extract timestamp
        'location': {
            'country': locationParts[0],  #Extract country from location
            'city': locationParts[1],  #Extract city from location
            'area': locationParts[2],  #Extract area from location
            'factory': locationParts[3],  #Extract factory from location
            'section': locationParts[4]  #Extract section from location
        },
        'data': {
            'status':
            jsonObject['operationStatus'],  #copy operationStatus to status
            'temperature': jsonObject['temp']  #copy temp to temperature
        }
    }

    return result


#convert Json data from format 2 to a unified format
def convertFromFormat2(jsonObject):
    #convert the ISO timestamp to miliseconds since epoch
    date = datetime.datetime.strptime(
        jsonObject['timestamp'],
        '%Y-%m-%dT%H:%M:%S.%fZ')  #ISO timestamp format
    timestamp = round((date - datetime.datetime(1970, 1, 1)).total_seconds() *
                      1000)  #convert to miliseconds since epoch
    #create a dictionary for a unified format
    # IMPLEMENT: Conversion From Type 1
    result = {
        'deviceID': jsonObject['device']['id'],  #extract device id
        'deviceType': jsonObject['device']['type'],  #extract device type
        'timestamp': timestamp,  #copy the converted tiemstamp
        'location': {
            'country': jsonObject['country'],  #Extract country 
            'city': jsonObject['city'],  #Extract city 
            'area': jsonObject['area'],  #Extract area 
            'factory': jsonObject['factory'],  #Extract factory 
            'section': jsonObject['section']  #Extract section 
        },
        'data': jsonObject['data']  #copy the entire 'data' field
    }

    return result


def main(jsonObject):

    result = {}

    if (jsonObject.get('device') == None):
        result = convertFromFormat1(jsonObject)
    else:
        result = convertFromFormat2(jsonObject)

    return result


class TestSolution(unittest.TestCase):

    def test_sanity(self):

        result = json.loads(json.dumps(jsonExpectedResult))
        self.assertEqual(result, jsonExpectedResult)

    def test_dataType1(self):

        result = main(jsonData1)
        self.assertEqual(result, jsonExpectedResult,
                         'Converting from Type 1 failed')

    def test_dataType2(self):

        result = main(jsonData2)
        self.assertEqual(result, jsonExpectedResult,
                         'Converting from Type 2 failed')


if __name__ == '__main__':
    unittest.main()
