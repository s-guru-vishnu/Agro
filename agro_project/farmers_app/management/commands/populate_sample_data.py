from django.core.management.base import BaseCommand
from farmers_app.db_connection import get_services_collection
import random
from datetime import datetime

class Command(BaseCommand):
    help = 'Populate sample data for fertilizers, machines, and manpower'

    def handle(self, *args, **options):
        services_collection = get_services_collection()


        base_lat = 10.999671
        base_lon = 77.084172


        locations = [
            {'city': 'Coimbatore', 'state': 'Tamil Nadu', 'pincode': '641001'},
            {'city': 'Pollachi', 'state': 'Tamil Nadu', 'pincode': '642001'},
            {'city': 'Mettupalayam', 'state': 'Tamil Nadu', 'pincode': '641301'},
            {'city': 'Tiruppur', 'state': 'Tamil Nadu', 'pincode': '641601'},
            {'city': 'Erode', 'state': 'Tamil Nadu', 'pincode': '638001'},
            {'city': 'Salem', 'state': 'Tamil Nadu', 'pincode': '636001'},
            {'city': 'Udumalpet', 'state': 'Tamil Nadu', 'pincode': '642126'},
            {'city': 'Palani', 'state': 'Tamil Nadu', 'pincode': '624601'},
            {'city': 'Dindigul', 'state': 'Tamil Nadu', 'pincode': '624001'},
            {'city': 'Karur', 'state': 'Tamil Nadu', 'pincode': '639001'},
        ]


        fertilizer_names = [
            'NPK 19:19:19', 'Urea', 'DAP (Diammonium Phosphate)', 'Potash', 'Super Phosphate',
            'Ammonium Sulphate', 'Zinc Sulphate', 'Boron', 'Iron Chelate', 'Organic Compost',
            'Vermicompost', 'Farm Yard Manure', 'Bio Fertilizer', 'Seaweed Extract', 'Fish Meal',
            'Bone Meal', 'Neem Cake', 'Mustard Cake', 'Groundnut Cake', 'Coconut Cake',
            'NPK 20:20:20', 'NPK 15:15:15', 'NPK 12:12:12', 'NPK 17:17:17', 'NPK 14:14:14',
            'Micronutrient Mix', 'Calcium Nitrate', 'Magnesium Sulphate', 'Manganese Sulphate',
            'Copper Sulphate', 'Molybdenum', 'Sulphur', 'Gypsum', 'Lime', 'Rock Phosphate',
            'Single Super Phosphate', 'Triple Super Phosphate', 'Muriate of Potash',
            'Sulphate of Potash', 'Ammonium Nitrate', 'Calcium Ammonium Nitrate',
            'NPK 10:26:26', 'NPK 12:32:16', 'NPK 20:10:10', 'NPK 15:15:15', 'NPK 19:19:19',
            'NPK 17:17:17', 'NPK 14:14:14', 'NPK 12:12:12', 'NPK 20:20:20', 'NPK 15:15:15'
        ]


        machine_names = [
            'Mahindra 575 DI', 'John Deere 5050D', 'Sonalika DI 35', 'New Holland 3630',
            'Eicher 380', 'Swaraj 744', 'Farmtrac 60', 'Preet 9090', 'Force Orchard Master',
            'Kubota M7040', 'Tractor Rotavator', 'Disc Harrow', 'Cultivator', 'Plough',
            'Seed Drill', 'Planter', 'Sprayer', 'Harvester', 'Thresher', 'Balers',
            'Tractor Trailer', 'Tillage Equipment', 'Irrigation Pump', 'Drip Irrigation System',
            'Sprinkler System', 'Power Tiller', 'Mini Tractor', 'Combine Harvester',
            'Reaper', 'Straw Reaper', 'Chaff Cutter', 'Maize Sheller', 'Groundnut Digger',
            'Potato Digger', 'Onion Harvester', 'Tomato Harvester', 'Cotton Picker',
            'Sugarcane Harvester', 'Rice Transplanter', 'Paddy Thresher', 'Wheat Thresher',
            'Corn Sheller', 'Sunflower Harvester', 'Soybean Harvester', 'Pulse Harvester',
            'Oilseed Harvester', 'Fruit Picker', 'Pruning Machine', 'Mulching Machine',
            'Compost Turner', 'Manure Spreader'
        ]


        worker_skills = [
            'Plowing and Tilling', 'Sowing and Planting', 'Harvesting', 'Irrigation Management',
            'Crop Protection', 'Organic Farming', 'Dairy Farming', 'Poultry Farming',
            'Goat Rearing', 'Fish Farming', 'Beekeeping', 'Mushroom Cultivation',
            'Vermicomposting', 'Greenhouse Management', 'Hydroponics', 'Tractor Operation',
            'Machine Maintenance', 'Soil Testing', 'Crop Rotation', 'Pest Control',
            'Weed Management', 'Fertilizer Application', 'Pruning and Training', 'Grafting',
            'Seed Treatment', 'Nursery Management', 'Orchard Management', 'Vegetable Farming',
            'Flower Cultivation', 'Medicinal Plant Farming', 'Spice Cultivation', 'Coconut Farming',
            'Banana Cultivation', 'Sugarcane Farming', 'Cotton Farming', 'Rice Farming',
            'Wheat Farming', 'Maize Farming', 'Pulse Farming', 'Oilseed Farming',
            'Fruit Picking', 'Grading and Sorting', 'Packaging', 'Transportation',
            'Warehouse Management', 'Market Linkage', 'Farm Accounting', 'Record Keeping',
            'Farm Planning', 'Crop Insurance'
        ]

        self.stdout.write('🌱 Starting to populate sample data...')





        self.stdout.write('📦 Generating 50 fertilizer entries...')
        fertilizers = []
        for i in range(50):
            location = random.choice(locations)

            lat_offset = random.uniform(-0.5, 0.5)
            lon_offset = random.uniform(-0.5, 0.5)

            fertilizer = {
                'name': fertilizer_names[i],
                'description': f'High quality {fertilizer_names[i]} suitable for all crops. Certified organic and chemical-free.',
                'service_type': 'fertilizer',
                'price': round(random.uniform(200, 5000), 2),
                'quantity': random.randint(10, 500),
                'unit': 'kg',
                'availability': True,
                'location': {
                    'address': f'{random.randint(1, 999)} Main Street',
                    'city': location['city'],
                    'state': location['state'],
                    'pincode': location['pincode'],
                    'latitude': base_lat + lat_offset,
                    'longitude': base_lon + lon_offset
                },
                'created_at': datetime.now(),
                'is_sample_data': True
            }
            fertilizers.append(fertilizer)


        self.stdout.write('🚜 Generating 50 machine entries...')
        machines = []
        for i in range(50):
            location = random.choice(locations)
            lat_offset = random.uniform(-0.5, 0.5)
            lon_offset = random.uniform(-0.5, 0.5)

            machine = {
                'name': machine_names[i],
                'description': f'Well-maintained {machine_names[i]} available for rent. Includes operator if needed.',
                'service_type': 'machine',
                'type': random.choice(['Tractor', 'Harvester', 'Tiller', 'Sprayer', 'Irrigation', 'Other']),
                'price': round(random.uniform(500, 5000), 2),
                'price_unit': 'per day',
                'availability': True,
                'location': {
                    'address': f'{random.randint(1, 999)} Farm Road',
                    'city': location['city'],
                    'state': location['state'],
                    'pincode': location['pincode'],
                    'latitude': base_lat + lat_offset,
                    'longitude': base_lon + lon_offset
                },
                'created_at': datetime.now(),
                'is_sample_data': True
            }
            machines.append(machine)


        self.stdout.write('👥 Generating 50 manpower entries...')
        manpower_list = []
        first_names = ['Ramesh', 'Suresh', 'Kumar', 'Raj', 'Mohan', 'Gopal', 'Arun', 'Vijay', 'Prakash', 'Senthil',
                      'Murugan', 'Selvam', 'Kannan', 'Muthu', 'Velan', 'Karuppan', 'Pandi', 'Durai', 'Sundaram', 'Lakshmanan',
                      'Ravi', 'Karthik', 'Sathish', 'Prabhu', 'Naveen', 'Harish', 'Deepak', 'Vinoth', 'Sakthi', 'Jegan',
                      'Manikandan', 'Saravanan', 'Karthikeyan', 'Prasanth', 'Sivakumar', 'Balaji', 'Ganesh', 'Krishnan', 'Natarajan', 'Perumal',
                      'Thangavel', 'Chinnasamy', 'Palanisamy', 'Subramanian', 'Ramanathan', 'Venkatesh', 'Srinivasan', 'Gopalakrishnan', 'Narayanan', 'Mahadevan']
        last_names = ['Kumar', 'Reddy', 'Naidu', 'Pillai', 'Iyer', 'Iyengar', 'Gounder', 'Thevar', 'Nadar', 'Chettiar']

        for i in range(50):
            location = random.choice(locations)
            lat_offset = random.uniform(-0.5, 0.5)
            lon_offset = random.uniform(-0.5, 0.5)

            worker = {
                'name': f'{random.choice(first_names)} {random.choice(last_names)}',
                'skills': ', '.join(random.sample(worker_skills, random.randint(3, 8))),
                'experience': random.randint(1, 20),
                'service_type': 'manpower',
                'rate': round(random.uniform(300, 1500), 2),
                'unit': random.choice(['per day', 'per hour', 'per acre']),
                'availability': True,
                'location': {
                    'address': f'{random.randint(1, 999)} Village Street',
                    'city': location['city'],
                    'state': location['state'],
                    'pincode': location['pincode'],
                    'latitude': base_lat + lat_offset,
                    'longitude': base_lon + lon_offset
                },
                'created_at': datetime.now(),
                'is_sample_data': True
            }
            manpower_list.append(worker)


        if fertilizers:
            result = services_collection.insert_many(fertilizers)
            self.stdout.write(self.style.SUCCESS(f'✅ Inserted {len(result.inserted_ids)} fertilizers'))

        if machines:
            result = services_collection.insert_many(machines)
            self.stdout.write(self.style.SUCCESS(f'✅ Inserted {len(result.inserted_ids)} machines'))

        if manpower_list:
            result = services_collection.insert_many(manpower_list)
            self.stdout.write(self.style.SUCCESS(f'✅ Inserted {len(result.inserted_ids)} manpower entries'))

        self.stdout.write(self.style.SUCCESS('\n🎉 Sample data population completed!'))
        self.stdout.write(f'📍 Base location: {base_lat}, {base_lon}')
        self.stdout.write(f'📊 Total entries: {len(fertilizers) + len(machines) + len(manpower_list)}')