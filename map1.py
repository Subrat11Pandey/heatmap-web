import folium
import pandas
import csv
import firebase_admin
from firebase import firebase
from folium.plugins import HeatMap

firebase = firebase.FirebaseApplication("https://janaparvani-default-rtdb.firebaseio.com/",None)

# choice = int(input("press 1- Input 0- Output : "))
finaldata = firebase.get('Problems', '')

item = finaldata.items()
def enter_location():
    for key, val in finaldata.items():
        # print(key)
        # print(val['Latitude'])
        lat = (val["Latitude"])
        lon = (val["Longitude"])
        flag = (val["Flag"])
        if(flag==0):
            problem_title =  (val["Problems"])
            problem =(int(val["Severity"])/10)
            print(key,lat,lon,problem_title,problem)

        # lat = input("Enter the latitude")
        # lon = input("Enter the longitude")

            with open('trial.csv', mode='a') as trial_file:
                trial_writer = csv.writer(trial_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                trial_writer.writerow([problem,problem_title, lat, lon])
            flag = 1
            firebase.post('/Problems/'+key+'/Flag',flag)

def display_location():
    with open('trial.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            else:
                try:
                    print(f'\t{row[0]}, {row[1]}, {row[2]}', {row[3]})
                    line_count += 1
                except Exception:
                    pass


def maping():
    data = pandas.read_csv("trial.csv")
    lat = list(data["LAT"])
    lon = list(data["LON"])
    problem = list(data["PROB"])
    problem_title = list(data["STATEMENT"])

    def color_producer (problem):

        if (problem<3):
                return "green"
        elif (problem>=3 and problem<=6):
                return "orange"
        else:
            return "red"
    map = folium.Map(location=[12.961264, 77.562666], zoom_start =12 ,tiles = "Stamen Terrain")

    fg= folium.FeatureGroup(name="My Map")
    for lt , ln , problem, problem_title in zip(lat, lon,problem,problem_title):
        tx= (problem,problem_title)
        fg.add_child(folium.CircleMarker(location=[lt , ln ],radius =6, popup=tx,fill_color=color_producer(problem), color = 'black',fill = True , fill_opacity = 0.7))




    map.add_child(fg)
    map.save("Map1.html")
data_array = []
def heatmap():
    k = []
    data = pandas.read_csv("trial.csv")
    lat = list(data["LAT"])
    lon = list(data["LON"])
    problem = list(data["PROB"])
    for lt , ln , problem in zip(lat, lon,problem):
        k= [lt , ln , problem]
        data_array.append(k)
    
    print(k)
    
    mapObj = folium.Map(location=[12.961264, 77.562666], zoom_start =12 ,tiles = "Stamen Terrain")
    # print(data_val)
    HeatMap(data_array).add_to(mapObj)
    mapObj.save("outpot.html")






# enter_location()
heatmap()
# maping()
# display_location()
