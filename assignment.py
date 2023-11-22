import json
import random

class ParkingLot:
    def __init__(self, square_footage, parking_spot_size=96):
        self.square_footage = square_footage
        self.parking_spot_size = parking_spot_size
        self.num_parking_spots = int(square_footage / parking_spot_size)
        self.parking_spots = [None] * self.num_parking_spots

    def park_car(self, car, spot_number):
        if self.parking_spots[spot_number] is not None:
            print(f"Car with license plate {car.license_plate} failed to park in spot {spot_number} because it is already occupied.")
            return False

        self.parking_spots[spot_number] = car
        print(f"Car with license plate {car.license_plate} parked successfully in spot {spot_number}.")
        return True

    def get_parked_vehicles_json(self):
        parked_vehicles_json = {}
        for spot_number, car in enumerate(self.parking_spots):
            if car is not None:
                parked_vehicles_json[spot_number] = car.license_plate

        return parked_vehicles_json

    def upload_parked_vehicles_to_s3(self, bucket_name, file_name):
        parked_vehicles_json = self.get_parked_vehicles_json()

        with open(file_name, "w") as file:
            json.dump(parked_vehicles_json, file)

        import boto3

        s3_client = boto3.client("s3", endpoint_url="https://s3.us-east-2.amazonaws.com")
        s3_client.upload_file(file_name, bucket_name, file_name)


class Car:
    def __init__(self, license_plate):
        self.license_plate = license_plate

    def __str__(self):
        return self.license_plate

    def park(self, parking_lot):
        while True:
            spot_number = random.randint(0, parking_lot.num_parking_spots - 1)
            if parking_lot.park_car(self, spot_number):
                break


if __name__ == "__main__":
    parking_lot = ParkingLot(2000)

    cars = [
        Car("ABC123"),
        Car("DEF456"),
        Car("GHI789"),
        Car("JKL012"),
        Car("MNO345"),
    ]

    while cars:
        car = cars.pop()
        car.park(parking_lot)

        if parking_lot.parking_spots.count(None) == 0:
            break

    parking_lot.upload_parked_vehicles_to_s3("your-bucket-name", "parked_vehicles.json")
