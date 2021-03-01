class model_parser:
    def __init__(self,raw_data = None):
        self.raw_data = raw_data
    def run(self):
        # list of all devices that are currently supported
        model_list = ['3700','C7200-IS-M' , 'windows','C2600-I-M']
        model_list = [x.lower() for x in model_list]
        raw_desc =  [x.lower() for x in self.raw_data["system_description"].split(" ")]
        main_model = [model.lower() for model in model_list if model in raw_desc]
        self.raw_data["device_model"] = main_model[0]
        return self.raw_data

