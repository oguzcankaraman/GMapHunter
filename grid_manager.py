class GridManager:
    def __init__(self, start_lat, start_lng, end_lat, end_lng, step=0.02):
        self.start_lat = start_lat
        self.start_lng = start_lng
        self.end_lat = end_lat
        self.end_lng = end_lng
        self.step = step

    def generate_coordinates(self):
        """
        Belirlenen alanı step (adım) büyüklüğünde karelere böler.
        Generator (yield) kullanarak hafızayı şişirmez.
        """
        lat = self.start_lat
        while lat < self.end_lat:
            lng = self.start_lng
            while lng < self.end_lng:
                yield lat, lng
                lng += self.step
            lat += self.step