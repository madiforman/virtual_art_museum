class Piece:
    def __init__(self, id, response):
        self.id = id
        self.data = {}
        self.process_response(response)

    def process_response(self, response):
        keys = ['title',
                'artistDisplayName',
                'image_url', 
                'department',
                'objectBeginDate', 
                'objectEndDate',
                'medium', 
                'artistDisplayBio', 
                'artistNationality']

        for key in keys:
            if key == 'image_url':
                self.data[key] = self.check_image_fields(response)
            else:
                self.data[key] = response[key]

    def check_image_fields(self, response):
        if response['primaryImage'] == '':
            if response['primaryImageSmall'] != '':
                return response['primaryImageSmall']
            if response['additionalImages'] != []:
                return response['additionalImages'][0]
        else:
            return response['primaryImage']

    def __str__(self):
        str =  f"Title: {self.data['title']} \n"
        str += f"Artist: {self.data['artistDisplayName']} \n"
        str += f"Department: {self.data['department']} \n"
        str += f"Image: {self.data['image_url']} \n"
        str += f"Date: {self.data['objectBeginDate']} - {self.data['objectEndDate']} \n"
        str += f"Medium: {self.data['medium']} \n"
        str += f"Display Bio: {self.data['artistDisplayBio']} \n"
        return str