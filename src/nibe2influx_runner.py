from nibe2influx.nibe2influx import main

class TestDatabase:

    def persist(self, measurement):
        print(measurement)

if __name__ == '__main__':
    main(db=TestDatabase())